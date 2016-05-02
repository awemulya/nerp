# import dbsettings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import User
# from core.models import validate_in_fy
from njango.fields import BSDateField, today
from njango.nepdate import bs2ad, bs
from django.core.validators import MaxValueValidator, MinValueValidator
from calendar import monthrange as mr
from datetime import date, datetime
from hr.bsdate import BSDate
from .helpers import get_y_m_tuple_list, are_side_months, zero_for_none, none_for_zero
# import pdb


from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import F
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# from core.models import FiscalYear
# from solo.models import SingletonModel
# from django.core.exceptions import ValidationError


# def validate_month(value):
#     if value < 1 and value > 12:
#         raise ValidationError(
#             _('%(value)s is not'),
#             params={'value': value},
#         )

# Account type name should be same as fieldname in employee account with small letter and underscope
# That is field name for 'BANK ACCOUNT' in employee model 
# will be 'bank_account'
acc_type = [('bank_account', _('Bank Account')),
            ('insurance_account', _('Insurance Account')),
            ('nalakosh_account', _('Nagarik Lagani Kosh Account')),
            ('sanchayakosh_account', _('Sanchayakosh Account'))]
deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
deduct_for = [('EMPLOYEE ACC', _('For employee Account')),
              ('EXPLICIT ACC', _('An Explicit Account'))]
payment_cycle = [('M', _('Monthly')),
                 ('Y', _('Yearly')),
                 ('D', _('Daily')),
                 ('H', _('Hourly'))]
holder_type = [('EMPLOYEE', _("Employee's Account")),
               ('COMPANY', _('Company Account'))]

# allowance
# When yearly than when to pay should be in setting


