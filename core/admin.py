from django.contrib import admin
from app.utils.translation import TranslationAdmin
from core.models import FiscalYear, Donor, Activity, BudgetHead, Employee, Party, Account, TaxScheme, BudgetBalance, \
    Language

admin.site.register(Party, TranslationAdmin)
admin.site.register(FiscalYear)
admin.site.register(Donor, TranslationAdmin)
admin.site.register(Activity, TranslationAdmin)
admin.site.register(BudgetHead, TranslationAdmin)
admin.site.register(BudgetBalance)
admin.site.register(Employee, TranslationAdmin)
admin.site.register(Account, TranslationAdmin)
admin.site.register(TaxScheme, TranslationAdmin)
admin.site.register(Language)
