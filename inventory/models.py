# -*- coding: utf-8 -*-

from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db.models import F
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext as _

from app.utils.helpers import zero_for_none, none_for_zero
from app.utils.translation import ne2en
from users.models import User
from core.models import FiscalYear, Party
from app.utils.translation import BSDateField



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

    def __str__(self):
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


class Item(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    account = models.OneToOneField(InventoryAccount, related_name='item', null=True)
    type_choices = [('consumable', _('Consumable')), ('non-consumable', _('Non-Consumable'))]
    type = models.CharField(choices=type_choices, max_length=15, default='consumable')
    unit = models.CharField(max_length=50, default=_('pieces'))
    # vattable = models.BooleanField(default=True)
    property_classification_reference_number = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        account_no = kwargs.pop('account_no')
        opening_balance = kwargs.pop('opening_balance')
        if account_no:
            if self.account:
                account = self.account
                account.account_no = account_no
            else:
                account = InventoryAccount(code=self.code, name=self.name, account_no=account_no,
                                           opening_balance=opening_balance, current_balance=opening_balance)
            account.save()
            self.account = account
        super(Item, self).save(*args, **kwargs)

    def add_category(self, category):
        category_instance, created = Category.objects.get_or_create(name=category)
        self.categories.add(category_instance)

    def __unicode__(self):
        return self.name


class JournalEntry(models.Model):
    date = BSDateField()
    content_type = models.ForeignKey(ContentType, related_name='inventory_journal_entries')
    model_id = models.PositiveIntegerField()
    creator = generic.GenericForeignKey('content_type', 'model_id')
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
        obj_transaction = Transaction.objects.filter(account__name=self.account.name, cr_amount=None)
        total = 0
        for o in obj_transaction:
            total += o.dr_amount
        return total

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
        else:
            raise Exception('Transactions can only be either "dr" or "cr".')
        transaction.account = arg[1]
        transaction.account.current_balance += diff
        transaction.current_balance = transaction.account.current_balance
        transaction.account.save()
        journal_entry.transactions.add(transaction)
        alter(transaction.account, date, diff)


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
    release_no = models.IntegerField(blank=True, null=True)
    fiscal_year = models.ForeignKey(FiscalYear)
    demandee = models.ForeignKey(User)
    date = BSDateField()
    purpose = models.CharField(max_length=254)

    def get_voucher_no(self):
        return self.release_no

    def __init__(self, *args, **kwargs):
        super(Demand, self).__init__(*args, **kwargs)
        if not self.pk and not self.release_no:
            self.release_no = get_next_voucher_no(Demand, 'release_no')


class DemandRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    release_quantity = models.FloatField(null=True, blank=True)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    demand = models.ForeignKey(Demand, related_name='rows')
    statuses = [('Requested', 'Requested'), ('Approved', 'Approved'), ('Fulfilled', 'Fulfilled')]
    status = models.CharField(max_length=9, choices=statuses, default='Requested')

    def save(self, *args, **kwargs):
        self.quantity = ne2en(self.quantity)
        self.release_quantity = ne2en(self.release_quantity)
        super(DemandRow, self).save(*args, **kwargs)

    def get_voucher_no(self):
        return self.demand.release_no


class EntryReport(models.Model):
    entry_report_no = models.PositiveIntegerField(blank=True, null=True)
    fiscal_year = models.ForeignKey(FiscalYear)
    source_content_type = models.ForeignKey(ContentType)
    source_object_id = models.PositiveIntegerField()
    source = generic.GenericForeignKey('source_content_type', 'source_object_id')

    def get_absolute_url(self):
        if self.source.__class__.__name__ == 'Handover':
            source_type = 'handover'
        else:
            source_type = 'purchase'
        return '/inventory/entry-report/' + source_type + '/' + str(self.source.id)


class EntryReportRow(models.Model):
    sn = models.PositiveIntegerField()
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    rate = models.FloatField()
    other_expenses = models.FloatField(default=0)
    remarks = models.CharField(max_length=254, blank=True, null=True)
    entry_report = models.ForeignKey(EntryReport, related_name='rows')

    def total_entry_cost(self):
        return self.rate * self.quantity * 1.13 + self.other_expenses

    def get_voucher_no(self):
        return self.entry_report.entry_report_no


class Handover(models.Model):
    voucher_no = models.PositiveIntegerField(blank=True, null=True)
    addressee = models.CharField(max_length=254)
    date = BSDateField()
    office = models.CharField(max_length=254)
    designation = models.CharField(max_length=254)
    handed_to = models.CharField(max_length=254)
    due_days = models.PositiveIntegerField(default=7)
    fiscal_year = models.ForeignKey(FiscalYear)
    types = [('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')]
    type = models.CharField(max_length=9, choices=types, default='Incoming')
    entry_reports = generic.GenericRelation(EntryReport, content_type_field='source_content_type_id',
                                            object_id_field='source_object_id')

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


class PurchaseOrder(models.Model):
    party = models.ForeignKey(Party)
    order_no = models.IntegerField(blank=True, null=True)
    date = BSDateField()
    due_days = models.IntegerField(default=3)
    fiscal_year = models.ForeignKey(FiscalYear)
    entry_reports = generic.GenericRelation(EntryReport, content_type_field='source_content_type_id',
                                            object_id_field='source_object_id')

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
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='rows')


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
    release_no = models.IntegerField(blank=True, null=True)
    fiscal_year = models.ForeignKey(FiscalYear)


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


class YearlyReport(models.Model):
    release_no = models.IntegerField(blank=True, null=True)
    fiscal_year = models.ForeignKey(FiscalYear)


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


    