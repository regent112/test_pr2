from django.core.exceptions import ValidationError
from main.models import EquipmentType, Equipment
from main.serializers import EquipmentSerializer, EquipmentTypeSerializer
import re
from typing import Any, Dict, Final, List, Optional


def _validate_mask(mask: str, serial_number: str) -> bool:
    """
    валидация серийного номера по указанной маске
    """
    re_mask_list: List[str] = []
    d_mask: Final = {
        'N': r'[0-9]',
        'A': r'[A-Z]',
        'a': r'[a-z]',
        'X': r'[A-Z0-9]',
        'Z': r'[\-_@]'
    }
    for char in mask:
        re_mask_list.append(d_mask[char])
    return bool(re.fullmatch(''.join(re_mask_list), serial_number))


def _get_equipmenttypeid_via_serialnumber(serial_number: str) -> int:
    """
    получение ID типа устройства по серийному номеру
    """
    mask: str
    type_id: int
    for mask, type_id in list(
            EquipmentType.objects.values_list('mask', 'id')
    ):
        if _validate_mask(mask, serial_number):
            return type_id
    raise ValidationError('Invalid serial number=%(value)s', params={'value': serial_number})


def list_equipments(page=1, count=20, serial_number='', note='') -> List[Dict[str, Any]]:
    """
    список устройств
    """
    offset = count * (page - 1)
    query = Equipment.objects.select_related('equipmenttype')[offset: offset + count]
    if serial_number:
        query = query.filter(
            serial_number__contains=serial_number
        )
    if note:
        query = query.filter(
            note__icontains=note
        )
    return EquipmentSerializer(query).data


def get_equipment(equipment_id: int) -> Dict[str, Any]:
    """
    информация об устройстве
    """
    return EquipmentSerializer(
        Equipment.objects.select_related('equipmenttype').get(
            id__exact=equipment_id
        )
    ).data


def create_equipment(serial_number: str, note: str) -> Dict[str, Any]:
    """
    создание устройства
    """
    equipmenttype_id = _get_equipmenttypeid_via_serialnumber(serial_number)
    equipment = Equipment.objects.create(
        serial_number=serial_number,
        note=note,
        equipmenttype_id=equipmenttype_id
    )
    return EquipmentSerializer(equipment).data


def change_equipment(
    equipment_id: int, serial_number: Optional[str] = None, note: Optional[str] = None
) -> Dict[str, Any]:
    """
    изменение данных об устройстве
    """
    equipment: Equipment = Equipment.objects.get(id__exact=equipment_id)
    update_fields: List[str] = []
    if serial_number is not None and equipment.serial_number != serial_number:
        equipmenttype_id = _get_equipmenttypeid_via_serialnumber(serial_number)
        equipment.serial_number = serial_number
        update_fields.append('serial_number')
        if equipment.equipmenttype_id != equipmenttype_id:
            equipment.equipmenttype_id = equipmenttype_id
            update_fields.append('equipmenttype_id')
    if note is not None and equipment.note != note:
        equipment.note = note
        update_fields.append('note')
    if update_fields:
        equipment.save(update_fields=update_fields)
    return EquipmentSerializer(equipment).data


def delete_equipment(equipment_id: int) -> None:
    """
    удаление устройства
    """
    Equipment.objects.filter(id__exact=equipment_id).delete()


def list_equipmenttypes(page=1, count=20, mask='', name='') -> List[Dict[str, Any]]:
    """
    список типов устройств
    """
    offset = count * (page - 1)
    query = EquipmentType.objects.all()[offset: offset + count]
    if mask:
        query = query.filter(
            mask__contains=mask
        )
    if name:
        query = query.filter(
            name__icontains=name
        )
    return EquipmentTypeSerializer(query).data
