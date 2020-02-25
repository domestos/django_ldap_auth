from rest_framework import serializers
from apps.accounts.models import User 
from apps.equipment.models import  Location, EquipmentType, Equipment

#=================__PERSON__===========================
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields="__all__"
        # fields = (
        #     'id',
        #     'email',
        #     # 'url',
        #     'first_name',
        #     'last_name',
        #     'department',
        #     'when_created',
        #     'when_changed',
        #     'enabled',
        # )
    
#=================__LOCATION__=========================
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            'id',
            'name'
        )

#=================__DIVECE_TYPE__========================
class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = (
            'id',
            'name'
        )


#=================__DIVECE__============================
class EquipmentSerializer(serializers.ModelSerializer):
    user_id= UserSerializers(many=False, read_only=True)
    type_id = EquipmentTypeSerializer(many=False, read_only=True)
    location_id =LocationSerializer(many=False, read_only=True)


    class Meta:
        model = Equipment
        fields = (
            'id',
            'inventory_number',
            'user_id',
            'type_id',
            'location_id'
        )
