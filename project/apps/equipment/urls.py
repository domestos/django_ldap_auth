from .views import *
from django.urls import path

urlpatterns = [
    path('', EquipmentView.as_view(), name='equipment_url'),
    path('new', NewEquipmentView.as_view(), name='new_equipment_url'),
    path('update/<int:pk>', UpdateEquipmentView.as_view(), name='update_equipment_url'),
    path('equipment_action', equipment_action, name='equipment_action_url'),
    path('update/<int:e_pk>/history/<int:h_pk>/delete', DeleteEquipmentHistory.as_view(), name='delete_equipment_url'),

    
]