from flask import Blueprint, render_template, Flask, redirect, url_for, request
from app.interfaces.iroutes import IRoutes
from app.router.routes import AppRoutesEnum
from app.router.api_routes import AuthApiRoutesEnum
from app.utils.api_utils import build_api_route, make_api_request, ApiMethodsEnum

class AppRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.app_routes_bp = Blueprint('app_routes', __name__)        
        self.base_url = self.app.config['API_BASE_URL']
        self.port = self.app.config['API_PORT']
        
    def register_routes(self):
        self.app.logger.info("Registering routes for AppRoutes")
        self.app.logger.info(f"Registering route: {AppRoutesEnum.HOME.value}")
        self.app_routes_bp.route(AppRoutesEnum.HOME.value, methods=["GET"])(self.get_index)
        self.app.logger.info(f"Registering route: {AppRoutesEnum.LOGIN.value}")
        self.app_routes_bp.route(AppRoutesEnum.GET_LOGIN.value, methods=["GET"])(self.get_login)
        self.app_routes_bp.route(AppRoutesEnum.LOGIN.value, methods=["POST"])(self.login)
        self.app.register_blueprint(self.app_routes_bp)
        
    def get_index(self):
        return render_template(self.app.router.get_template(AppRoutesEnum.HOME.value))
    
    def get_login(self):
        return render_template(self.app.router.get_template(AppRoutesEnum.GET_LOGIN.value))
    
    def login(self):
        try:
            data = request.form
            username = data.get('username')
            password = data.get('password')
            
            body = {
                "username": username,
                "password": password
            }
            
            url = build_api_route(self.base_url, self.port, AuthApiRoutesEnum.LOGIN.value)
            headers = {"Content-type": "application/json"}
            result = make_api_request(url, headers, self.app, ApiMethodsEnum.POST, body)
            
            if not result:
                return "Login failed", 401
            
            return redirect(url_for('hello_routes.get_hellos'))
        except Exception as e:
            self.app.logger.error(f"Error in login: {e}")
            return "Internal Server Error", 500