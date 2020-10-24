from django.db import models

class Territory(models.Model):
    Tname = models.CharField(max_length=30)
    TID =  models.AutoField(primary_key=True)

    def __str__(self):
        return '{} Territory'.format(self.Tname)

class Item(models.Model):
    item_id = models.CharField(max_length=30) 
    Item = models.AutoField(primary_key=True)

    def __str__(self):
        return '{} Item id'.format(self.item_id)

class TerritoryItemMap(models.Model):
    Warehouse_Stock = models.IntegerField(blank=True, null=True)
    Store_Stock = models.IntegerField(blank=True, null=True)
    Transit_Stock = models.IntegerField(blank=True, null=True)
    Price = models.FloatField()
    TerritoryID = models.ForeignKey(Territory, on_delete=models.PROTECT)
    ItemID = models.ForeignKey(Item, on_delete=models.PROTECT)

    def __str__(self):
        return '{} - Mapping - {}'.format(self.TerritoryID.Tname, self.ItemID.item_id)