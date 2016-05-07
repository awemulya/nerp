from django.db import models
from njango.fields import BSDateField, today

from core.models import Currency, FiscalYear, validate_in_fy

IMPREST_TRANSACTION_TYPES = (('initial_deposit', 'Initial Deposit'), ('gon_fund_transfer', 'GON Fund Transfer'),
                             ('replenishment_received', 'Replenishment Received'),
                             ('payment', 'Payment'), ('liquidation', 'Liquidation'))


class ImprestTransaction(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, choices=IMPREST_TRANSACTION_TYPES)
    date = BSDateField(null=True, blank=True, default=today, validators=[validate_in_fy])
    date_of_payment = BSDateField(null=True, blank=True, default=today, validators=[validate_in_fy])
    wa_no = models.CharField(max_length=10, verbose_name='Withdrawal Application No.', null=True, blank=True)
    # ref = models.CharField(max_length=10, verbose_name='Reference', null=True, blank=True)
    amount_nrs = models.FloatField(blank=True, null=True)
    amount_usd = models.FloatField(blank=True, null=True)
    # currency = models.ForeignKey(Currency)
    # description = models.TextField(null=True, blank=True)
    exchange_rate = models.FloatField(null=True, blank=True)
    fy = models.ForeignKey(FiscalYear)

    def __str__(self):
        return self.name or self.get_type_display()


class ExpenditureCategory(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        st = self.name
        if self.code:
            st = st + ' - ' + self.code
        return st

    class Meta(object):
        ordering = ('order',)


class Expenditure(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    category = models.ManyToManyField(ExpenditureCategory, blank=True)

    def __str__(self):
        st = self.name
        if self.code:
            st = st + ' - ' + self.code
        return st
