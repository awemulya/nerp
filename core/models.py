from django.core.exceptions import ValidationError
from django.db import models
from njango.models import TranslatableNumberModel
from njango.nepdate import bs, bs2ad, tuple_from_string
from njango.utils import get_calendar
from django.utils.translation import ugettext_lazy as _
from users.templatetags.filters import localize

FISCAL_YEARS = (
    (2069, "2069/70"),
    (2070, "2070/71"),
    (2071, "2071/72"),
    (2072, "2072/73"),
)

SOURCES = [('nepal_government', 'Nepal Government'), ('foreign_cash_grant', 'Foreign Cash Grant'),
           ('foreign_compensating_grant', 'Foreign Compensating Grant'), ('foreign_cash_loan', 'Foreign Cash Loan'),
           ('foreign_compensating_loan', 'Foreign Compensating Loan'),
           ('foreign_substantial_aid', 'Foreign Substantial Aid')]


class FiscalYear(models.Model):
    year = models.IntegerField(choices=FISCAL_YEARS, unique=True)

    @staticmethod
    def from_date(date):
        month = int(date.split('-')[1])
        year = int(date.split('-')[0])
        if month < 4:
            year -= 1
        return FiscalYear.get(year)

    @staticmethod
    def get(year=None):
        if not year:
            year = app_setting.fiscal_year
        return FiscalYear.objects.get(year=year)

    @staticmethod
    def start(year=None):
        if not year:
            year = app_setting.fiscal_year
        fiscal_year_start = str(year) + '-04-01'
        tuple_value = tuple_from_string(fiscal_year_start)
        calendar = get_calendar()
        if calendar == 'ad':
            tuple_value = bs2ad(tuple_value)
        return tuple_value

    @staticmethod
    def end(year=None):
        if not year:
            year = app_setting.fiscal_year
        fiscal_year_end = str(int(year) + 1) + '-03-' + str(bs[int(year) + 1][2])
        tuple_value = tuple_from_string(fiscal_year_end)
        calendar = get_calendar()
        if calendar == 'ad':
            tuple_value = bs2ad(tuple_value)
        return tuple_value

    def __unicode__(self):
        return str(self.year) + '/' + str(self.year - 1999)


class FYManager(models.Manager):
    def fiscal_year(self, year=None):
        if year:
            original_fiscal_year = app_setting.fiscal_year
            app_setting.fiscal_year = year  # bypasses validation
            lookup_year = year
        else:
            lookup_year = app_setting.fiscal_year
        # import ipdb
        # ipdb.set_trace()
        result = super(FYManager, self).get_queryset().filter(date__gte=FiscalYear.start(lookup_year),
                                                              date__lte=FiscalYear.end(lookup_year))
        # return super(FYManager, self).get_queryset().filter(Q(date__year__range=(FiscalYear.start(year)[0], FiscalYear.end(year)[0])))
        if year:
            app_setting.fiscal_year = original_fiscal_year
        return result


import dbsettings


class AppSetting(dbsettings.Group):
    site_name = dbsettings.StringValue(default='NERP')
    # fiscal_year = dbsettings.MultipleChoiceValue(choices=[('13+', '13-19'), ('19+', '19-25'), ('25+', '25-40')])
    fiscal_year = dbsettings.StringValue(
        choices=FISCAL_YEARS)
    header_for_forms = dbsettings.TextValue()


app_setting = AppSetting()


class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name + ' (' + self.code + ')'

        # def save(self, *args, **kwargs):
        #     if len(self.code) is not 0 and len(self.name) is 0:
        #         self.name = 'default'
        #     elif len(self.code) is 0 and len(self.name) is not 0:
        #         self.code = 'default'
        #     super(Language, self).save(*args, **kwargs)


class Account(models.Model):
    name = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name


class Party(models.Model):
    name = models.CharField(max_length=254, verbose_name=_('Name'))
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
        verbose_name_plural = _('Parties')


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
        verbose_name_plural = _('Activities')


class BudgetHead(TranslatableNumberModel):
    name = models.CharField(max_length=254)
    no = models.PositiveIntegerField()
    _translatable_number_fields = ('no',)

    def get_current_balance(self):
        return BudgetBalance.objects.get(fiscal_year=FiscalYear.get(app_setting.fiscal_year), budget_head=self)

    current_balance = property(get_current_balance)

    def __unicode__(self):
        return self.no + ' - ' + self.name


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


def validate_in_fy(value):
    fiscal_year = app_setting.fiscal_year
    fiscal_year_start = fiscal_year + '-04-01'
    fiscal_year_end = str(int(fiscal_year) + 1) + '-03-' + str(bs[int(fiscal_year) + 1][2])
    calendar = get_calendar()
    if calendar == 'bs':
        value_tuple = bs2ad(value)
    else:
        if type(value) == tuple:
            value_tuple = value
        else:
            value_tuple = tuple_from_string(value)
    if not bs2ad(fiscal_year_start) <= value_tuple <= bs2ad(fiscal_year_end):
        raise ValidationError('%s %s' % (localize(value), _('is not in current fiscal year.')))
