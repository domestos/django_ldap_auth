from rest_framework import serializers
from apps.accounts.models import User 
from apps.equipment.models import  Location, EquipmentType, Equipment
from django.core.serializers.json import Serializer

#=================__PERSON__===========================

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        print(dir(model))
        # fields="__all__"
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'department',
            'when_created',
            'when_changed',
            'enabled',
        )
        def create(self, validated_data):
            """Nested serializer need to over-ride the create fn to work"""
            user = User.objects.create( **validated_data)
            user.set_password(validated_data.get("password"))
            user.save()
            return user
        
    

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
    user= UserSerializers(many=False, read_only=True)
    device_type = EquipmentTypeSerializer(many=False, read_only=True)
    location =LocationSerializer(many=False, read_only=True)


    class Meta:
        model = Equipment
        fields = ( "__all__"
            # 'id',
            # 'date_of_purchase',
            # 'inventory_number',
            # 'user',
            # 'device_type',
            # 'location'
        )



#=================__DIVECE__============================
class EquipmentSerializer2(serializers.HyperlinkedModelSerializer):
    # user= UserSerializers(many=False, read_only=True)
    # device_type = EquipmentTypeSerializer(many=False, read_only=True)
    # location =LocationSerializer(many=False, read_only=True)
    

    class Meta:
        model = Equipment
        fields = ( "__all__"
            # 'id',
            # 'date_of_purchase',
            # 'inventory_number',
            # 'user',
            # 'device_type',
            # 'location'
        )


#=================__DIVECE__============================
class EquipmentSerializer3(serializers.HyperlinkedModelSerializer):
    user= UserSerializers(many=False, read_only=True)
    device_type = EquipmentTypeSerializer(many=False, read_only=True)
    location =LocationSerializer(many=False, read_only=True)


    class Meta:
        model = Equipment
        fields = ( "__all__"
            # 'id',
            # 'date_of_purchase',
            # 'inventory_number',
            # 'user',
            # 'device_type',
            # 'location'
        )