class Account(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    opening_dr = models.FloatField(default=0)
    opening_cr = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/ledger/' + str(self.id)

    # def get_last_day_last_transaction(self):
    #     transactions = Transaction.objects.filter(account=self, date__lt=date.today()).order_by('-id', '-date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0]
    #
    # def get_last_transaction_before(self, before_date):
    #     transactions = Transaction.objects.filter(account=self, date__lt=before_date).order_by('-id', '-date')[:1]
    #     if len(transactions) > 0:
    #         return transactions[0]
    #
    @property
    def balance(self):
        return self.get_balance()

    def get_balance(self):
        return zero_for_none(self.current_dr) - zero_for_none(self.current_cr)

    def get_day_opening_dr(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_dr
        return self.current_dr

    def get_day_opening_cr(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_cr
        return self.current_cr

    # def get_day_opening(self, before_date=None):
        if not before_date:
            before_date = datetime.date.today()
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return zero_for_none(transactions[0].current_dr) - zero_for_none(transactions[0].current_cr)
        return self.opening_dr - self.opening_cr

    # day_opening_dr = property(get_day_opening_dr)
    # day_opening_cr = property(get_day_opening_cr)
    #
    # day_opening = property(get_day_opening)

    def get_cr_amount(self, day):
        # journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_cr
        return 0

    def get_dr_amount(self, day):
        # journal_entry= JournalEntry.objects.filter(date__lt=day,transactions__account=self).order_by('-id','-date')[:1]
        transactions = Transaction.objects.filter(journal_entry__date__lt=day, account=self).order_by(
            '-journal_entry__id', '-journal_entry__date')[:1]
        if len(transactions) > 0:
            return transactions[0].current_dr
        return 0

    # no need
    def save(self, *args, **kwargs):
        queryset = Account.objects.all()
        original_name = self.name
        nxt = 2
        if not self.pk:
            while queryset.filter(**{'name': self.name}):
                self.name = original_name
                end = '%s%s' % ('-', nxt)
                if len(self.name) + len(end) > 100:
                    self.name = self.name[:100 - len(end)]
                self.name = '%s%s' % (self.name, end)
                nxt += 1
        return super(Account, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    # class Meta:
    #     unique_together = ('name', 'company')


class JournalEntry(models.Model):
    date = models.DateField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    source = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.content_type) + ': ' + str(self.object_id) + ' [' + str(self.date) + ']'

    class Meta:
        verbose_name_plural = u'Journal Entries'


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    journal_entry = models.ForeignKey(JournalEntry, null=True, related_name='transactions')

    def get_balance(self):
        return zero_for_none(self.current_dr) - zero_for_none(self.current_cr)

    def __str__(self):
        return str(self.account) + ' [' + str(self.dr_amount) + ' / ' + str(self.cr_amount) + ']'


def alter(account, date, dr_difference, cr_difference):
    Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_dr=none_for_zero(zero_for_none(F('current_dr')) + zero_for_none(dr_difference)),
        current_cr=none_for_zero(zero_for_none(F('current_cr')) + zero_for_none(cr_difference)))


def set_transactions(submodel, date, *args):
    if isinstance(date, unicode):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(submodel), object_id=submodel.id,
        defaults={
            'date': date
        })
    for arg in args:
        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
        if arg[1] == 'cash':
            arg[1] = Account.objects.get(name='Cash')
        matches = journal_entry.transactions.filter(account=arg[1])
        if not matches:
            transaction = Transaction()
            transaction.account = arg[1]
            if arg[0] == 'dr':
                transaction.dr_amount = float(zero_for_none(arg[2]))
                transaction.cr_amount = None
                transaction.account.current_dr = none_for_zero(
                    zero_for_none(transaction.account.current_dr) + transaction.dr_amount)
                alter(arg[1], date, float(arg[2]), 0)
            if arg[0] == 'cr':
                transaction.cr_amount = float(zero_for_none(arg[2]))
                transaction.dr_amount = None
                transaction.account.current_cr = none_for_zero(
                    zero_for_none(transaction.account.current_cr) + transaction.cr_amount)
                alter(arg[1], date, 0, float(arg[2]))
            transaction.current_dr = none_for_zero(
                zero_for_none(transaction.account.get_dr_amount(date + datetime.timedelta(days=1)))
                + zero_for_none(transaction.dr_amount))
            transaction.current_cr = none_for_zero(
                zero_for_none(transaction.account.get_cr_amount(date + datetime.timedelta(days=1)))
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

        # the following code lies outside if,else block, inside for loop
        transaction.account.save()
        try:
            journal_entry.transactions.add(transaction, bulk=False)
        except TypeError:  # for Django <1.9
            journal_entry.transactions.add(transaction)


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            try:
                JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
                                         model_id=instance.id).delete()
            except:
                pass
            instance.delete()


@receiver(pre_delete, sender=Transaction)
def _transaction_delete(sender, instance, **kwargs):
    transaction = instance
    # cancel out existing dr_amount and cr_amount from account's current_dr and current_cr
    if transaction.dr_amount:
        transaction.account.current_dr -= transaction.dr_amount

    if transaction.cr_amount:
        transaction.account.current_cr -= transaction.cr_amount

    alter(transaction.account, transaction.journal_entry.date, float(zero_for_none(transaction.dr_amount)) * -1,
          float(zero_for_none(transaction.cr_amount)) * -1)

    transaction.account.save()


class AccountType(models.Model):
    name = models.CharField(max_length=150, choices=acc_type, unique=True)
    description = models.CharField(max_length=250)
    permanent_multiply_rate = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


# class Account(models.Model):
#     # account_holder_type = models.CharField(choices=holder_type, max_length=50)
#     # account_type = models.ForeignKey(AccountType)
#     org_name = models.CharField(max_length=200)
#     branch = models.CharField(max_length=150)
#     acc_number = models.CharField(max_length=100)
#     description = models.CharField(max_length=256)

#     def __unicode__(self):
#         return '[%s][%s]' % (
#                                    # self.account_type,
#                                    self.org_name,
#                                    self.acc_number,
#                                    # self.account_holder_type
#                                    )


# class Transaction(models.Model):
#     account = models.ForeignKey(Account)
#     credit = models.FloatField()
#     debit = models.FloatField()
#     date_time = models.DateTimeField(default=timezone.now)
#     description = models.CharField(max_length=120)

#     def __unicode__(self):
#         return str(self.account.id)

# class InsuranceAccount(models.model):
#     org_name = models.CharField(max_length=200)
#     branch = models.CharField(max_length=150)
#     acc_number = models.CharField(max_length=100)

#     def __unicode__(self):
#         return self.org_name


# class NalaAccount(models.model):
#     # org_name = models.CharField(max_length=200)
#     branch = models.CharField(max_length=150)
#     acc_number = models.CharField(max_length=100)

#     def __unicode__(self):
#         return str(self.acc_number)


class EmployeeGrade(models.Model):
    grade_name = models.CharField(max_length=100)
    salary_scale = models.FloatField()
    # rate increases yearly with grade rate. Also shold mention when in setting? How much times
    grade_number = models.PositiveIntegerField()
    grade_rate = models.FloatField()
    parent_grade = models.ForeignKey('self', null=True, blank=True)
    # When employee is tecnician it should have no siblings
    is_technical = models.BooleanField(default=False)

    def __unicode__(self):
        if self.is_technical:
            return self.grade_name + '( Is Tecnician)'
        else:
            return self.grade_name


class Designation(models.Model):
    designation_name = models.CharField(max_length=100)
    grade = models.ForeignKey(EmployeeGrade)

    def __unicode__(self):
        return self.designation_name


# This is bhatta
class Allowance(models.Model):
    # deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
    name = models.CharField(max_length=100)
    employee_grade = models.ForeignKey(EmployeeGrade)
    # Any one out of two should be filled
    sum_type = models.CharField(max_length=50, choices=deduct_choice)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    # When to pay? ==> May be it should be in settingShould be in setting
    payment_cycle = models.CharField(max_length=50, choices=payment_cycle)
    year_payment_cycle_month = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
                ],
        )
    description = models.CharField(max_length=250)

    def __unicode__(self):
        if self.sum_type == 'AMOUNT':
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.amount_rate)


