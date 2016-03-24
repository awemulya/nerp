# import dbsettings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import User
# from core.models import FiscalYear
# from solo.models import SingletonModel
# from django.core.exceptions import ValidationError


# def validate_month(value):
#     if value < 1 and value > 12:
#         raise ValidationError(
#             _('%(value)s is not'),
#             params={'value': value},
#         )


class Account(models.Model):
    acc_type = [('BANK ACC', _('Bank Account')), ('INSURANCE ACC', _('InsuranceAccount')), ('NALA ACC', _('Nagarik Lagani Kosh Account')), ('SANCHAI KOSH', _('Sanchai Kosh'))]
    holder_type = [('EMPLOYEE', _("Employee's Account")), ('COMPANY', _('Company Account'))]
    account_holder_type = models.CharField(choices=holder_type)
    account_type = models.CharField(options=acc_type)
    org_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=150)
    acc_number = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    credit = models.FloatField()
    debit = models.FloatField()

    def __unicode__(self):
        return '%s[%s][%s]' %  (self.account_type, self.org_name, self.acc_number)  


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
    is_tecnicial = models.BooleanField(deault=False)

    def __unicode__(self):
        if self.is_tecnician:
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
    name = models.CharField(max_length=100)
    employee_grade = models.ForeignKey(EmployeeGrade)
    # Any one out of two should be filled
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    # When to pay? ==> May be it should be in settingShould be in setting
    payment_cycle = [('M', _('Monthly')), ('Y', _('Yearly')), ('D', _('Daily')),  ('H', _('Hourly'))]
    description = models.Charfield(max_length=250)

    def __unicode__(self):
        return self.name


# This is incentive(for motivation)
class Incentive(models.Model):
    name = models.CharField(max_length=100)
    employee_grade = models.ForeignKey(EmployeeGrade)
    # Any one of the two should be filled
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    # When to pay? == May be we should keep it in setting
    payment_cycle = [('M', _('Monthly')), ('Y', _('Yearly')), ('D', _('Daily')),  ('H', _('Hourly'))]
    description = models.Charfield(max_length=250)

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    # Budget code (Functionality to change budget code for employee group)
    budget_code = models.CharField(max_length=100)
    working_branch = models.CharField(max_length=100)
    # Employee ko section or branch coz he can be in another branch and payed from central
    sex_choice = [('M', _('Male')), ('F', _('Female'))]
    employee = models.OneToOneField(User)
    sex = models.CharField(choices=sex_choice, max_length=1)
    designation = models.ForeignKey(Designation)
    pan_number = models.CharField(max_length=100)
    bank_account = models.OneToOneField(Account)
    insurance_account = models.OneToOneField(Account)
    nalakosh_account = models.OneToOneField(Account)
    pro_tempore = models.OneToOneField('self', null=True, blank=True)
    # Talab rokka(Should not transact when payment_halt=True)
    payment_halt = models.BooleanField(default=False)
    appoint_date = models.DateField(default=timezone.now().date())
    # allowence will be added to salary 
    allowence = models.ManyToManyField(Allowence, null=True, blank=True)
    # incentive will have diff trancation
    incentive = models.ManyToManyField(Incentive, null=True, blank=True)
    # Permanent has extra functionality while deduction from salary
    is_permanent = models.BooleanField(default=False)

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


# This should be in setting as many to many
class Deduction(models.Models):
    name = models.CharField(max_length=150)
    # Below only one out of two should be active
    amount = models.FloatField(null=True, blank=True)
    amount_rate = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class IncomeTaxRate(models.Model):
    start_from = models.FloatField()
    end_to = models.FloatField()
    tax_rate = models.FloatField()

    # Income tax ma female ko lago 10% discount

    def __unicode__(self):
        return u"From %f - %f is %f%"


class PaymentRecord(models.Model):
    payed_employee = models.ForeignKey(Employee)
    payed_from_date = models.DateField()
    payed_to_date = models.DateField()
    absent_days = models.PositiveIntegerField()
    deductiom = models.ManyToManyField(Deduction)
    payed_amout = models.FloatField()
    # Deducted amount fields

    def total_present_days(self):
        return self.payed_to_date - self.payed_from_date - self.absent_days

    def __unicode__(self):
        return str(self.id)

# class HrConfig(dbsettings.Group):
#     site_name = models.CharField(max_length=255, default='Site Name')
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
#  When Salary increased in middle of the month each day earning shoud be calculated
#  
#  
#  
#  Make branch model with code on which employee work
  
  
#  When does increse in scale get active?
#  The day from which the goverment announces it or the day from which the employeer is apponted