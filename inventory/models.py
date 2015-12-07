# -*- coding: utf-8 -*-

import datetime
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db.models import F
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from njango.utils import ne2en
from njango.fields import BSDateField, today

from app.utils.helpers import zero_for_none, none_for_zero
from users.models import User
from core.models import FiscalYear, Party, validate_in_fy, FYManager
from core.signals import fiscal_year_signal


def alter(account, date, diff):
    Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_balance=none_for_zero(zero_for_none(F('current_balance')) + zero_for_none(diff)))


def set_transactions(model, date, *args):
    args = [arg for arg in args if arg is not None]
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(model), model_id=model.id,
        defaults={
            'date': date
        })

    for arg in args:
        matches = journal_entry.transactions.filter(account=arg[1])
        diff = 0
        if not matches:
            transaction = Transaction()
        else:
            transaction = matches[0]
            diff = zero_for_none(transaction.cr_amount)
            diff -= zero_for_none(transaction.dr_amount)
        if arg[0] == 'dr':
            transaction.dr_amount = float(arg[2])
            transaction.cr_amount = None
            diff += float(arg[2])
        elif arg[0] == 'cr':
            transaction.cr_amount = float(arg[2])
            transaction.dr_amount = None
            diff -= float(arg[2])
        elif arg[0] == 'ob':
            transaction.dr_amount = float(arg[2])
            transaction.cr_amount = None
            diff = 0
        else:
            raise Exception('Transactions can only be either "dr" or "cr".')
        transaction.account = arg[1]
        if isinstance(transaction.account.current_balance, unicode):
            transaction.account.current_balance = float(transaction.account.current_balance)
        transaction.account.current_balance += diff
        transaction.current_balance = transaction.account.current_balance
        transaction.account.save()
        journal_entry.transactions.add(transaction)
        alter(transaction.account, date, diff)


class Site(models.Model):
    name = models.CharField(max_length=250)
    head_office = models.BooleanField(default=False)
    branch_office = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.branch_office:
            Site.objects.all().update(branch_office=False)
        super(Site, self).save(*args, **kwargs)


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Inventory Categories'


class InventoryAccount(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    account_no = models.PositiveIntegerField()
    current_balance = models.FloatField(default=0)
    # current_cr = models.FloatField(null=True, blank=True)
    opening_balance = models.FloatField(default=0)
    opening_rate = models.FloatField(default=0)
    opening_rate_vattable = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.account_no) + ' [' + self.name + ']'

    def get_absolute_url(self):
        return '/inventory_account/' + str(self.id)

    @staticmethod
    def get_next_account_no():
        from django.db.models import Max

        max_voucher_no = InventoryAccount.objects.all().aggregate(Max('account_no'))['account_no__max']
        if max_voucher_no:
            return max_voucher_no + 1
        else:
            return 1

    def get_category(self):
        try:
            item = self.item
        except:
            return None
        try:
            category = item.category
        except:
            return None
        return category

    def add_category(self, category):
        category_instance, created = Category.objects.get_or_create(name=category)
        self.category = category_instance

    def get_all_categories(self):
        return self.category.get_ancestors(include_self=True)

    categories = property(get_all_categories)

    # def get_cr_amount(self, day):
    # transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
    # '-journal_entry__id', '-journal_entry__date')[:1]
    # if len(transactions) > 0:
    # return transactions[0].current_cr
    # return 0
    #
    # def get_dr_amount(self, day):
    #     #journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
    #     transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
    #         '-journal_entry__id', '-journal_entry__date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0].current_dr
    #     return 0


class Depreciation(models.Model):
    depreciation_choices = [('Fixed percentage', _('Fixed percentage')),
                            ('Compounded percentage', _('Compounded percentage')), ('Fixed price', _('Fixed price'))]
    depreciate_type = models.CharField(choices=depreciation_choices, max_length=25, default="Fixed percentage")
    depreciate_value = models.PositiveIntegerField(default=0)
    time = models.PositiveIntegerField(default=0)
    time_choices = [('days', _('Day(s)')), ('months', _('Month(s)')), ('years', _('Year(s)'))]
    time_type = models.CharField(choices=time_choices, max_length=8, default='years')

    def __str__(self):
        return unicode(self.depreciate_item.first()) + ': ' + self.depreciate_type + ' - ' + unicode(
            self.depreciate_value) + ' @ ' + unicode(self.time) + ' ' + self.time_type