# This is incentive(for motivation)
class Incentive(models.Model):
    # deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
    name = models.CharField(max_length=100)
    employee_grade = models.ForeignKey(EmployeeGrade)
    # Any one of the two should be filled
    sum_type = models.CharField(max_length=50, choices=deduct_choice)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    # When to pay? == May be we should keep it in setting
    # payment_cycle = [('M', _('Monthly')), ('Y', _('Yearly')), ('D', _('Daily')),  ('H', _('Hourly'))]
    payment_cycle = models.CharField(max_length=50, choices=payment_cycle)
    year_payment_cycle_month = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
                ],
        )
    description = models.CharField(max_length=250)

    def __unicode__(self):
        if self.sum_type == 'AMOUNT':
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.rate)


class BranchOffice(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


# These two below should be in setting as many to many
# Imp: Deductin cant be in BAnk Account type and should be one to one with account type
class Deduction(models.Model):
    # deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
    name = models.CharField(max_length=150)
    # Below only one out of two should be active
    deduct_type = models.CharField(max_length=50, choices=deduct_choice)
    deduction_for = models.CharField(max_length=50, choices=deduct_for)
    # Explit acc is only specified when deduction for is explicit_acc
    explicit_acc = models.ForeignKey(Account, null=True, blank=True)
    # In which type of account to make deduction transaction when deduction for is employee acc
    in_acc_type = models.ForeignKey(AccountType)
    # transact_in = models.CharField(choice=acc_type)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=150)
    priority = models.IntegerField(unique=True)

    with_temporary_employee = models.BooleanField(default=False)
    # For permanent
    add2_init_salary = models.BooleanField(default=False)

    taxable = models.BooleanField(default=False)

    def __unicode__(self):
        if self.deduct_type == 'AMOUNT':
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.amount_rate)

    def save(self, *args, **kwargs):
        if self.explicit_acc:
            self.with_temporary_employee = True
        super(Deduction, self).save(*args, **kwargs)


