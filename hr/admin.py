from django.contrib import admin
from .models import EmployeeAccount, EmployeeGrade, Employee, Designation, Incentive, Allowance, TaxScheme, BranchOffice, Deduction, ProTempore, PaymentRecord, PayrollEntry, IncentiveName, AllowanceName, DeductionDetail, IncentiveDetail, AllowanceDetail, MaritalStatus
from .forms import EmployeeAccountInlineFormset, AllowanceForm, IncentiveForm, DeductionForm, EmployeeForm, IncentiveInlineFormset


class EmployeeAccountInline(admin.TabularInline):
    model = EmployeeAccount
    formset = EmployeeAccountInlineFormset
    extra = 1


class EmployeeIncentiveInline(admin.TabularInline):
    model = Incentive
    formset = IncentiveInlineFormset
    extra = 1


class EmployeeAdmin(admin.ModelAdmin):
    inlines = (EmployeeAccountInline, EmployeeIncentiveInline)
    form = EmployeeForm
    pass


class AllowanceAdmin(admin.ModelAdmin):
    form = AllowanceForm


class IncentiveAdmin(admin.ModelAdmin):
    form = IncentiveForm


class DeductionAdmin(admin.ModelAdmin):
    form = DeductionForm


# class AccountAdmin(admin.ModelAdmin):
#     inlines = (EmployeeAccountInline,)



# class AccountInline(admin.TabularInline):
#     model = EmployeeAccount.account.through


# class EmployeeInline(admin.TabularInline):
#     model = EmployeeAccount.employee.through


# class EmployeeAccountAdmin(admin.ModelAdmin):
#     pass


# admin.site.register(AccountType)
# admin.site.register(Account)
# admin.site.register(Transaction)

admin.site.register(EmployeeGrade)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Designation)
admin.site.register(Incentive, IncentiveAdmin)
admin.site.register(Allowance, AllowanceAdmin)
admin.site.register(TaxScheme)
admin.site.register(BranchOffice)
admin.site.register(Deduction, DeductionAdmin)
admin.site.register(ProTempore)
admin.site.register(PaymentRecord)
admin.site.register(PayrollEntry)
admin.site.register(EmployeeAccount)
admin.site.register(IncentiveName)
admin.site.register(AllowanceName)

admin.site.register(DeductionDetail)
admin.site.register(IncentiveDetail)
admin.site.register(AllowanceDetail)

# admin.site.register(AllowanceAccount)
# admin.site.register(IncentiveAccount)
# admin.site.register(DeductionAccount)
# admin.site.register(JournalEntry)
# admin.site.register(CompanyAccount)
admin.site.register(MaritalStatus)
# admin.site.register(SalaryAccount)
