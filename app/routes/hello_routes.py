import requests
from flask import Blueprint, render_template, Flask
from app.interfaces.iroutes import IRoutes
from app.utils.api_utils import build_api_route
from enum import Enum
from app.modules.hello.enums.hello_routes import HelloRoutesEnum

class HelloRoutesRoutesEnum(Enum):
    HELLO = "/hello"
    
class HelloRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.hello_routes_bp = Blueprint('hello_routes', __name__)
        self.base_url = self.app.config['API_BASE_URL']
        self.port = self.app.config['API_PORT']
        
    def register_routes(self):
        self.hello_routes_bp.route(HelloRoutesRoutesEnum.HELLO.value, methods=["GET"])(self.get_hello)

    def get_hello(self):
        response = requests.get(build_api_route(self.base_url, self.port, HelloRoutesEnum.HELLO.value))
        data = response.json()

        return render_template(self.app.router.get_template(HelloRoutesRoutesEnum.HELLO.value), data=data)