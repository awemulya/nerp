# import dbsettings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import User
from core.models import validate_in_fy
from njango.fields import BSDateField, today

# from core.models import FiscalYear
# from solo.models import SingletonModel
# from django.core.exceptions import ValidationError


# def validate_month(value):
#     if value < 1 and value > 12:
#         raise ValidationError(
#             _('%(value)s is not'),
#             params={'value': value},
#         )

# acc_type = [('BANK ACC', _('Bank Account')), ('INSURANCE ACC', _('InsuranceAccount')), ('NALA ACC', _('Nagarik Lagani Kosh Account')), ('SANCHAI KOSH', _('Sanchai Kosh'))]
deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]


class AccountType(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)


class Account(models.Model):
    holder_type = [('EMPLOYEE', _("Employee's Account")), ('COMPANY', _('Company Account'))]
    account_holder_type = models.CharField(choices=holder_type, max_length=50)
    account_type = models.ForeignKey(AccountType)
    org_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=150)
    acc_number = models.CharField(max_length=100)
    description = models.CharField(max_length=256)

    def __unicode__(self):
        return '%s[%s][%s]' %  (self.account_type, self.org_name, self.acc_number)  


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
    duduct_type = models.CharField(max_length=50, choices=deduct_choice)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    # When to pay? ==> May be it should be in settingShould be in setting
    payment_cycle = [('M', _('Monthly')), ('Y', _('Yearly')), ('D', _('Daily')),  ('H', _('Hourly'))]
    description = models.CharField(max_length=250)

    def __unicode__(self):
        if self.deduct_type == 'AMOUNT':
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.rate)


# This is incentive(for motivation)
class Incentive(models.Model):
    # deduct_choice = [('AMOUNT', _('Amount')), ('RATE', _('Rate'))]
    name = models.CharField(max_length=100)
    employee_grade = models.ForeignKey(EmployeeGrade)
    # Any one of the two should be filled
    duduct_type = models.CharField(max_length=50, choices=deduct_choice)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    # When to pay? == May be we should keep it in setting
    payment_cycle = [('M', _('Monthly')), ('Y', _('Yearly')), ('D', _('Daily')),  ('H', _('Hourly'))]
    description = models.CharField(max_length=250)

    def __unicode__(self):
        if self.deduct_type == 'AMOUNT':
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
    duduct_type = models.CharField(max_length=50, choices=deduct_choice)
    # In which type of account to make deduction transaction
    in_acc_type = models.OneToOneField(AccountType)
    # transact_in = models.CharField(choice=acc_type)
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=150)

    def __unicode__(self):
        if self.deduct_type == 'AMOUNT':
            return '%s, %f' % (self.name, self.amount)
        else:
            return '%s, %f' % (self.name, self.rate)


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
    bank_account = models.OneToOneField(Account, related_name='bank_account')
    insurance_account = models.OneToOneField(Account, related_name='insurance_acc')
    nalakosh_account = models.OneToOneField(Account, related_name='nalakosh_acc')
    sanchai_account = models.OneToOneField(Account, related_name='sanchai_acc')
    # pro_tempore = models.OneToOneField('self', null=True, blank=True, related_name='pro_temp')
    # Talab rokka(Should not transact when payment_halt=True)
    payment_halt = models.BooleanField(default=False)
    appoint_date = models.DateField(auto_now_add=True)
    dismiss_date = models.DateField(null=True, blank=True)
    # allowence will be added to salary 
    allowence = models.ManyToManyField(Allowence, blank=True)
    # incentive will have diff trancation
    incentive = models.ManyToManyField(Incentive, blank=True)
    # Permanent has extra functionality while deduction from salary
    is_permanent = models.BooleanField(default=False)
    deductions = models.ManyToManyField(Deduction)

    def current_salary(self):
        grade_salary = self.designation.grade.salary_scale
        grade_number = self.designation.grade.grade_number
        grade_rate = self.designation.grade.grade_rate
        # Instead of appoint_date we need to use lagu miti for now its oppoint date and lagu miti should be in appSETTING
        appointed_since = timezone.now().date() - self.appoint_date
        years_worked = appointed_since.days/365.25
        if years_worked <= grade_number:
            return grade_salary + int(years_worked) * grade_rate
        elif grade_number > years_worked:
            return grade_salary + grade_number * grade_rate

    def __unicode__(self):
        return str(self.id)


class ProTempore(models.Model):
    employee = models.OneToOneField(Employee, related_name="real_employee_post")
    pro_tempore = models.OneToOneField(Employee, related_name="virtual_employee_post")
    appoint_date = models.DateField(auto_now_add=True)
    dismiss_date = models.DateField(null=True, blank=True)

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
    # 
    # Sabai ko account huncha 


class IncomeTaxRate(models.Model):
    start_from = models.FloatField()
    end_to = models.FloatField()
    tax_rate = models.FloatField()

    # Income tax ma female ko lago 10% discount(Suruma tax lagaera??)

    def __unicode__(self):
        return u"From %f - %f is %f%"


class PaymentRecord(models.Model):
    paid_employee = models.ForeignKey(Employee)
    paid_from_date = BSDateField()
    paid_to_date = BSDateField()
    absent_days = models.PositiveIntegerField()
    allowence = models.FloatField(null=True, blank=True)
    incentive = models.FloatField(null=True, blank=True)
    deduced_amount = models.FloatField(null=True, blank=True)
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