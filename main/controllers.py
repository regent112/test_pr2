from django.db import IntegrityError
from main.models import EquipmentType, Equipment
from main.serializers import EquipmentSerializer, EquipmentTypeSerializer
import re
from typing import Any, Dict, Final, List, Optional, Tuple, Iterable


def _get_equipmenttypeids_via_serialnumber(serial_numbers: Iterable[str]) -> List[int]:
    """
    получение ID типа устройства по серийному номеру
    """
    types: List[Tuple[str, int]] = list(
        EquipmentType.objects.values_list('mask', 'id')
    )
    d_mask: Final = {
        'N': r'[0-9]',
        'A': r'[A-Z]',
        'a': r'[a-z]',
        'X': r'[A-Z0-9]',
        'Z': r'[\-_@]'
    }
    for index in range(len(types)):
        re_mask_list: List[str] = []
        for char in types[index][0]:
            re_mask_list.append(d_mask[char])
        types[index] = (''.join(re_mask_list), types[index][1])
    list_ids: List[int] = []
    for serial_number in serial_numbers:
        is_find = False
        for mask, type_id in types:
            if bool(re.fullmatch(mask, serial_number)):
                list_ids.append(type_id)
                is_find = True
                break
        if not is_find:
            list_ids.append(0)
    return list_ids


def list_equipments(page=1, count=20, serial_number='', note='') -> List[Dict[str, Any]]:
    """
    список устройств
    """
    offset = count * (page - 1)
    query = Equipment.objects.select_related('equipmenttype')
    if serial_number:
        query = query.filter(
            serial_number__contains=serial_number
        )
    if note:
        query = query.filter(
            note__icontains=note
        )
    return EquipmentSerializer(list(query[offset: offset + count]), many=True).data


def get_equipment(equipment_id: int) -> Dict[str, Any]:
    """
    информация об устройстве
    """
    return EquipmentSerializer(
        Equipment.objects.select_related('equipmenttype').get(
            id__exact=equipment_id
        )
    ).data


def create_equipments(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    создание устройства
    """
    list_ids = _get_equipmenttypeids_via_serialnumber(map(lambda el: el['serial_number'], data))
    list_res: List[Dict[str, Any]] = []
    for data, equipmenttype_id in zip(data, list_ids):
        serial_number = data['serial_number']
        if not equipmenttype_id:
            list_res.append({
                'status': 'FAIL',
                'message': f'Invalid serial_number = "{serial_number}"'
            })
            continue
        try:
            equipment = Equipment.objects.create(
                serial_number=serial_number,
                note=data['note'],
                equipmenttype_id=equipmenttype_id
            )
            list_res.append(EquipmentSerializer(equipment).data)
        except IntegrityError:
            list_res.append({
                'status': 'FAIL',
                'message': f'Device exists. Serial_number = "{serial_number}"'
            })
    return list_res


def change_equipment(
    equipment_id: int, serial_number: Optional[str] = None, note: Optional[str] = None
) -> Dict[str, Any]:
    """
    изменение данных об устройстве
    """
    equipment: Equipment = Equipment.objects.get(id__exact=equipment_id)
    update_fields: List[str] = []
    if serial_number is not None and equipment.serial_number != serial_number:
        equipmenttype_id = _get_equipmenttypeids_via_serialnumber([serial_number])[0]
        if not equipmenttype_id:
            return {
                'status': 'FAIL',
                'message': f'Invalid serial_number = "{serial_number}"'
            }
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


def delete_equipment(equipment_id: int) -> Dict[str, Any]:
    """
    удаление устройства
    """
    Equipment.objects.filter(id__exact=equipment_id).delete()
    return {'status': 'OK', 'message': f'Equipment {equipment_id} deleted'}


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
