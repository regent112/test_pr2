from django.db import models
from typing import Any


class EquipmentType(models.Model):
    """
    таблица типов устройств
    """
    id: int
    objects: Any
    name: str = models.CharField(max_length=500)
    mask: str = models.CharField(max_length=500)


class Equipment(models.Model):
    """
    таблица устройств
    """
    id: int
    objects: Any
    equipmenttype: EquipmentType = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, related_name='equipments')
    equipmenttype_id: int
    serial_number: str = models.CharField(max_length=500)
    note: str = models.TextField()

    class Meta:
        unique_together = ('equipmenttype', 'serial_number')
