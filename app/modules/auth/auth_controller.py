from app.interfaces.icontroller import IController
from flask import Flask, Blueprint, request, jsonify
from app.utils.api_utils import generate_api_route
from app.router.api_routes import AuthApiRoutesEnum
from app.modules.auth.auth_service import AuthService
from app.modules.auth.dto.login_dto import LoginDto

class AuthController(IController):
    def __init__(self, app: Flask):
        self.app = app
        self.service = AuthService(self.app)
        self.hello_bp = Blueprint('auth', __name__)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for AuthController")
        self.hello_bp.route(generate_api_route(AuthApiRoutesEnum.LOGIN.value), methods=['POST'])(self.login)
        self.app.register_blueprint(self.hello_bp)
                
    def login(self):
        data = LoginDto(**request.json)
        username = data.username
        password = data.password
        result = self.service.login(username, password)
        return jsonify(result)