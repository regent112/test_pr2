import cherrypy
import json
from typing import Any, Callable, Dict, List, Optional, Union
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_pr2.settings")
django.setup()
from main import controllers


class Api(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"


def _get_bytes(f: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> bytes:
        return json.dumps(f(*args, **kwargs)).encode('utf-8')
    return wrapper


@cherrypy.expose
class Equipments(object):
    @_get_bytes
    def GET(self, equipment_id=None, page=1, count=20, serial_number='', note='') -> Union[
        List[Dict[str, Any]], Dict[str, Any]
    ]:
        if equipment_id is None:
            return controllers.list_equipments(page=int(page), count=int(count), serial_number=serial_number, note=note)
        else:
            return controllers.get_equipment(int(equipment_id))

    @_get_bytes
    def POST(self, equipments: str) -> List[Dict[str, Any]]:
        return controllers.create_equipments(json.loads(equipments))

    @_get_bytes
    def PUT(self, equipment_id: str, serial_number: Optional[str] = None, note: Optional[str] = None) -> Dict[str, Any]:
        return controllers.change_equipment(int(equipment_id), serial_number, note)

    @_get_bytes
    def DELETE(self, equipment_id: str) -> Dict[str, Any]:
        return controllers.delete_equipment(int(equipment_id))


@cherrypy.expose
class EquipmentTypes(object):
    @_get_bytes
    def GET(self, page=1, count=20, mask='', name='') -> List[Dict[str, Any]]:
        return controllers.list_equipmenttypes(page=int(page), count=int(count), mask=mask, name=name)


if __name__ == '__main__':
    conf = {
        '/equipment': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
        '/equipment-type': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
            'controllers': EquipmentTypes()
        },
    }
    api = Api()
    api.equipment = Equipments()
    api.__setattr__('equipment-type', EquipmentTypes())
    cherrypy.quickstart(api, '/api/', conf)