class Employee(models.Model):
    # Budget code (Functionality to change budget code for employee group)
    budget_code = models.CharField(max_length=100)
    # working_branch = models.CharField(max_length=100)
    # Employee ko section or branch coz he can be in another branch and paid from central
    sex_choice = [('M', _('Male')), ('F', _('Female'))]
    marital_statuses = [('M', _('Married')), ('U', _('Unmarried'))]
    employee = models.OneToOneField(User)
    sex = models.CharField(choices=sex_choice, max_length=1)
    marital_status = models.CharField(
        default='U',
        max_length=1,
        choices=marital_statuses
    )
    designation = models.ForeignKey(Designation)
    pan_number = models.CharField(max_length=100)
    working_branch = models.ForeignKey(BranchOffice)
    accounts = models.ManyToManyField(Account, through="EmployeeAccount")
    # bank_account = models.OneToOneField(Account,
    #                                     related_name='bank_account')
    # insurance_account = models.OneToOneField(Account,
    #                                          related_name='insurance_acc')
    # nalakosh_account = models.OneToOneField(Account,
    #                                         related_name='nalakosh_acc')
    # # Change the name below to sanchaya_account
    # sanchayakosh_account = models.OneToOneField(Account,
    #                                        related_name='sanchai_acc')
    # pro_tempore = models.OneToOneField('self', null=True, blank=True, related_name='pro_temp')
    # Talab rokka(Should not transact when payment_halt=True)
    payment_halt = models.BooleanField(default=False)
    appoint_date = BSDateField(default=today)
    dismiss_date = BSDateField(null=True, blank=True)
    # allowance will be added to salary 
    allowances = models.ManyToManyField(Allowance, blank=True)
    # incentive will have diff trancation
    incentives = models.ManyToManyField(Incentive, blank=True)
    # Permanent has extra functionality while deduction from salary
    is_permanent = models.BooleanField(default=False)
    # deductions need to be removed from this table
    # deductions = models.ManyToManyField(Deduction)

    # def current_salary(self, add_month):
    #     grade_salary = self.designation.grade.salary_scale
    #     grade_number = self.designation.grade.grade_number
    #     grade_rate = self.designation.grade.grade_rate
    #     # Instead of appoint_date we need to use lagu miti for now its oppoint date and lagu miti should be in appSETTING
    #     appointed_since = today() - self.appoint_date
    #     total_days = appointed_since.days
    #     salary = 0
    #     years_worked = total_days/365
    #     if years_worked <= grade_number:
    #         salary += grade_salary + int(years_worked) * grade_rate
    #     elif years_worked > grade_number:
    #         salary += grade_salary + grade_number * grade_rate
    #     if add_month:
    #         for i in range(1, add_month+1):
    #             month_days = bs[today.year][today.month+i-1]
    #             total_days += month_days
    #             years_worked = total_days/365
    #             if years_worked <= grade_number:
    #                 salary += grade_salary + int(years_worked) * grade_rate
    #             elif years_worked > grade_number:
    #                 salary += grade_salary + grade_number * grade_rate
    #     return salary

    def current_salary_by_month(self, from_date, to_date):
        grade_salary = self.designation.grade.salary_scale
        grade_number = self.designation.grade.grade_number
        grade_rate = self.designation.grade.grade_rate
        salary = 0
        for year, month in get_y_m_tuple_list(from_date, to_date):
            if type(from_date) == type(to_date):
                if isinstance(from_date, date):
                    try:
                        days_worked = date(year, month, 1) - self.appoint_date
                    except:
                        raise TypeError('Internal and external setting mismatch')
                else:
                    if isinstance(self.appoint_date, date):
                        raise TypeError('Internal and external setting mismatch')
                    else:
                        days_worked = date(*bs2ad(date(year, month, 1))) - date(*bs2ad((self.appoint_date)))

            years_worked = days_worked.days / 365
            if years_worked <= grade_number:
                salary += grade_salary + int(years_worked) * grade_rate
            elif years_worked > grade_number:
                salary += grade_salary + grade_number * grade_rate
        return salary

    def current_salary_by_day(self, from_date, to_date):
        if from_date.year == to_date.year and from_date.month == to_date.month:
            salary_pure_months = 0
            lhs_month_salary = 0
            lhs_days = 0
            if type(from_date) == type(to_date):
                if isinstance(from_date, date):
                    month = date(from_date.year, from_date.month, 1)
                    # We need to add because from and to in same month
                    # Will be different when many months
                    # because we cut them to slots
                    rhs_days = (to_date - from_date).days + 1

                    from_date_month_days = mr(month.year, month.month)[1]
                    to_date_month_days = from_date_month_days
                else:
                    month = BSDate(from_date.year, from_date.month, 1)
                    rhs_days = (to_date - from_date).days + 1
                    from_date_month_days = bs[month.year][month.month-1]
                    to_date_month_days = from_date_month_days
                    # pdb.set_trace()

            rhs_month_salary = self.current_salary_by_month(
                month,
                month
                )

        elif are_side_months(from_date, to_date):
            salary_pure_months = 0
            if type(from_date) == type(to_date):
                if isinstance(from_date, date):
                    lhs_month = date(from_date.year, from_date.month, 1)
                    rhs_month = date(to_date.year, to_date.month, 1)
                    lhs_days = (rhs_month - from_date).days
                    rhs_days = (to_date - rhs_month).days + 1

                    from_date_month_days = mr(lhs_month.year, lhs_month.month)[1]
                    to_date_month_days = mr(rhs_month.year, rhs_month.month)[1]

                else:
                    lhs_month = BSDate(from_date.year, from_date.month, 1)
                    rhs_month = BSDate(to_date.year, to_date.month, 1)
                    lhs_days = (rhs_month - from_date).days
                    rhs_days = (to_date - rhs_month).days + 1

                    from_date_month_days = bs[lhs_month.year][lhs_month.month-1]
                    to_date_month_days = bs[rhs_month.year][rhs_month.month-1]
            lhs_month_salary = self.current_salary_by_month(
                lhs_month,
                lhs_month
                )
            rhs_month_salary = self.current_salary_by_month(
                rhs_month,
                rhs_month
                )
        else:
            # Get pure months
            if type(from_date) == type(to_date):
                if isinstance(from_date, date):
                    if from_date.month == 12:
                        from_date_m = date(from_date.year + 1, 1, 1)
                    else:
                        from_date_m = date(from_date.year, from_date.month + 1, 1)
                    if to_date.month == 1:
                        to_date_m = date(to_date.year-1, 12, 1)
                    else:
                        to_date_m = date(to_date.year, to_date.month-1, 1)
                    lhs_month = date(from_date.year, from_date.month, 1)
                    rhs_month = date(to_date.year, to_date.month, 1)
                    lhs_days = (from_date_m - from_date).days
                    rhs_days = (to_date - to_date_m).days + 1

                    from_date_month_days = mr(lhs_month.year, lhs_month.month)[1]
                    to_date_month_days = mr(rhs_month.year, rhs_month.month)[1]

                else:
                    if from_date.month == 12:
                        from_date_m = BSDate(from_date.year+1, 1, 1)
                    else:
                        from_date_m = BSDate(from_date.year, from_date.month+1, 1)
                    if to_date.month == 1:
                        to_date_m = BSDate(to_date.year-1, 12, 1)
                    else:
                        to_date_m = BSDate(to_date.year, to_date.month-1, 1)
                    lhs_month = BSDate(from_date.year, from_date.month, 1)
                    rhs_month = BSDate(to_date.year, to_date.month, 1)
                    lhs_days = (from_date_m - from_date).days
                    rhs_days = (to_date - to_date_m).days + 1

                    from_date_month_days = bs[lhs_month.year][lhs_month.month-1]
                    to_date_month_days = bs[rhs_month.year][rhs_month.month-1]

            salary_pure_months = self.current_salary_by_month(
                from_date_m,
                to_date_m
                )
            lhs_month_salary = self.current_salary_by_month(
                lhs_month,
                lhs_month
                )
            rhs_month_salary = self.current_salary_by_month(
                rhs_month,
                rhs_month
                )
        lhs_salary = lhs_month_salary / float(from_date_month_days) * lhs_days
        rhs_salary = rhs_month_salary / float(to_date_month_days) * rhs_days
        salary = salary_pure_months + lhs_salary + rhs_salary
        return salary

        # grade_salary = self.designation.grade.salary_scale
        # grade_number = self.designation.grade.grade_number
        # grade_rate = self.designation.grade.grade_rate
        # salary = 0
        pass

    def has_account(self, account_type):
        for i in self.accounts.all():
            if i.employee_account.account_type == account_type:
                return True
        return False

    def __unicode__(self):
        return str(self.employee.full_name)


