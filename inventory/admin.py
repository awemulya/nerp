from django.contrib import admin
from models import Item, InventoryAccount, EntryReportRow, Demand, Inspection, DemandRow, InspectionRow, YearlyReport, YearlyReportRow, \
    ItemLocation, ItemInstance, Release, Transaction, JournalEntry


class DemandRowAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'unit', 'status', 'location')
    list_display_links = ('item',)
    list_filter = ('status', 'unit', 'location')
    search_fields = ('item', 'location')


class DemandAdmin(admin.ModelAdmin):
    list_display = ('release_no', 'fiscal_year', 'demandee', 'date')
    list_display_links = ('release_no',)
    list_filter = ('fiscal_year', 'demandee')


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
admin.site.register(InventoryAccount, InventoryAccountAdmin)
admin.site.register(Demand, DemandAdmin)
admin.site.register(DemandRow, DemandRowAdmin)
admin.site.register(ItemLocation, ItemLocationAdmin)
admin.site.register(ItemInstance, ItemInstanceAdmin)
admin.site.register(Inspection)
admin.site.register(InspectionRow)
admin.site.register(YearlyReport)
admin.site.register(YearlyReportRow)
admin.site.register(Release)
admin.site.register(EntryReportRow)
admin.site.register(Transaction)
admin.site.register(JournalEntry)
admin.site.register(PartyQuotation)
admin.site.register(QuotationComparison)
admin.site.register(QuotationComparisonRow)

