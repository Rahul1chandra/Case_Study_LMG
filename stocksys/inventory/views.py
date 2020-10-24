from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse

from inventory.models import Territory, Item, TerritoryItemMap
from django.db.models import Sum

class Login(View):
    """View for login and logout
       input parameter request object .
    """
    def get(self, request):
        if request.GET.get('logoff', None):
            # import ipdb; ipdb.set_trace()
            try:
                logout(request)
                return JsonResponse({"logoff":True})
            except Exception as er:
                # this shouldn't occur 
                return JsonResponse({"logoff":False, "Failure": "Unknown Reason"})
        return render(request, 'login.html', context={})
    
    def post(self, request):
        response = {}
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response["status"] = True
        else:
            response["status"] = False
        return JsonResponse(response)

class Report(View):

    def overallstock(self):
        # Overall Stock: Sum of ALL Warehouse_Stock's + Sum of ALL Store_Stock's + Sum of ALL
        # Transit_Stock's --( No Territory and Item ID filter will be applied)
        
        sum_list = TerritoryItemMap.objects.aggregate(Sum('Store_Stock'), 
        Sum('Transit_Stock'), 
        Sum('Warehouse_Stock')).values() 
        return sum(sum_list)
    
    def totalstock(self, Titem_obj):
        # Total Stock: Sum of Warehouse_Stock’s + Sum of all Store_Stock’s + Sum of all
        # Transit_Stock -- (For seleted Territory and Item ID)
        totalstock_sum = Titem_obj.aggregate(Sum('Store_Stock'), Sum('Transit_Stock'), Sum('Warehouse_Stock')).values()
        return sum(totalstock_sum)

    def warehouseStock(self, Titem_obj):
        # Warehouse Stock: Sum of Warehouse_Stock's (For selected Territory and Item ID)
        warehousestock_sum = Titem_obj.aggregate(Sum('Warehouse_Stock'))
        return sum(warehousestock_sum.values())

    def storestock(self, Titem_obj):
        # Store Stock: Sum of Store_Stock's (For selected Territory and Item ID)
        storestock_sum = Titem_obj.aggregate(Sum('Store_Stock'))
        return sum(storestock_sum.values())

    def pricevalue(self, selected_Territory):
        # Price Value: (Sum of all Warehouse_Stock’s in selected Territory + Sum of all
        # Store_Stock's in selected Territory + Sum of all Transit Stock’s) * Price --( For selected
        # Territory and Item ID)
        #totalstock_sum
        # return sum()
        sum_calculate = 0
        for country in selected_Territory:
            obj = TerritoryItemMap.objects.filter(TerritoryID=country).aggregate(Sum('Warehouse_Stock'), 
            Sum('Store_Stock'),
            Sum('Transit_Stock')
            )
            price_per_territory = TerritoryItemMap.objects.filter(TerritoryID=country)[0].Price
            sum_calculate += sum(obj.values()) * price_per_territory
        return sum_calculate




    def get(self, request):
        territoryobj = Territory.objects.values('Tname', 'TID')
        itemobj = Item.objects.values('item_id', 'Item')
        
        if request.GET.getlist('territorylist[]',None ) and request.GET.getlist('itemlist[]', None):
            Titem_obj = TerritoryItemMap.objects.filter(TerritoryID__in = request.GET.getlist('territorylist[]'),
            ItemID__in = request.GET.getlist('itemlist[]'))
            sum_overall = self.overallstock()
            sum_totalstock = self.totalstock(Titem_obj)
            sum_warehouseStock = self.warehouseStock(Titem_obj)
            sum_storestock = self.storestock(Titem_obj)
            price_value = self.pricevalue(selected_Territory=request.GET.getlist('territorylist[]'))

            return JsonResponse({
                "sum_overall":sum_overall, 
                "sum_totalstock":sum_totalstock, 
                "sum_warehouseStock":sum_warehouseStock,
                "sum_storestock":sum_storestock,
                "price_value":price_value })

        return render(request, 'report.html', context={"territoryobj":territoryobj, "itemobj":itemobj})



def db_initialize():
    from csv import reader
    from inventory.models import Territory, Item, TerritoryItemMap
    from decimal import Decimal
    with open('data.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if csv_reader.line_num == 1:
                pass
            else:
                # import ipdb; ipdb.set_trace()
                # ['ID', 'Territory', 'Warehouse_Stock', 'Store_Stock', 'Transit_Stock', 'Price']
                # ['201117130', 'Spain', '34.0', '20.0', '0.0', '32.49675']
                
                if Territory.objects.filter(Tname= row[1]):
                    pass
                else:
                    Territory.objects.create(Tname = row[1])

                if Item.objects.filter(item_id=row[0]):
                    # print ("duplicate item")
                    pass
                else:
                    Item.objects.create(item_id = row[0])
                ###########
                if Item.objects.filter(item_id = row[0]) and Territory.objects.filter(Tname = row[1]):
                    if TerritoryItemMap.objects.filter(Warehouse_Stock =  int(float(row[2])),  
                    Store_Stock = int(float( row[3])), 
                    Transit_Stock = int(float(row[4])), 
                    Price = float(Decimal(row[5])), 
                    TerritoryID = Territory.objects.get(Tname = row[1]), 
                    ItemID = Item.objects.get(item_id=row[0]) ):
                        # print ("already exits ")
                        pass  
                    else:
                        TerritoryItemMap.objects.create(
                        Warehouse_Stock =  int(float(row[2])),
                        Store_Stock = int(float(row[3])),
                        Transit_Stock =int(float(row[4])),
                        Price = float(Decimal(row[5])),
                        TerritoryID = Territory.objects.get(Tname = row[1]),
                        ItemID = Item.objects.get(item_id = row[0]))
                print (csv_reader.line_num)