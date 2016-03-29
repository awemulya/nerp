from django.contrib import admin
from .models import AccountType, Account, Transaction, EmployeeGrade, Employee, Designation, Incentive, Allowence, IncomeTaxRate, BranchOffice, Deduction, ProTempore, PaymentRecord, PayrollEntry

admin.site.register(AccountType)
admin.site.register(Account)
admin.site.register(Transaction)

admin.site.register(EmployeeGrade)
admin.site.register(Employee)
admin.site.register(Designation)
admin.site.register(Incentive)
admin.site.register(Allowence)
admin.site.register(IncomeTaxRate)
admin.site.register(BranchOffice)
admin.site.register(Deduction)
admin.site.register(ProTempore)
admin.site.register(PaymentRecord)
admin.site.register(PayrollEntry)