class ProTempore(models.Model):
    employee = models.OneToOneField(Employee,
                                    related_name="real_employee_post")
    pro_tempore = models.OneToOneField(Employee,
                                       related_name="virtual_employee_post")
    appoint_date = BSDateField(default=today)
    dismiss_date = BSDateField(null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)

    # Employee is permanent o r temporary? 10% PF in permanent
    # Beema(insurance) +200
    # There is also another insurance in Nagarik Lagani kosh()

    #dEDUCTION PART(employee)
    # In  permanent case:
    # 10% x 2 to sanchaikosh
    # Bima ie 200 currently x 2 nagarik lagani kosh(bima)
    # There is also another insurance in Nagarik Lagani kosh().. Person anusar farak rate either in percentage or fixed rate
    # Advance settlement
    # There can also be some other deduction eg in earthquake gov cut it down
    # Social Security tax (1%)
    # Remunuration Tax (income tax)
    # Baki chai either in bank or cash

    # Sabai ko account huncha 


class IncomeTaxRate(models.Model):
    start_from = models.FloatField()
    end_to = models.FloatField(null=True, blank=True)
    tax_rate = models.FloatField()
    rate_over_tax_amount = models.FloatField(null=True, blank=True)
    is_last = models.BooleanField(default=False)
    # Income tax ma female ko lago 10% discount(Suruma tax lagaera??)

    def __unicode__(self):
        return u"From %f" % (self.start_from)


