from django.contrib import admin
from core.models import FiscalYear, Donor, Activity, BudgetHead, Employee, Party, Account, TaxScheme, BudgetBalance, \
    Language

admin.site.register(FiscalYear)
admin.site.register(Donor)
admin.site.register(Activity)
admin.site.register(BudgetHead)
admin.site.register(BudgetBalance)
admin.site.register(Employee)
admin.site.register(Party)
admin.site.register(Account)
admin.site.register(TaxScheme)
admin.site.register(Language)
