# import dbsettings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import User
from core.models import validate_in_fy
from njango.fields import BSDateField, today
from njango.nepdate import bs2ad, bs
from django.core.validators import MaxValueValidator, MinValueValidator
from calendar import monthrange as mr
from datetime import date

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

# Allowence
# When yearly than when to pay should be in setting


def get_y_m_tuple_list(from_date, to_date):
    return_list = []
    while from_date <= to_date:
        return_list.append((from_date.year, from_date.month))
        if from_date.month < 12:
            from_date = date(
                from_date.year,
                from_date.month + 1,
                from_date.day
                )
        else:
            from_date = date(
                from_date.year + 1,
                1,
                from_date.day
                )
    return return_list


def are_side_months(from_date, to_date):
    if from_date.year == to_date.year and to_date.month - from_date.month == 1:
        return True
    elif to_date.year - from_date.year == 1 and from_date.month - to_date.month == 11:
        return True
    else:
        return False


class AccountType(models.Model):
    name = models.CharField(max_length=150, choices=acc_type, unique=True)
    description = models.CharField(max_length=250)
    permanent_multiply_rate = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Account(models.Model):
    # account_holder_type = models.CharField(choices=holder_type, max_length=50)
    # account_type = models.ForeignKey(AccountType)
    org_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=150)
    acc_number = models.CharField(max_length=100)
    description = models.CharField(max_length=256)

    def __unicode__(self):
        return '[%s][%s]' % (
                                   # self.account_type,
                                   self.org_name,
                                   self.acc_number,
                                   # self.account_holder_type
                                   )


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    credit = models.FloatField()
    debit = models.FloatField()
    date_time = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return str(self.account.id)

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
class Allowence(models.Model):
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

    def __unicode__(self):
        if self.deduct_type == 'AMOUNT':
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.amount_rate)


