from django.db import models
from app.utils.translation import transl
import dbsettings

FISCAL_YEARS = (
    (2069, "2069/70"),
    (2070, "2070/71"),
    (2071, "2071/72")
)

SOURCES = [('nepal_government', 'Nepal Government'), ('foreign_cash_grant', 'Foreign Cash Grant'),
           ('foreign_compensating_grant', 'Foreign Compensating Grant'), ('foreign_cash_loan', 'Foreign Cash Loan'),
           ('foreign_compensating_loan', 'Foreign Compensating Loan'),
           ('foreign_substantial_aid', 'Foreign Substantial Aid')]


class AppSetting(dbsettings.Group):
    site_name = dbsettings.StringValue(default='NERP')
    fiscal_year = dbsettings.StringValue(choices=FISCAL_YEARS)
    header_for_forms = dbsettings.TextValue()


app_setting = AppSetting()


class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' (' + self.code + ')'


class Account(models.Model):
    name = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.CharField(max_length=254, blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    pan_no = models.CharField(max_length=50, blank=True, null=True)
    account = models.OneToOneField(Account, related_name='party')

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(name_en=self.name_en, name_ne=self.name_ne)
            account.save()
            self.account = account
        super(Party, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Parties'


class FiscalYear(models.Model):
    year = models.IntegerField(choices=FISCAL_YEARS, unique=True)

    def __unicode__(self):
        return str(self.year) + '/' + str(self.year - 1999)


class Employee(models.Model):
    name = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(name_en=self.name_en, name_ne=self.name_ne)
            account.save()
            self.account = account
        super(Employee, self).save(*args, **kwargs)


class Donor(models.Model):
    name = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=254)
    no = models.PositiveIntegerField()

    def __unicode__(self):
        return str(self.no) + ' - ' + self.name

    class Meta:
        verbose_name_plural = 'Activities'


class BudgetHead(models.Model):
    name = models.CharField(max_length=254)
    no = models.PositiveIntegerField()

    def get_current_balance(self):
        return BudgetBalance.objects.get(fiscal_year=AppSetting.objects.first(), budget_head=self)

    current_balance = property(get_current_balance)

    def __unicode__(self):
        return transl(self.no) + ' - ' + self.name


class BudgetBalance(models.Model):
    budget_head = models.ForeignKey(BudgetHead, related_name='balance')
    fiscal_year = models.ForeignKey(FiscalYear)
    nepal_government = models.FloatField(default=0)
    foreign_cash_grant = models.FloatField(default=0)
    foreign_compensating_grant = models.FloatField(default=0)
    foreign_cash_loan = models.FloatField(default=0)
    foreign_compensating_loan = models.FloatField(default=0)
    foreign_substantial_aid = models.FloatField(default=0)
    nepal_government_due = models.FloatField(default=0, editable=False)
    foreign_cash_grant_due = models.FloatField(default=0, editable=False)
    foreign_compensating_grant_due = models.FloatField(default=0, editable=False)
    foreign_cash_loan_due = models.FloatField(default=0, editable=False)
    foreign_compensating_loan_due = models.FloatField(default=0, editable=False)
    foreign_substantial_aid_due = models.FloatField(default=0, editable=False)

    def total(self):
        return self.nepal_government + self.foreign_cash_grant + self.foreign_compensating_grant + self.foreign_cash_loan + self.foreign_compensating_loan + self.foreign_substantial_aid

    def __unicode__(self):
        return self.budget_head.name + ' - ' + str(self.fiscal_year)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.nepal_government_due = self.nepal_government
            self.foreign_cash_grant_due = self.foreign_cash_grant
            self.foreign_compensating_grant_due = self.foreign_compensating_grant
            self.foreign_cash_loan_due = self.foreign_cash_loan
            self.foreign_compensating_loan_due = self.foreign_compensating_loan
            self.foreign_substantial_aid_due = self.foreign_substantial_aid
        super(BudgetBalance, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['budget_head', 'fiscal_year']


class TaxScheme(models.Model):
    name = models.CharField(max_length=254)
    percent = models.FloatField()

    def get_multiplier(self):
        return self.percent / 100

    multiplier = property(get_multiplier)

    def __unicode__(self):
        return self.name + ' (' + str(self.percent) + '%)'