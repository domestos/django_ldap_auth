from rest_framework import serializers
from apps.equipment.models import Person, Location, EquipmentType, Device

#=================__PERSON__===========================
class PersonSerializers(serializers.Serializer):  
    fname = serializers.CharField(max_length=50)
    sname = serializers.CharField()
    
    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fname = validated_data.get('fname', instance.fname)
        instance.sname = validated_data.get('sname', instance.sname)
        instance.save()
        return instance

#=================__LOCATION__=========================
class LocationSerializer(serializers.Serializer):
    location = serializers.CharField()
    
    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self,  instance, validated_data):
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance

#=================__DIVECE_TYPE__========================
class TypeDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = (
            'id',
            'name'
        )


#=================__DIVECE__============================
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'id',
            'inventory_number',
            'person_id',
            'type_id',
            'location_id'
        )
