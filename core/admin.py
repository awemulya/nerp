from django.contrib import admin
from solo.admin import SingletonModelAdmin
from app.utils.translation import TranslationAdmin
from core.models import FiscalYear, Donor, Activity, BudgetHead, Employee, TaxScheme, BudgetBalance, \
    Language, Currency, AppSetting


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'code')
    list_display_links = ('__unicode__', 'name', 'code')
    search_fields = ('name', 'code')


class TaxSchemeAdmin(TranslationAdmin):
    list_display = ('name', 'percent')
    search_fields = ('name', 'percent')


admin.site.register(FiscalYear)
admin.site.register(Currency)
admin.site.register(Donor, TranslationAdmin)
admin.site.register(Activity, TranslationAdmin)
admin.site.register(BudgetHead, TranslationAdmin)
admin.site.register(BudgetBalance)
admin.site.register(Employee, TranslationAdmin)
admin.site.register(TaxScheme, TaxSchemeAdmin)
admin.site.register(Language, LanguageAdmin)



admin.site.register(AppSetting, SingletonModelAdmin)

