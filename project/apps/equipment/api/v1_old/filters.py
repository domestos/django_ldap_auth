import django_filters
from apps.inventory.models import Person, Location, TypeDevice, Device

class DeviceFilter(django_filters.FilterSet):
    class Meta:
        model = Device
        fields = {
            'inventory_number':['icontains'],
            'person_id__fname': ['icontains'],
        }
       