class DeductionDetail(models.Model):
    deduction = models.ForeignKey(Deduction, related_name='deduced_amount_detail')
    amount = models.FloatField()


class PaymentRecord(models.Model):
    paid_employee = models.ForeignKey(Employee)
    paid_from_date = BSDateField()
    paid_to_date = BSDateField()
    absent_days = models.PositiveIntegerField()
    allowance = models.FloatField(null=True, blank=True)
    incentive = models.FloatField(null=True, blank=True)
    deduction_detail = models.ManyToManyField(DeductionDetail, blank=True)
    income_tax = models.FloatField(null=True, blank=True)
    pro_tempore_amount = models.FloatField(null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    paid_amount = models.FloatField()
    # Deducted amount fields
    # How much incentive and how much allowance

    def total_present_days(self):
        return self.paid_to_date - self.paid_from_date - self.absent_days

    def __unicode__(self):
        return str(self.id)


class PayrollEntry(models.Model):
    entry_row = models.ManyToManyField(PaymentRecord)
    entry_datetime = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)


class EmployeeAccount(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    account = models.OneToOneField(
                                    Account,
                                    on_delete=models.CASCADE,
                                    related_name='employee_account',
                                    )
    account_type = models.ForeignKey(
                                    AccountType
                                    )

    class Meta:
        unique_together = (("employee", "account"),)


class CompanyAccount(models.Model):
    account = models.OneToOneField(
                                    Account,
                                    on_delete=models.CASCADE,
                                    related_name='company_account'
                                    )

# class HrConfig(dbsettings.Group):
#     sk_deduction_rate = models.PositiveIntegerField()
#     maintenance_mode = models.BooleanField(default=False)
#     ** Sanchai Kosh ko percentage
#     ** Tax rate
#     ** Lagu miti of rate
#     ** Absent case

#     def __unicode__(self):
#         return u"hr config"

#     class Meta:
#         verbose_name = "Setup Income Tax Rate"


#  allowance in EmployeeRank
#  Incentive in Employee

# to do
# Maximim provision of grade rate upto 10 times ==> constant or variable
# Manage allowance, Incentive and Tax with  salary
# Think about salary paused
# niyukti **of


# Can employee be django auth user? Yes
# Case of employee as technician##Done

# In case employee is pro-tempore we need to transact his normal salary and extract pro-tempor employee salay, get the difference of their salary and transact differnece seperately
#  Talab rokka
#  When did emloyee start his job
#  
#  
#  Incentive rate employee anusar farak huncha month anusar pani farak parcha
#  Salary advance
#  
#  
#  When Salary increased in middle of the month each day earning shoud be calculated ****
#  
#  
#  
#  Make branch model with code on which employee work
  
  
#  When does increse in scale get active?
#  The day from which the goverment announces it or the day from which the employeer is apponted