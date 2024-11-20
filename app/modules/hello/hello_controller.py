from flask import Blueprint, jsonify, Flask
from app.modules.hello.hello_service import HelloService
from app.modules.hello.hello_model import HelloModel
from app.utils.decorators import log_request, require_json
from app.utils.api_utils import generate_api_route
from app.router.api_routes import HelloApiRoutesEnum
from app.interfaces.icontroller import IController

class HelloController(IController):
    def __init__(self, app: Flask):
        self.app = app
        self.hello_service = HelloService(self.app.db)
        self.hello_bp = Blueprint('hello', __name__)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for HelloController")
        self.hello_bp.route(generate_api_route(HelloApiRoutesEnum.HELLO.value))(self.get_hello)
        self.app.register_blueprint(self.hello_bp)
    
    def apply_decorators(self):
        pass
    
    def get_hello(self):
        message = self.hello_service.get_hello_message()
        return jsonify(message)