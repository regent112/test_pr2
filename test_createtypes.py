import requests
import os
import json
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_pr2.settings")
django.setup()
from main.models import EquipmentType, Equipment


if __name__ == '__main__':
    EquipmentType.objects.all().delete()
    EquipmentType.objects.create(
        name='TP-Link',
        mask='AaNZX'
    )
    EquipmentType.objects.create(
        name='D-Link',
        mask='XZNaA'
    )
    resp = requests.post(
        'http://127.0.0.1:8080/api/equipment',
        data={
            'equipments': json.dumps([
                {
                    # fail
                    'serial_number': 'FtD-R',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # pass
                    'serial_number': 'Ft7_5',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # pass
                    'serial_number': 'Ft7-R',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # fail
                    'serial_number': 'ft7-R',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # fail
                    'serial_number': 'FT7-R',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # fail
                    'serial_number': 'FtD-R',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # fail
                    'serial_number': 'Ft70R',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # fail
                    'serial_number': 'Ft7-_',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # fail
                    'serial_number': 'Ft7-R',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # pass
                    'serial_number': 'R-7tF',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                }
            ])
        }
    )
    r_json = resp.json()
    print(
        r_json[0].get('status') == 'FAIL',
        r_json[1].get('status') is None,
        r_json[2].get('status') is None,
        r_json[3].get('status') == 'FAIL',
        r_json[4].get('status') == 'FAIL',
        r_json[5].get('status') == 'FAIL',
        r_json[6].get('status') == 'FAIL',
        r_json[7].get('status') == 'FAIL',
        r_json[8].get('status') == 'FAIL',
        r_json[9].get('status') is None
    )
    resp = requests.post(
        'http://127.0.0.1:8080/api/equipment',
        data={
            'equipments': json.dumps([
                {
                    # fail
                    'serial_number': 'R-7tF',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # pass
                    'serial_number': '0@7tF',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # fail
                    'serial_number': '_-7tF',
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
            ])
        }
    )
    r_json = resp.json()
    print(
        r_json[0].get('status') == 'FAIL',
        r_json[1].get('status') is None,
        r_json[2].get('status') == 'FAIL'
    )
    EquipmentType.objects.create(
        name='D-Big',
        mask=(
            'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
            'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
            'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
            'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
            'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
        )
    )
    resp = requests.post(
        'http://127.0.0.1:8080/api/equipment',
        data={
            'equipments': json.dumps([
                {
                    # pass
                    'serial_number': (
                        '555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '5555555555555555555555555555555555555'
                    ),
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                },
                {
                    # pass
                    'serial_number': (
                        '655555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                        '55555555555555555555555555555555555556'
                    ),
                    'note': 's,lerkjhglse tnhlst rnhlsetn h'
                }
            ])
        }
    )
    r_json = resp.json()
    print(
        r_json[0].get('status') is None,
        r_json[1].get('status') == 'FAIL'
    )
    e_id = r_json[0]['id']
    resp = requests.put(
        f'http://127.0.0.1:8080/api/equipment/{e_id}',
        data={
            'note': 'test 555'
        }
    )
    r_json = resp.json()
    print(r_json['note'] == 'test 555')
    resp = requests.put(
        f'http://127.0.0.1:8080/api/equipment/{e_id}',
        data={
            'serial_number': '555'
        }
    )
    r_json = resp.json()
    print(r_json['status'] == 'FAIL')
    resp = requests.put(
        f'http://127.0.0.1:8080/api/equipment/{e_id}',
        data={
            'serial_number': (
                '555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                '5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                '5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                '555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                '55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
                '5555555555555555555555555555555555556'
            ),
            'note': 'test 556'
        }
    )
    r_json = resp.json()
    print(
        r_json['note'] == 'test 556',
        r_json['serial_number'] == (
            '555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
            '5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
            '5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
            '555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
            '55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555'
            '5555555555555555555555555555555555556'
        ),
    )
    resp = requests.put(
        f'http://127.0.0.1:8080/api/equipment/{e_id}',
        data={
            'serial_number': '0@7tG',
            'note': 'test 557'
        }
    )
    r_json = resp.json()
    print(
        r_json['note'] == 'test 557',
        r_json['equipmenttype']['name'] == 'D-Link'
    )
    resp = requests.delete(
        f'http://127.0.0.1:8080/api/equipment/{e_id}',
    )
    r_json = resp.json()
    print(
        r_json['status'] == 'OK',
        not Equipment.objects.filter(id__exact=e_id).exists()
    )

    # print(resp.text)
