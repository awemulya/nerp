# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db.models import F
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext as _

from app.libr import zero_for_none, none_for_zero, digitize
from users.models import User


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u' Inventory Categories'


class InventoryAccount(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    opening_balance = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/inventory_account/' + str(self.id)

    def get_category(self):
        try:
            item = self.item
        except:
            return None
        try:
            category = self.item.category
        except:
            return None
        return category


    def add_category(self, category):
        category_instance, created = Category.objects.get_or_create(name=category)
        self.category = category_instance

    def get_all_categories(self):
        return self.category.get_ancestors(include_self=True)

    categories = property(get_all_categories)

    def get_cr_amount(self, day):
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_cr
        return 0

    def get_dr_amount(self, day):
        #journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_dr
        return 0


class Item(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    purchase_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    account = models.OneToOneField(InventoryAccount, related_name='item')
    type_choices = [('consumable', 'Consumable'), ('non-consumable', 'Non Consumable')]
    type = models.CharField(choices=type_choices, max_length=15, default='consumable')
    unit = models.CharField(max_length=50, default=_('pieces'))
    vattable = models.BooleanField(default=True)
    country_of_production = models.CharField(max_length=50, default=_('Nepal'), blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    expected_life = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    property_identification_reference_number = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = InventoryAccount(code=self.code, name=self.name)
            account.save()
            self.account = account
        super(Item, self).save(*args, **kwargs)

    def add_category(self, category):
        category_instance, created = Category.objects.get_or_create(name=category)
        self.categories.add(category_instance)

    def __unicode__(self):
        return '[' + self.code + '] ' + self.name


class JournalEntry(models.Model):
    date = models.DateField()
    content_type = models.ForeignKey(ContentType, related_name='inventory_journal_entries')
    model_id = models.IntegerField()

    def __str__(self):
        return str(self.content_type) + ': ' + str(self.model_id) + ' [' + str(self.date) + ']'

    class Meta:
        verbose_name_plural = u'InventoryJournal Entries'


class Transaction(models.Model):
    account = models.ForeignKey(InventoryAccount)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    journal_entry = models.ForeignKey(JournalEntry, related_name='transactions')

    # def get_balance(self):
    #     return zero_for_none(self.current_dr) - zero_for_none(self.current_cr)

    def __str__(self):
        return str(self.account) + ' [' + str(self.dr_amount) + ' / ' + str(self.cr_amount) + ']'


def alter(account, date, dr_difference, cr_difference):
    Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_dr=none_for_zero(zero_for_none(F('current_dr')) + zero_for_none(dr_difference)),
        current_cr=none_for_zero(zero_for_none(F('current_cr')) + zero_for_none(cr_difference)))


def set_transactions(submodel, date, *args):
    # [transaction.delete() for transaction in submodel.transactions.all()]
    # args = [arg for arg in args if arg is not None]
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(submodel), model_id=submodel.id,
        defaults={
            'date': date
        })
    for arg in args:
        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
        matches = journal_entry.transactions.filter(account=arg[1])
        if not matches:
            transaction = Transaction()
            transaction.account = arg[1]
            if arg[0] == 'dr':
                transaction.dr_amount = float(arg[2])
                transaction.cr_amount = None
                transaction.account.current_dr = none_for_zero(
                    zero_for_none(transaction.account.current_dr) + transaction.dr_amount)
                alter(arg[1], date, float(arg[2]), 0)
            if arg[0] == 'cr':
                transaction.cr_amount = float(arg[2])
                transaction.dr_amount = None
                transaction.account.current_cr = none_for_zero(
                    zero_for_none(transaction.account.current_cr) + transaction.cr_amount)
                alter(arg[1], date, 0, float(arg[2]))
            transaction.current_dr = none_for_zero(
                zero_for_none(transaction.account.get_dr_amount(date + timedelta(days=1)))
                + zero_for_none(transaction.dr_amount))
            transaction.current_cr = none_for_zero(
                zero_for_none(transaction.account.get_cr_amount(date + timedelta(days=1)))
                + zero_for_none(transaction.cr_amount))
        else:
            transaction = matches[0]
            transaction.account = arg[1]

            # cancel out existing dr_amount and cr_amount from current_dr and current_cr
            # if transaction.dr_amount:
            #     transaction.current_dr -= transaction.dr_amount
            #     transaction.account.current_dr -= transaction.dr_amount
            #
            # if transaction.cr_amount:
            #     transaction.current_cr -= transaction.cr_amount
            #     transaction.account.current_cr -= transaction.cr_amount

            # save new dr_amount and add it to current_dr/cr
            if arg[0] == 'dr':
                dr_difference = float(arg[2]) - zero_for_none(transaction.dr_amount)
                cr_difference = zero_for_none(transaction.cr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.dr_amount = float(arg[2])
                transaction.cr_amount = None
            else:
                cr_difference = float(arg[2]) - zero_for_none(transaction.cr_amount)
                dr_difference = zero_for_none(transaction.dr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.cr_amount = float(arg[2])
                transaction.dr_amount = None

            transaction.current_dr = none_for_zero(zero_for_none(transaction.current_dr) + dr_difference)
            transaction.current_cr = none_for_zero(zero_for_none(transaction.current_cr) + cr_difference)
            transaction.account.current_dr = none_for_zero(
                zero_for_none(transaction.account.current_dr) + dr_difference)
            transaction.account.current_cr = none_for_zero(
                zero_for_none(transaction.account.current_cr) + cr_difference)

        #the following code lies outside if,else block, inside for loop
        transaction.account.save()
        journal_entry.transactions.add(transaction)


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
                                     model_id=instance.id).delete()
            instance.delete()


@receiver(pre_delete, sender=Transaction)
def _transaction_delete(sender, instance, **kwargs):
    transaction = instance
    print transaction
    # cancel out existing dr_amount and cr_amount from account's current_dr and current_cr
    if transaction.dr_amount:
        transaction.account.current_dr -= transaction.dr_amount

    if transaction.cr_amount:
        transaction.account.current_cr -= transaction.cr_amount

    print transaction.dr_amount
    alter(transaction.account, transaction.journal_entry.date, float(zero_for_none(transaction.dr_amount)) * -1,
          float(zero_for_none(transaction.cr_amount)) * -1)

    transaction.account.save()


class Demand(models.Model):
    release_no = models.IntegerField()
    fiscal_year = models.CharField(max_length=10)
    demandee = models.ForeignKey(User)
    date = models.DateField()
    purpose = models.CharField(max_length=254)


class DemandRow(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    release_quantity = models.FloatField()
    remarks = models.CharField(max_length=254, blank=True, null=True)
    demand = models.ForeignKey(Demand, related_name='rows')

    def save(self, *args, **kwargs):
        self.quantity = digitize(self.quantity)
        self.release_quantity = digitize(self.release_quantity)
        super(DemandRow, self).save(*args, **kwargs)


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.CharField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True)


class PurchaseOrder(models.Model):
    party = models.ForeignKey(Party)
    order_no = models.IntegerField()
    date = models.DateField()
    due_days = models.IntegerField(default=3)


class PurchaseOrderRow(models.Model):
    sn = models.IntegerField()
    budget_title_no = models.IntegerField()
    item = models.ForeignKey(Item)
    specification = models.CharField(max_length=254, blank=True, null=True)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    rate = models.FloatField()
    remarks = models.CharField(max_length=254, blank=True, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='rows')