from django.contrib import admin

# Register your models here.

from .models import Item, Territory, TerritoryItemMap
admin.site.register(Item)
admin.site.register(Territory)
admin.site.register(TerritoryItemMap)