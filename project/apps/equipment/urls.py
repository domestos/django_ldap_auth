from .views import *
from django.urls import path

urlpatterns = [
    path('', EquipmentView.as_view(), name='equipment_url'),
 
]