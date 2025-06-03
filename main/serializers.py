from main.models import EquipmentType, Equipment
from rest_framework import serializers


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    equipmenttype = EquipmentTypeSerializer()

    class Meta:
        model = Equipment
        fields = '__all__'
