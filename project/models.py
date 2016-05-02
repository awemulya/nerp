from django.db import models

from core.models import Currency, FiscalYear

IMPREST_TRANSACTION_TYPES = (('initial_deposit', 'Initial Deposit'), ('gon_fund_transfer', 'GON Fund Transfer'),
                             ('replenishment_received', 'Replenishment Received'),
                             ('payment', 'Payment'), ('liquidation', 'Liquidation'))


class ImprestTransaction(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, choices=IMPREST_TRANSACTION_TYPES)
    date = models.DateField(null=True, blank=True)
    wa_no = models.CharField(max_length=10, verbose_name='Withdrawal Application No.', null=True, blank=True)
    ref = models.CharField(max_length=10, verbose_name='Reference', null=True, blank=True)
    amount = models.FloatField()
    currency = models.ForeignKey(Currency)
    description = models.TextField(null=True, blank=True)
    exchange_rate = models.FloatField(null=True, blank=True)
    fy = models.ForeignKey(FiscalYear)

    def __str__(self):
        return self.name
