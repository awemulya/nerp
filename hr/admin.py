from django.contrib import admin
from .models import BankAccount, EmployeeGrade, Employee, Designation, Incentive, Allowence, IncomeTaxRate

admin.site.register(BankAccount)
admin.site.register(EmployeeGrade)
admin.site.register(Employee)
admin.site.register(Designation)
admin.site.register(Incentive)
admin.site.register(Allowence)
admin.site.register(IncomeTaxRate)
