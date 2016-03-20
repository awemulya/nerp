# import dbsetting
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from users.models import User
from core.models import FiscalYear
# from solo.models import SingletonModel
# from django.core.exceptions import ValidationError


# def validate_month(value):
#     if value < 1 and value > 12:
#         raise ValidationError(
#             _('%(value)s is not'),
#             params={'value': value},
#         )


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=200)
    branch =models.CharField(max_length=150)
    acc_number = models.CharField(max_length=100)

    def __unicode__(self):
        return self.bank_name


class EmployeeGrade(models.Model):
    grade_name = models.CharField(max_length=100)
    rate = models.FloatField()
    # rate increases yearly with grade rate. Also shold mention when in setting? How much times
    grade_rate = models.FloatField()
    parent_grade = models.ForeignKey('self', null=True, blank=True)
    # When employee is tecnician it should have no siblings
    is_tecnician = models.BooleanField(deault=False)

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
    amount = models.FloatField()
    # When to pay? Should be in setting
    rate_of_payment = [('M', _('Monthly')), ('Y', _('Yearly')), ('D', _('Daily')),  ('H', _('Hourly'))]
    description = models.Charfield(max_length=250)

    def __unicode__(self):
        return self.name


# This is incentive(for motivation)
class Incentive(models.Model):
    name = models.CharField(max_length=100)
    employee_grade = models.ForeignKey(EmployeeGrade)
    amount = models.FloatField()
    # When to pay?
    rate_of_payment = [('M', _('Monthly')), ('Y', _('Yearly')), ('D', _('Daily')),  ('H', _('Hourly'))]

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    # Budget code (Functionality to change budget code for employee group)
    # Employee ko section or branch coz he can be in another branch and payed from central
    sex_choice = [('M', _('Male')), ('F', _('Female'))]
    employee = models.ForeignKey(User)
    sex = models.CharField(choices=sex_choice, max_length=1)
    designation = models.ForeignKey(Designation)
    pan_number = models.CharField(max_length=100)
    bank_account = models.ForeignKey(BankAccount)
    pro_tempore = models.ForeignKey('self', null=True, blank=True)
    # Talab rokka(Should not transact when payment_halt=True)
    payment_halt = models.BooleanField(default=False)
    appoint_date = models.DateField(default=timezone.now().date())
    # allowence will be added to salary 
    allowence = models.ManyToManyField(Allowence, null=True, blank=True)
    # incentive will have diff trancation
    incentive = models.ManyToManyField(Incentive, null=True, blank=True)
    # Employee is permanent or temporary? 10% PF in permanent
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
    month = [(1, _('Baisak')),
             (2, _('Jeth')),
             (3, _('Aasar')),
             (4, _('Shrawan')),
             (5, _('Bhadra')),
             (6, _('Aswin')),
             (7, _('Kartik')),
             (8, _('Mangsir')),
             (9, _('Poush')),
             (10, _('Magh')),
             (11, _('Falgun')),
             (12, _('Chaitra')),
             ]
    payed_to = models.ForeignKey(Employee)
    fiscal_year = models.ForeignKey(FiscalYear)
    month = models.IntegerField(choices=month)


# class IncomeTaxConfig(dbsettings.Group):
#     site_name = models.CharField(max_length=255, default='Site Name')
#     maintenance_mode = models.BooleanField(default=False)

#     def __unicode__(self):
#         return self.

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