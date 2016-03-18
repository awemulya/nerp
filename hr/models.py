from django.db import models
from django.utils.translation import ugettext_lazy as _


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=200)
    acc_number = models.CharField(max_length=100)


class EmployeeGrade(models.Model):
    grade_name = models.CharField(max_length=100)
    rate = models.FloatField()
    grade_rate = models.FloatField()
    parent_grade = models.ForeignKey('self', null=True, blank=True)


class Employee(models.Model):
    sex_choice = [('M', _('Male')), ('F', _('Female'))]
    name = models.CharField(max_length=100)
    sex = models.CharField(choices=sex_choice, max_length=1)
    grade = models.ForeignKey(EmployeeGrade)
    pan_number = models.CharField(max_length=100)
    bank_account = models.ForeignKey(BankAccount)


# This is bhatta
class Allowence(models.Model):
    pass


# This is incentive
class Incentive(models.Model):
    pass





# to do
# Maximim provision of grade rate upto 10 times
