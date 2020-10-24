from django.urls import path
from inventory.views import Login, Report

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('report', Report.as_view(), name='report'),
    
]