class Item(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    account = models.OneToOneField(InventoryAccount, related_name='item', null=True)
    type_choices = [('consumable', _('Consumable')), ('non-consumable', _('Non-consumable'))]
    type = models.CharField(choices=type_choices, max_length=15, default='consumable')
    unit = models.CharField(max_length=50, default=_('pieces'))
    # vattable = models.BooleanField(default=True)
    property_classification_reference_number = models.CharField(max_length=20, blank=True, null=True)
    other_properties = JSONField(blank=True, null=True)
    depreciation = models.ForeignKey(Depreciation, blank=True, null=True, related_name='depreciate_item')

    def save(self, *args, **kwargs):
        account_no = kwargs.pop('account_no')
        opening_balance = kwargs.pop('opening_balance')
        opening_rate = kwargs.pop('opening_rate')
        opening_rate_vattable = kwargs.pop('opening_rate_vattable')
        if account_no:
            if self.account:
                account = self.account
                account.account_no = account_no
            else:
                account = InventoryAccount(code=self.code, name=self.name, account_no=account_no,
                                           opening_balance=opening_balance, current_balance=opening_balance,
                                           opening_rate=opening_rate, opening_rate_vattable=opening_rate_vattable)
            account.save()
            self.account = account
        super(Item, self).save(*args, **kwargs)

    def add_category(self, category):
        category_instance, created = Category.objects.get_or_create(name=category)
        self.categories.add(category_instance)

    def __unicode__(self):
        return self.name


class ItemLocation(models.Model):
    name = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class JournalEntry(models.Model):
    date = BSDateField()
    content_type = models.ForeignKey(ContentType, related_name='inventory_journal_entries')
    model_id = models.PositiveIntegerField()
    creator = GenericForeignKey('content_type', 'model_id')
    # country_of_production = models.CharField(max_length=50, blank=True, null=True)
    # size = models.CharField(max_length=100, blank=True, null=True)
    # expected_life = models.CharField(max_length=100, blank=True, null=True)
    # source = models.CharField(max_length=100, blank=True, null=True)

    @staticmethod
    def get_for(source):
        try:
            return JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(source), model_id=source.id)
        except JournalEntry.DoesNotExist:
            return None

    def __str__(self):
        return str(self.content_type) + ': ' + str(self.model_id) + ' [' + str(self.date) + ']'

    class Meta:
        verbose_name_plural = u'InventoryJournal Entries'


class Transaction(models.Model):
    account = models.ForeignKey(InventoryAccount)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    current_balance = models.FloatField(null=True, blank=True)
    journal_entry = models.ForeignKey(JournalEntry, related_name='transactions')

    def __str__(self):
        return str(self.account) + ' [' + str(self.dr_amount) + ' / ' + str(self.cr_amount) + ']'

    def total_dr_amount(self):
        dr_transctions = Transaction.objects.filter(account__name=self.account.name, cr_amount=None,
                                                    journal_entry__journal__rate=self.journal_entry.creator.rate)
        total = 0
        for transaction in dr_transctions:
            total += transaction.dr_amount
        return total

    def total_dr_amount_without_rate(self):
        dr_transctions = Transaction.objects.filter(account__name=self.account.name, cr_amount=None)
        total = 0
        for transaction in dr_transctions:
            total += transaction.dr_amount
        return total


