from flask import Blueprint, render_template, Flask
from app.interfaces.iroutes import IRoutes
from app.router.routes import AppRoutesEnum

class AppRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.app_routes_bp = Blueprint('app_routes', __name__)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for AppRoutes")
        self.app_routes_bp.route(AppRoutesEnum.HOME.value, methods=["GET"])(self.get_index)
        self.app.register_blueprint(self.app_routes_bp)
        
    def get_index(self):
        return render_template(self.app.router.get_template(AppRoutesEnum.HOME.value))