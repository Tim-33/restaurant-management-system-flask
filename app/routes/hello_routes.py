from flask import Blueprint, render_template, Flask
from app.interfaces.iroutes import IRoutes
from app.utils.api_utils import build_api_route
from app.router.api_routes import HelloApiRoutesEnum
from app.router.routes import HelloRoutesEnum
from app.utils.api_utils import make_api_request, ApiMethodsEnum
    
class HelloRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.hello_routes_bp = Blueprint('hello_routes', __name__)
        self.base_url = self.app.config['API_BASE_URL']
        self.port = self.app.config['API_PORT']
        
    def register_routes(self):
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO.value, methods=["GET"])(self.get_hellos)
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO_ID.value, methods=["GET"])(self.get_hello)
        self.app.register_blueprint(self.hello_routes_bp)
        
    def get_hellos(self):
        url = build_api_route(self.base_url, self.port, HelloApiRoutesEnum.HELLO.value)
        headers = {"Content-type": "application/json"}
        data = make_api_request(url, headers, self.app, ApiMethodsEnum.GET)
        return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO.value), data=data)
    
    def get_hello(self, id):
        url = build_api_route(self.base_url, self.port, HelloApiRoutesEnum.HELLO_ID.value)
        headers = {"Content-type": "application/json"}
        data = make_api_request(url, headers, self.app, ApiMethodsEnum.GET)
        return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO_ID.value), data=data)
    