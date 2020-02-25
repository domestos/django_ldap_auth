from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import DeviceFilter

from apps.inventory.models import Person, Location, TypeDevice, Device
from .serializers import PersonSerializers, LocationSerializer, TypeDeviceSerializer, DiveceSerializer

#=================__PERSON__===========================
class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializers

#=================__LOCATION__=========================
class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

#=================__DIVECE_TYPE__========================
class TypeDeviceViewSet(ModelViewSet):
    queryset = TypeDevice.objects.all()
    serializer_class = TypeDeviceSerializer

#=================__DIVECE__============================
class DiveceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DiveceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['inventory_number', 'person_id__fname']
    filter_class = DeviceFilter
       
   
    
    # filter_backends = [DjangoFilterBackend,
    #                    filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['inventory_number', 'person_id__fname']
   
    # search_fields = ['inventory_number', 'person_id__fname' ]
    # ordering_fields = ['inventory_number', '=person_id__fname']
    # ordering = ['person_id__fname']
