from flask import Blueprint, jsonify, Flask
from app.modules.hello.hello_service import HelloService
from app.utils.decorators import log_request
from app.utils.api_utils import generate_api_route
from app.modules.hello.enums.hello_routes import HelloRoutesEnum
from app.interfaces.icontroller import IController

class HelloController(IController):
    def __init__(self, app: Flask):
        self.app = app
        self.hello_bp = Blueprint('hello', __name__)
        self.hello_service = HelloService(self.app.db)
        
    def register_routes(self):
        self.hello_bp.route(generate_api_route(HelloRoutesEnum.HELLO.value), methods=["GET"])(self.get_hello)
        self.app.register_blueprint(self.hello_bp)
    
    @log_request
    def get_hello(self):
        message = self.hello_service.get_hello_message()
        return jsonify(message)