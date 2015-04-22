from django.contrib import admin
from models import Item, InventoryAccount, Demand, Inspection, InspectionRow, YearlyReport, YearlyReportRow

admin.site.register(Item)
admin.site.register(InventoryAccount)
admin.site.register(Demand)
admin.site.register(Inspection)
admin.site.register(InspectionRow)
admin.site.register(YearlyReport)
admin.site.register(YearlyReportRow)