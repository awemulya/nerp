from django.db import models
from njango.fields import BSDateField, today

from core.models import Currency, FiscalYear, validate_in_fy, Donor, Account

IMPREST_TRANSACTION_TYPES = (('initial_deposit', 'Initial Deposit'), ('gon_fund_transfer', 'GON Fund Transfer'),
                             ('replenishment_received', 'Replenishment Received'),
                             ('payment', 'Payment'), ('liquidation', 'Liquidation'))

AID_TYPES = (('loan', 'Loan'), ('grant', 'Grant'))


class Project(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def get_imprest(self, fy=None):
        if not fy:
            fy = FiscalYear.get()
        elif type(fy) in [int, str]:
            fy = FiscalYear.get(fy)
        imprest, created = ImprestLedger.objects.get_or_create(project=self, fy=fy)
        return imprest

    def get_imprest_ledger(self, fy=None):
        return self.get_imprest(fy).ledger

    def __str__(self):
        return self.name


class Aid(models.Model):
    donor = models.ForeignKey(Donor)
    type = models.CharField(choices=AID_TYPES, max_length=10)
    key = models.CharField(max_length=50)
    project = models.ForeignKey(Project)

    def __str__(self):
        return str(self.donor) + ' ' + str(self.get_type_display()) + ' ' + self.key


class Signatory(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    default = models.BooleanField(default=False, verbose_name='Required to sign on all notes?')
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.name


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
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.name or self.get_type_display()


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    gon_funded = models.BooleanField(default=False, verbose_name='GON Funded?')
    order = models.PositiveIntegerField(default=0)
    project = models.ForeignKey(Project)

    def __str__(self):
        st = self.name
        if self.code:
            st = st + ' - ' + self.code
        return st

    def get_absolute_url(self):
        #     TODO after CRUD
        return '# TODO'

    class Meta(object):
        ordering = ('order',)
        verbose_name_plural = 'Expense Categories'


class Expense(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    category = models.ManyToManyField(ExpenseCategory, blank=True)
    enabled = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    project = models.ForeignKey(Project)

    def __str__(self):
        st = self.name
        if self.code:
            st = st + ' - ' + self.code
        return st

    class Meta(object):
        ordering = ('order',)


class ExpenseRow(models.Model):
    category = models.ForeignKey(ExpenseCategory)
    expense = models.ForeignKey(Expense)
    amount = models.FloatField()
    fy = models.ForeignKey(FiscalYear)
    project = models.ForeignKey(Project)

    def __str__(self):
        return str(self.fy) + '-' + str(self.category) + ' - ' + str(self.expense) + ' : ' + str(self.amount)


class ImprestLedger(models.Model):
    ledger = models.ForeignKey(Account)
    project = models.ForeignKey(Project)
    fy = models.ForeignKey(FiscalYear)

    def __str__(self):
        return 'Imprest: ' + str(self.project) + ' - ' + str(self.fy)

    class Meta:
        unique_together = ('project', 'fy')
