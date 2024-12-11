from flask import Blueprint, jsonify, Flask, request
from app.modules.hello.hello_service import HelloService
from app.modules.hello.hello_model import HelloModel
from app.modules.hello.dto.create_hello_dto import CreateHelloDto
from app.utils.decorators import log_request, require_json
from app.utils.api_utils import generate_api_route
from app.router.api_routes import HelloApiRoutesEnum
from app.interfaces.icontroller import IController
from typing import List

class HelloController(IController):
    def __init__(self, app: Flask):
        self.app = app
        self.hello_service = HelloService(self.app)
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
    
    def get_all(self) -> List[HelloModel]:
        message = self.hello_service.get_hello_messages()
        return jsonify(message)
    
    def get_one(self, id) -> HelloModel:
        message = self.hello_service.get_hello_message(id)
        return jsonify(message)
    
    def insert(self):
        data = CreateHelloDto(**request.json)
        message = self.hello_service.insert_hello_message(data.message)
        return jsonify(message)
    
    def update(self, id):
        data = CreateHelloDto(**request.json)
        message = self.hello_service.update_hello_message(data.message, id)
        return jsonify(message)
    
    def delete(self, id):
        message = self.hello_service.delete_hello_message(id)
        return jsonify(message)
