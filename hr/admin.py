from django.contrib import admin
from .models import Account, EmployeeGrade, Employee, Designation, Incentive, Allowence, IncomeTaxRate

admin.site.register(Account)
admin.site.register(EmployeeGrade)
admin.site.register(Employee)
admin.site.register(Designation)
admin.site.register(Incentive)
admin.site.register(Allowence)
admin.site.register(IncomeTaxRate)
