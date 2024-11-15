import requests
from flask import Blueprint, render_template, Flask
from app.interfaces.iroutes import IRoutes
from app.utils.api_utils import build_api_route
from app.router.api_routes import HelloApiRoutesEnum
from app.router.routes import HelloRoutesEnum
    
class HelloRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.hello_routes_bp = Blueprint('hello_routes', __name__)
        self.base_url = self.app.config['API_BASE_URL']
        self.port = self.app.config['API_PORT']
        
    def register_routes(self):
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO.value, methods=["GET"])(self.get_hello)
        self.app.register_blueprint(self.hello_routes_bp)
        
    def get_hello(self):
        url = build_api_route(self.base_url, self.port, HelloApiRoutesEnum.HELLO.value)
        headers = {"Content-type": "application/json"}
        self.app.logger.info(f"Sending request to {url} with headers {headers}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json() 
        return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO.value), data=data)
    