from django.contrib import admin
from app.utils.translation import TranslationAdmin
from core.models import FiscalYear, Donor, Activity, BudgetHead, Employee, Party, Account, TaxScheme, BudgetBalance, \
    Language, Currency


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'code')
    list_display_links = ('__unicode__', 'name', 'code')
    search_fields = ('name', 'code')


class PartyAdmin(TranslationAdmin):
    list_display = ('__unicode__', 'address', 'phone_no', 'pan_no')
    list_display_links = ('__unicode__', 'pan_no', 'phone_no')
    search_fields = ('address', 'phone_no', 'pan_no')


class TaxSchemeAdmin(TranslationAdmin):
    list_display = ('name', 'percent')
    search_fields = ('name', 'percent')


admin.site.register(Party, PartyAdmin)
admin.site.register(FiscalYear)
admin.site.register(Currency)
admin.site.register(Donor, TranslationAdmin)
admin.site.register(Activity, TranslationAdmin)
admin.site.register(BudgetHead, TranslationAdmin)
admin.site.register(BudgetBalance)
admin.site.register(Employee, TranslationAdmin)
admin.site.register(Account, TranslationAdmin)
admin.site.register(TaxScheme, TaxSchemeAdmin)
admin.site.register(Language, LanguageAdmin)

