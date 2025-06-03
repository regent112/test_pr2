import cherrypy
import json
from typing import Any, Callable, Dict, List
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
    def GET(self, page=1, count=20, serial_number='', note='') -> List[Dict[str, Any]]:
        return controllers.list_equipments(page=int(page), count=int(count), serial_number=serial_number, note=note)

    @_get_bytes
    def POST(self, equipments: str) -> List[Dict[str, Any]]:
        return controllers.create_equipments(json.loads(equipments))


if __name__ == '__main__':
    conf = {
        '/equipment': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
    }
    api = Api()
    api.equipment = Equipments()
    cherrypy.quickstart(api, '/api/', conf)
