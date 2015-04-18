from django.contrib import admin
from models import Item, InventoryAccount, Demand, DemandRow, ItemLocation, TrackItem

admin.site.register(Item)
admin.site.register(InventoryAccount)
admin.site.register(Demand)
admin.site.register(DemandRow)
admin.site.register(ItemLocation)
admin.site.register(TrackItem)