# def set_transactions(submodel, date, *args):
# # [transaction.delete() for transaction in submodel.transactions.all()]
# # args = [arg for arg in args if arg is not None]
# journal_entry, created = JournalEntry.objects.get_or_create(
# content_type=ContentType.objects.get_for_model(submodel), model_id=submodel.id,
# defaults={
#            'date': date
#        })
#    for arg in args:
#        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
#        matches = journal_entry.transactions.filter(account=arg[1])
#        if not matches:
#            transaction = Transaction()
#            transaction.account = arg[1]
#            if arg[0] == 'dr':
#                transaction.dr_amount = float(arg[2])
#                transaction.cr_amount = None
#                transaction.account.current_dr = none_for_zero(
#                    zero_for_none(transaction.account.current_dr) + transaction.dr_amount)
#                alter(arg[1], date, float(arg[2]), 0)
#            if arg[0] == 'cr':
#                transaction.cr_amount = float(arg[2])
#                transaction.dr_amount = None
#                transaction.account.current_cr = none_for_zero(
#                    zero_for_none(transaction.account.current_cr) + transaction.cr_amount)
#                alter(arg[1], date, 0, float(arg[2]))
#            transaction.current_dr = none_for_zero(
#                zero_for_none(transaction.account.get_dr_amount(date + timedelta(days=1)))
#                + zero_for_none(transaction.dr_amount))
#            transaction.current_cr = none_for_zero(
#                zero_for_none(transaction.account.get_cr_amount(date + timedelta(days=1)))
#                + zero_for_none(transaction.cr_amount))
#        else:
#            transaction = matches[0]
#            transaction.account = arg[1]
#
#            # cancel out existing dr_amount and cr_amount from current_dr and current_cr
#            # if transaction.dr_amount:
#            #     transaction.current_dr -= transaction.dr_amount
#            #     transaction.account.current_dr -= transaction.dr_amount
#            #
#            # if transaction.cr_amount:
#            #     transaction.current_cr -= transaction.cr_amount
#            #     transaction.account.current_cr -= transaction.cr_amount
#
#            # save new dr_amount and add it to current_dr/cr
#            if arg[0] == 'dr':
#                dr_difference = float(arg[2]) - zero_for_none(transaction.dr_amount)
#                cr_difference = zero_for_none(transaction.cr_amount) * -1
#                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
#                transaction.dr_amount = float(arg[2])
#                transaction.cr_amount = None
#            else:
#                cr_difference = float(arg[2]) - zero_for_none(transaction.cr_amount)
#                dr_difference = zero_for_none(transaction.dr_amount) * -1
#                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
#                transaction.cr_amount = float(arg[2])
#                transaction.dr_amount = None
#
#            transaction.current_dr = none_for_zero(zero_for_none(transaction.current_dr) + dr_difference)
#            transaction.current_cr = none_for_zero(zero_for_none(transaction.current_cr) + cr_difference)
#            transaction.account.current_dr = none_for_zero(
#                zero_for_none(transaction.account.current_dr) + dr_difference)
#            transaction.account.current_cr = none_for_zero(
#                zero_for_none(transaction.account.current_cr) + cr_difference)
#
#        #the following code lies outside if,else block, inside for loop
#        transaction.account.save()
#        journal_entry.transactions.add(transaction)


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            # JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
            #                         model_id=instance.id).delete()
            instance.delete()


def get_next_voucher_no(cls, attr):
    from django.db.models import Max

    max_voucher_no = cls.objects.all().aggregate(Max(attr))[attr + '__max']
    if max_voucher_no:
        return max_voucher_no + 1
    else:
        return 1


class Demand(models.Model):
    release_no = models.IntegerField()
    demandee = models.ForeignKey(User, related_name='demands')
    date = BSDateField(default=today, validators=[validate_in_fy])
    purpose = models.CharField(max_length=254)

    objects = FYManager()

    def get_voucher_no(self):
        return self.release_no

    def __init__(self, *args, **kwargs):
        super(Demand, self).__init__(*args, **kwargs)
        if not self.pk and not self.release_no:
            self.release_no = get_next_voucher_no(Demand, 'release_no')

    def __str__(self):
        return unicode(self.release_no)

    @property
    def fiscal_year(self):
        return FiscalYear.from_date(self.date)

    @property
    def status(self):
        status_hash = {
            'Requested': 0,
            'Approved': 1,
            'Fulfilled': 2,
        }
        status_codes = []
        rows = self.rows.all()
        for row in rows:
            status_codes.append(status_hash[row.status])
        if not status_codes:
            return _('Empty')
        inv_hash = {v: k for k, v in status_hash.items()}
        status_text = _(inv_hash[min(status_codes)])
        if len(set(status_codes)) > 1:
            status_text = "%s %s" % (_('Partially'), _(inv_hash[max(status_codes)]))
        return status_text

    @property
    def status_code(self):
        status_hash = {
            'Requested': 0,
            'Approved': 1,
            'Fulfilled': 2,
        }
        status_codes = []
        rows = self.rows.all()
        for row in rows:
            status_codes.append(status_hash[row.status])
        if not status_codes:
            return None
        status_code = str(min(status_codes))
        if len(set(status_codes)) > 1:
            status_code = "%s%s" % ('0', str(max(status_codes)))
        return status_code


class DemandRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    # release_quantity = models.FloatField(null=True, blank=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    demand = models.ForeignKey(Demand, related_name='rows')
    statuses = [('Requested', _('Requested')), ('Approved', _('Approved')), ('Fulfilled', _('Fulfilled'))]
    status = models.CharField(max_length=9, choices=statuses, default='Requested')
    location = models.ForeignKey(ItemLocation, null=True, blank=True)
    purpose = models.CharField(max_length=100, null=True, blank=True)

    @property
    def release_quantity(self):
        return len(self.releases.all())

    def save(self, *args, **kwargs):
        self.quantity = ne2en(self.quantity)
        # self.release_quantity = ne2en(self.release_quantity)
        super(DemandRow, self).save(*args, **kwargs)

    def get_voucher_no(self):
        return self.demand.release_no

    def __unicode__(self):
        return unicode(self.item) + ' (' + unicode(self.quantity) + ')'


class EntryReport(models.Model):
    entry_report_no = models.PositiveIntegerField(blank=True, null=True)
    source_content_type = models.ForeignKey(ContentType)
    source_object_id = models.PositiveIntegerField()
    source = GenericForeignKey('source_content_type', 'source_object_id')

    @property
    def fiscal_year(self):
        return FiscalYear.from_date(self.source.date)

    def get_absolute_url(self):
        if self.source.__class__.__name__ == 'Handover':
            source_type = 'handover'
        else:
            source_type = 'purchase'
        return '/inventory/entry-report/' + source_type + '/' + str(self.source.id)

    def __str__(self):
        return unicode(self.entry_report_no)


class EntryReportRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    rate = models.FloatField()
    vattable = models.BooleanField(default=True)
    other_expenses = models.FloatField(default=0)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    entry_report = models.ForeignKey(EntryReport, related_name='rows', blank=True, null=True)
    journal = GenericRelation(JournalEntry, related_query_name='journal', content_type_field="content_type",
                              object_id_field='model_id')

    def total_entry_cost(self):
        cost = self.rate * self.quantity
        if self.vattable:
            cost *= 1.13
        return cost + self.other_expenses

    def get_voucher_no(self):
        if self.entry_report:
            return self.entry_report.entry_report_no
        else:
            return 'Opening Balance'


class Handover(models.Model):
    voucher_no = models.PositiveIntegerField(blank=True, null=True)
    addressee = models.CharField(max_length=254)
    date = BSDateField(default=today, validators=[validate_in_fy])
    office = models.CharField(max_length=254)
    designation = models.CharField(max_length=254)
    handed_to = models.CharField(max_length=254)
    due_days = models.PositiveIntegerField(default=7)
    types = [('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')]
    type = models.CharField(max_length=9, choices=types, default='Incoming')
    entry_reports = GenericRelation(EntryReport, content_type_field='source_content_type_id',
                                    object_id_field='source_object_id')

    @property
    def fiscal_year(self):
        return FiscalYear.from_date(self.date)

    def get_entry_report(self):
        entry_reports = self.entry_reports.all()
        if len(entry_reports):
            return entry_reports[0]
        return None

    def get_absolute_url(self):
        return reverse('update_handover', kwargs={'id': self.id})

    def __unicode__(self):
        return _('Handover') + ' (' + str(self.voucher_no) + ')'


class HandoverRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    total_amount = models.FloatField()
    received_date = models.DateField(null=True, blank=True)
    condition = models.TextField(null=True, blank=True)
    handover = models.ForeignKey(Handover, related_name='rows')

    @property
    def rate(self):
        return self.total_amount / self.quantity

    def total_entry_cost(self):
        if self.handover.type == 'Incoming':
            return self.total_amount

    @property
    def release_quantity(self):
        if self.handover.type == 'Outgoing':
            return self.total_amount

    def get_voucher_no(self):
        return self.handover.voucher_no


class UnsavedForeignKey(models.ForeignKey):
    # A ForeignKey which can point to an unsaved object
    allow_unsaved_instance_assignment = True


class PurchaseOrder(models.Model):
    party = models.ForeignKey(Party)
    order_no = models.IntegerField(blank=True, null=True)
    date = BSDateField(default=today, validators=[validate_in_fy])
    due_days = models.IntegerField(default=3)
    entry_reports = GenericRelation(EntryReport, content_type_field='source_content_type_id',
                                    object_id_field='source_object_id')

    @property
    def fiscal_year(self):
        return FiscalYear.from_date(self.date)

    def get_entry_report(self):
        entry_reports = self.entry_reports.all()
        if len(entry_reports):
            return entry_reports[0]
        return None

    def get_absolute_url(self):
        return reverse('update_purchase_order', kwargs={'id': self.id})

    def get_voucher_no(self):
        return self.order_no

    def __unicode__(self):
        return _('Purchase Order') + ' (' + str(self.order_no) + ')'


