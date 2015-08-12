from django.contrib import admin
from models import Item, InventoryAccount, Demand, Inspection, DemandRow, InspectionRow, YearlyReport, YearlyReportRow, \
    ItemLocation, ItemInstance, Release, PartyQuotation, QuotationComparison, QuotationComparisonRow

admin.site.register(Item)
admin.site.register(InventoryAccount)
admin.site.register(Demand)
admin.site.register(DemandRow)
admin.site.register(ItemLocation)
admin.site.register(ItemInstance)
admin.site.register(Inspection)
admin.site.register(InspectionRow)
admin.site.register(YearlyReport)
admin.site.register(YearlyReportRow)
admin.site.register(Release)
admin.site.register(PartyQuotation)
admin.site.register(QuotationComparison)
admin.site.register(QuotationComparisonRow)



