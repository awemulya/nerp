from django.contrib import admin
from .models import AccountType, Account,EmployeeAccount, Transaction, EmployeeGrade, Employee, Designation, Incentive, Allowance, IncomeTaxRate, BranchOffice, Deduction, ProTempore, PaymentRecord, PayrollEntry, IncentiveName, AllowanceName, DeductionDetail, IncentiveDetail, AllowanceDetail
from .forms import EmployeeAccountInlineFormset


class EmployeeAccountInline(admin.TabularInline):
    model = EmployeeAccount
    formset = EmployeeAccountInlineFormset
    extra = 1


class EmployeeAdmin(admin.ModelAdmin):
    inlines = (EmployeeAccountInline,)
    # form = EmployeeForm
    pass


# class AccountAdmin(admin.ModelAdmin):
#     inlines = (EmployeeAccountInline,)



# class AccountInline(admin.TabularInline):
#     model = EmployeeAccount.account.through


# class EmployeeInline(admin.TabularInline):
#     model = EmployeeAccount.employee.through


# class EmployeeAccountAdmin(admin.ModelAdmin):
#     pass


admin.site.register(AccountType)
admin.site.register(Account)
admin.site.register(Transaction)

admin.site.register(EmployeeGrade)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Designation)
admin.site.register(Incentive)
admin.site.register(Allowance)
admin.site.register(IncomeTaxRate)
admin.site.register(BranchOffice)
admin.site.register(Deduction)
admin.site.register(ProTempore)
admin.site.register(PaymentRecord)
admin.site.register(PayrollEntry)
admin.site.register(EmployeeAccount)
admin.site.register(IncentiveName)
admin.site.register(AllowanceName)

admin.site.register(DeductionDetail)
admin.site.register(IncentiveDetail)
admin.site.register(AllowanceDetail)