class Employee(models.Model):
    # Budget code (Functionality to change budget code for employee group)
    budget_code = models.CharField(max_length=100)
    # working_branch = models.CharField(max_length=100)
    # Employee ko section or branch coz he can be in another branch and paid from central
    sex_choice = [('M', _('Male')), ('F', _('Female'))]
    employee = models.OneToOneField(User)
    sex = models.CharField(choices=sex_choice, max_length=1)
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
    # allowence will be added to salary 
    allowences = models.ManyToManyField(Allowence, blank=True)
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

    def current_salary_by_month(self, date_type, from_date, to_date):
        grade_salary = self.designation.grade.salary_scale
        grade_number = self.designation.grade.grade_number
        grade_rate = self.designation.grade.grade_rate
        salary = 0
        for year, month in get_y_m_tuple_list(from_date, to_date):
            if date_type == 'AD':
                days_worked = date(year, month, 1) - self.appoint_date
            else:
                days_worked = date(*bs2ad(date(year, month, 1))) - date(*bs2ad((self.appoint_date)))

            years_worked = days_worked.days/365
            if years_worked <= grade_number:
                salary += grade_salary + int(years_worked) * grade_rate
            elif years_worked > grade_number:
                salary += grade_salary + grade_number * grade_rate
        return salary

    def current_salary_by_day(self, date_type, from_date, to_date):
        if from_date.year == to_date.year and from_date.month == to_date.month:
            salary_pure_months = 0
            lhs_month_salary = 0
            month = date(from_date.year, from_date.month, 1)
            rhs_month_salary = self.current_salary_by_month(
                date_type,
                month,
                month
                )
            lhs_days = 0
            if date_type == 'AD':
                # We need to add because from and to in same month
                # Will be different when many months
                # because we cut them to slots
                rhs_days = (to_date - from_date).days + 1

                from_date_month_days = mr(month.year, month.month)[1]
                to_date_month_days = from_date_month_days
            else:
                rhs_days = (date(*bs2ad(to_date)) - date(*bs2ad(from_date))).days + 1
                from_date_month_days = bs[month.year][month.month-1]
                to_date_month_days = from_date_month_days

        elif are_side_months(from_date, to_date):
            salary_pure_months = 0
            lhs_month = date(from_date.year, from_date.month, 1)
            rhs_month = date(to_date.year, to_date.month, 1)
            lhs_month_salary = self.current_salary_by_month(
                date_type,
                lhs_month,
                lhs_month
                )
            rhs_month_salary = self.current_salary_by_month(
                date_type,
                rhs_month,
                rhs_month
                )
            if date_type == 'AD':
                lhs_days = (rhs_month - from_date).days
                rhs_days = (to_date - rhs_month).days + 1

                from_date_month_days = mr(lhs_month.year, lhs_month.month)[1]
                to_date_month_days = mr(rhs_month.year, rhs_month.month)[1]

            else:
                lhs_days = (date(*bs2ad(rhs_month)) - date(*bs2ad(from_date))).days
                rhs_days = (date(*bs2ad(to_date)) - date(*bs2ad(rhs_month))).days +1

                from_date_month_days = bs[lhs_month.year][lhs_month.month-1]
                to_date_month_days = bs[rhs_month.year, rhs_month.month-1]
        else:
            # Get pure months
            if from_date.month == 12:
                from_date_m = date(from_date.year+1, 1, 1)
            else:
                from_date_m = date(from_date.year, from_date.month+1, 1)
            if to_date.month == 1:
                to_date_m = date(to_date.year-1, 12, 1)
            else:
                to_date_m = date(to_date.year, to_date.month-1, 1)
            lhs_month = date(from_date.year, from_date.month, 1)
            rhs_month = date(to_date.year, to_date.month, 1)
            salary_pure_months = self.current_salary_by_month(
                date_type,
                from_date_m,
                to_date_m
                )
            lhs_month_salary = self.current_salary_by_month(
                date_type,
                lhs_month,
                lhs_month
                )
            rhs_month_salary = self.current_salary_by_month(
                date_type,
                rhs_month,
                rhs_month
                )
            if date_type == 'AD':
                lhs_days = (from_date_m - from_date).days
                rhs_days = (to_date - to_date_m).days + 1

                from_date_month_days = mr(lhs_month.year, lhs_month.month)[1]
                to_date_month_days = mr(rhs_month.year, rhs_month.month)[1]

            else:
                lhs_days = (date(*bs2ad(from_date_m)) - date(*bs2ad(from_date))).days
                rhs_days = (date(*bs2ad(to_date)) - date(*bs2ad(to_date_m))).days +1

                from_date_month_days = bs[lhs_month.year][lhs_month.month-1]
                to_date_month_days = bs[rhs_month.year][rhs_month.month-1]

        lhs_salary = lhs_month_salary/from_date_month_days * lhs_days
        rhs_salary = rhs_month_salary/to_date_month_days + rhs_days
        salary = salary_pure_months + lhs_salary + rhs_salary
        return salary

        # grade_salary = self.designation.grade.salary_scale
        # grade_number = self.designation.grade.grade_number
        # grade_rate = self.designation.grade.grade_rate
        # salary = 0
        pass

    def __unicode__(self):
        return str(self.employee.full_name)


class ProTempore(models.Model):
    employee = models.OneToOneField(Employee,
                                    related_name="real_employee_post")
    pro_tempore = models.OneToOneField(Employee,
                                       related_name="virtual_employee_post")
    appoint_date = BSDateField(default=today)
    dismiss_date = BSDateField(null=True, blank=True)

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


class PaymentRecord(models.Model):
    paid_employee = models.ForeignKey(Employee)
    paid_from_date = BSDateField()
    paid_to_date = BSDateField()
    absent_days = models.PositiveIntegerField()
    allowence = models.FloatField(null=True, blank=True)
    incentive = models.FloatField(null=True, blank=True)
    deduced_amount = models.FloatField(null=True, blank=True)
    income_tax = models.FloatField(null=True, blank=True)
    paid_amount = models.FloatField()
    # Deducted amount fields
    # How much incentive and how much allowence

    def total_present_days(self):
        return self.paid_to_date - self.paid_from_date - self.absent_days

    def __unicode__(self):
        return str(self.id)


class PayrollEntry(models.Model):
    entry_row = models.ManyToManyField(PaymentRecord)
    entry_datetime = models.DateTimeField(default=timezone.now)


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


#  Allowence in EmployeeRank
#  Incentive in Employee

# to do
# Maximim provision of grade rate upto 10 times ==> constant or variable
# Manage Allowence, Incentive and Tax with  salary
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