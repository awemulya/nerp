from django.contrib import admin
from models import Item, InventoryAccount, EntryReport, EntryReportRow, Demand, Inspection, DemandRow, InspectionRow, YearlyReport, YearlyReportRow, \
    ItemLocation, ItemInstance, PartyQuotation, Release, Transaction, JournalEntry, QuotationComparison ,QuotationComparisonRow, PurchaseOrder, PurchaseOrderRow, Depreciation


class DemandRowInline(admin.TabularInline):
    model = DemandRow


class ReleaseInline(admin.TabularInline):
    model = Release


class DemandRowAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'unit', 'status', 'location')
    list_display_links = ('item',)
    list_filter = ('status', 'unit', 'location')
    search_fields = ('item', 'location')


class DemandAdmin(admin.ModelAdmin):
    list_display = ('release_no', 'fiscal_year', 'demandee', 'date')
    list_display_links = ('release_no',)
    list_filter = ('fiscal_year', 'demandee')
    inlines = [
        DemandRowInline,
    ]


class PurchaseOrderRowInline(admin.TabularInline):
    model = PurchaseOrderRow


class PurchaseOrderRowAdmin(admin.ModelAdmin):
    list_display = ('budget_title_no', 'item', 'quantity', 'unit',
        'rate', 'vattable',
        'remarks')
    search_fields = ('item',)


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'party', 'date', 'due_days', 'fiscal_year')
    inlines = [
        PurchaseOrderRowInline,
    ]


class EntryReportRowInline(admin.TabularInline):
    model = EntryReportRow


class EntryReportRowAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'unit', 'rate', 'other_expenses', 'remarks')
    list_display_links = ('item',)
    search_fields = ('item',)


class EntryReportAdmin(admin.ModelAdmin):
    list_display = ('entry_report_no', 'fiscal_year')
    inlines = [
        EntryReportRowInline,
    ]


class InspectionRowInline(admin.TabularInline):
    model = InspectionRow


class InspectionRowAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'rate', 'price',
        'matched_number', 'unmatched_number',
        'decrement', 'increment', 'good', 'bad',
        'remarks')
    list_display_links = ('item_name',)
    search_fields = ('item',)


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('report_no', 'fiscal_year')
    inlines = [
        InspectionRowInline,
    ]


class YearlyReportRowInline(admin.TabularInline):
    model = YearlyReportRow


class YearlyReportRowAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'account_no', 'income', 'expense',
        'remaining', 'remarks')
    list_display_links = ('item_name',)
    search_fields = ('item_name',)


class YearlyReportAdmin(admin.ModelAdmin):
    list_display = ('report_no', 'fiscal_year')
    inlines = [
        YearlyReportRowInline,
    ]


class QuotationComparisonRowInline(admin.TabularInline):
    model = QuotationComparisonRow


class PartyQuotationInline(admin.TabularInline):
    model = PartyQuotation


class QuotationComparisonRowAdmin(admin.ModelAdmin):
    inlines = [
        PartyQuotationInline,
    ]


class QuotationComparisonAdmin(admin.ModelAdmin):
    inlines = [
        QuotationComparisonRowInline,
    ]



class InventoryAccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'account_no', 'current_balance')
    list_display_links = ('code', 'name', 'account_no')
    search_fields = ('code', 'name', 'account_no')


class ItemInstanceAdmin(admin.ModelAdmin):
    list_display = ('item', 'item_rate', 'location')
    list_display_links = ('item',)
    list_filter = ('location',)
    search_fields = ('item', 'item_rate', 'location')


class ItemLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'remarks')
    search_fields = ('name',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', '__unicode__', 'unit', 'type')
    list_display_links = ('code', '__unicode__',)
    list_filter = ('type', 'unit')
    search_fields = ('code', 'name',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Depreciation)
admin.site.register(InventoryAccount, InventoryAccountAdmin)
admin.site.register(Demand, DemandAdmin)
admin.site.register(DemandRow, DemandRowAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderRow, PurchaseOrderRowAdmin)
admin.site.register(EntryReport, EntryReportAdmin)
admin.site.register(EntryReportRow, EntryReportRowAdmin)
admin.site.register(ItemLocation, ItemLocationAdmin)
admin.site.register(ItemInstance, ItemInstanceAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(InspectionRow, InspectionRowAdmin)
admin.site.register(YearlyReport, YearlyReportAdmin)
admin.site.register(YearlyReportRow, YearlyReportRowAdmin)
admin.site.register(Release)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(QuotationComparison, QuotationComparisonAdmin)
admin.site.register(QuotationComparisonRow, QuotationComparisonRowAdmin)