class PurchaseOrderRow(models.Model):
    sn = models.PositiveIntegerField()
    budget_title_no = models.IntegerField(blank=True, null=True)
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    rate = models.FloatField()
    vattable = models.BooleanField(default=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    purchase_order = UnsavedForeignKey(PurchaseOrder, related_name='rows')


class InventoryAccountRow(models.Model):
    country_of_production_or_company_name = models.CharField(max_length=254, blank=True, null=True)
    size = models.CharField(max_length=254, blank=True, null=True)
    expected_life = models.CharField(max_length=254, blank=True, null=True)
    source = models.CharField(max_length=254, blank=True, null=True)
    expense_total_cost_price = models.FloatField(blank=True, null=True)
    remaining_total_cost_price = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    # inventory_account = models.ForeignKey(InventoryAccount, related_name='rows')
    journal_entry = models.OneToOneField(JournalEntry, related_name='account_row')

    @property
    def expense_total(self):
        if self.expense_total_cost_price:
            return self.expense_total_cost_price
        total = 0
        if self.journal_entry.creator.__class__.__name__ == 'DemandRow':
            try:
                for release in self.journal_entry.creator.releases.all():
                    total += release.item_instance.rate
                return total
            except Exception as e:
                import ipdb

                ipdb.set_trace()
        return 0

    def __str__(self):
        return str(self.journal_entry)


@receiver(pre_delete, sender=EntryReportRow)
def _entry_report_row_delete(sender, instance, **kwargs):
    entry = JournalEntry.get_for(instance)
    if entry:
        entry.delete()


@receiver(pre_delete, sender=DemandRow)
def _demand_form_row_delete(sender, instance, **kwargs):
    entry = JournalEntry.get_for(instance)
    if entry:
        entry.delete()


@receiver(pre_delete, sender=Transaction)
def _transaction_delete(sender, instance, **kwargs):
    transaction = instance
    # cancel out existing dr_amount and cr_amount from account's current_dr and current_cr
    if transaction.dr_amount:
        transaction.account.current_balance -= transaction.dr_amount

    if transaction.cr_amount:
        transaction.account.current_balance += transaction.cr_amount

    # alter(transaction.account, transaction.journal_entry.date, float(zero_for_none(transaction.dr_amount)) * -1,
    #       float(zero_for_none(transaction.cr_amount)) * -1)

    transaction.account.save()


class Inspection(models.Model):
    report_no = models.IntegerField()
    date = BSDateField(default=today, validators=[validate_in_fy])
    # transaction = models.ForeignKey(Transaction, related_name='inspection')

    @property
    def fiscal_year(self):
        return FiscalYear.from_date(self.date)

    def __str__(self):
        return unicode(self.report_no)


class InspectionRow(models.Model):
    sn = models.PositiveIntegerField()
    account_no = models.PositiveIntegerField()
    property_classification_reference_number = models.CharField(max_length=20, blank=True, null=True)
    item_name = models.CharField(max_length=254)
    unit = models.CharField(max_length=50, default=_('pieces'))
    quantity = models.FloatField()
    rate = models.FloatField()
    price = models.FloatField(blank=True, null=True)
    matched_number = models.PositiveIntegerField(blank=True, null=True)
    unmatched_number = models.PositiveIntegerField(blank=True, null=True)
    decrement = models.PositiveIntegerField(blank=True, null=True)
    increment = models.PositiveIntegerField(blank=True, null=True)
    decrement_increment_price = models.FloatField(blank=True, null=True)
    good = models.PositiveIntegerField(blank=True, null=True)
    bad = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    inspection = models.ForeignKey(Inspection, related_name='rows')

    def __str__(self):
        return unicode(self.item_name)


class YearlyReport(models.Model):
    fiscal_year = models.OneToOneField(FiscalYear)


class YearlyReportRow(models.Model):
    sn = models.PositiveIntegerField()
    account_no = models.PositiveIntegerField()
    property_classification_reference_number = models.CharField(max_length=20, blank=True, null=True)
    item_name = models.CharField(max_length=254)
    income = models.FloatField()
    expense = models.FloatField()
    remaining = models.FloatField(blank=True, null=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    yearly_report = models.ForeignKey(YearlyReport, related_name='rows')


class QuotationComparison(models.Model):
    report_no = models.IntegerField()
    date = BSDateField(default=today, validators=[validate_in_fy], blank=True, null=True)

    @property
    def fiscal_year(self):
        return FiscalYear.from_date(self.date)


class QuotationComparisonRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item, related_name='item_quotation')
    specification = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.FloatField()
    estimated_cost = models.FloatField()
    quotation = models.ForeignKey(QuotationComparison, related_name='rows')
    # party = models.ForeignKey(PartyQuotation, related_name='bidder_quote')


class PartyQuotation(models.Model):
    party = models.ForeignKey(Party, related_name='party_quote')
    per_unit_price = models.FloatField()
    quotation_comparison_row = models.ForeignKey(QuotationComparisonRow, related_name='bidder_quote', blank=True, null=True)


class ItemInstance(models.Model):
    item = models.ForeignKey(Item, related_name='instances')
    item_rate = models.FloatField(null=True)
    location = models.ForeignKey(ItemLocation, null=True)
    other_properties = JSONField(null=True, blank=True)
    source = models.ForeignKey(EntryReportRow, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def transfer(self, to_location, to_user):
        if type(to_location) == unicode or type(to_location) == str:
            to_location = ItemLocation.objects.get(name=to_location)
        history = InstanceHistory.objects.create(instance=self, from_location=self.location, to_location=to_location,
                                                 from_user=self.user,
                                                 to_user=to_user)
        return history

    def undo_transfer(self):
        history = InstanceHistory.objects.filter(instance=self, to_location=self.location, to_user=self.user).order_by(
            '-id').last()
        self.user = history.from_user
        self.location = history.from_location
        self.save()
        history.delete()
        return self

    @property
    def rate(self):
        return self.item_rate

    def __unicode__(self):
        return unicode(self.item) + u' at ' + unicode(self.location)


class InstanceHistory(models.Model):
    instance = models.ForeignKey(ItemInstance)
    date = BSDateField(default=today, validators=[validate_in_fy], verbose_name=_('Date'))
    from_location = models.ForeignKey(ItemLocation, related_name='from_history', verbose_name=_('From Location'), null=True)
    to_location = models.ForeignKey(ItemLocation, related_name='to_history', null=True, blank=True, verbose_name=_('To Location'))
    from_user = models.ForeignKey(User, related_name='from_history', null=True, blank=True, verbose_name=_('From User'))
    to_user = models.ForeignKey(User, related_name='to_history', null=True, blank=True, verbose_name=_('To User'))

    def save(self, *args, **kwargs):
        ret = super(InstanceHistory, self).save(*args, **kwargs)
        self.instance.location_id = self.to_location_id
        self.instance.user_id = self.to_user_id
        self.instance.save()
        return ret

    def __str__(self):
        return str(self.instance)

    class Meta:
        verbose_name_plural = _('Instance History')


class Release(models.Model):
    demand_row = models.ForeignKey(DemandRow, related_name='releases')
    item_instance = models.ForeignKey(ItemInstance)
    location = models.ForeignKey(ItemLocation)

    def __unicode__(self):
        return unicode(self.item_instance)


class Expense(models.Model):
    voucher_no = models.PositiveIntegerField(verbose_name=_('Voucher No.'))
    date = BSDateField(default=today, validators=[validate_in_fy], verbose_name=_('Date'))
    instance = models.ForeignKey(ItemInstance)
    types = (('Waive', _('Waive')), ('Handover', _('Handover')), ('Auction', _('Auction')))
    type = models.CharField(choices=types, max_length=20, default='Waive', verbose_name=_('Type'))
    rate = models.FloatField(blank=True, null=True, verbose_name=_('Rate'))

    @property
    def fiscal_year(self):
        return FiscalYear.from_date(self.date)

    def get_next_voucher_no(self):
        if not self.pk and not self.voucher_no:
            return get_next_voucher_no(Expense, 'voucher_no')

    def __init__(self, *args, **kwargs):
        super(Expense, self).__init__(*args, **kwargs)

        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(Expense, 'voucher_no')

    def save(self, *args, **kwargs):
        created = False
        if not self.id:
            created = True
        super(Expense, self).save(*args, **kwargs)
        if created:
            self.instance.transfer(None, None)
            set_transactions(self, self.date,
                             ['cr', self.instance.item.account, 1])

    def __unicode__(self):
        ret = _('Expense')
        if self.pk:
            ret += ': ' + str(self.voucher_no)
        return unicode(ret)


def fiscal_year_changed(sender, **kwargs):
    # old_fiscal_year = kwargs.get('old_fiscal_year')
    # year_end = FiscalYear.end(old_fiscal_year.year)
    pass

# fiscal_year_signal.connect(fiscal_year_changed)
