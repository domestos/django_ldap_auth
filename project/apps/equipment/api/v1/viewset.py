from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# from .filters import DeviceFilter
from apps.accounts.models import User as Profile
from apps.equipment.models import Location, EquipmentType, Equipment
from .serializers import UserSerializers, LocationSerializer, EquipmentTypeSerializer, EquipmentSerializer

#=================__PERSON__===========================
class UserViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    for q in queryset:
        print(q.username)
    serializer_class = UserSerializers

#=================__LOCATION__=========================
class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

#=================__DIVECE_TYPE__========================
class EquipmentTypeViewSet(ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer

#=================__DIVECE__============================
class EquipmentViewSet(ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['inventory_number', 'person_id__fname']
    # filter_class = DeviceFilter
       
   
    
    # filter_backends = [DjangoFilterBackend,
    #                    filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['inventory_number', 'person_id__fname']
   
    # search_fields = ['inventory_number', 'person_id__fname' ]
    # ordering_fields = ['inventory_number', '=person_id__fname']
    # ordering = ['person_id__fname']
