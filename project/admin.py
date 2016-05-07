from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from .models import ImprestTransaction, ExpenditureCategory, Expenditure


class ExpenditureCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


class ExpenditureAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(ImprestTransaction)
admin.site.register(ExpenditureCategory, ExpenditureCategoryAdmin)
admin.site.register(Expenditure, ExpenditureAdmin)
