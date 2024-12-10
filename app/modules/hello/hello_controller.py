from flask import Blueprint, jsonify, Flask, request
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
        self.hello_bp.route(generate_api_route(HelloApiRoutesEnum.HELLO.value), methods=['GET'])(self.get_all)
        self.hello_bp.route(generate_api_route(HelloApiRoutesEnum.HELLO_ID.value), methods=['GET'])(self.get_one)
        self.hello_bp.route(generate_api_route(HelloApiRoutesEnum.HELLO.value), methods=['POST'])(self.insert)
        self.hello_bp.route(generate_api_route(HelloApiRoutesEnum.HELLO_ID.value), methods=['PUT'])(self.update)
        self.hello_bp.route(generate_api_route(HelloApiRoutesEnum.HELLO_ID.value), methods=['DELETE'])(self.delete)
        self.app.register_blueprint(self.hello_bp)
    
    def apply_decorators(self):
        pass
    
    def get_all(self):
        # message = self.hello_service.get_hello_messages()
        message = [ { "id": 1, "message": "Hello, World!" } ]
        return jsonify(message)
    
    def get_one(self, id):
        message = self.hello_service.get_hello_message(id)
        return jsonify(message)
    
    def insert(self):
        data = HelloModel.from_json(request.json)
        message = self.hello_service.insert_hello_message(data.message)
        return jsonify(message)
    
    def update(self, id):
        data = HelloModel.from_json(request.json)
        message = self.hello_service.update_hello_message(data.message, id)
        return jsonify(message)
    
    def delete(self, id):
        message = self.hello_service.delete_hello_message(id)
        return jsonify(message)
