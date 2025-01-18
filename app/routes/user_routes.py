from flask import Flask, render_template, Blueprint
from app.interfaces.iroutes import IRoutes
from app.services.user_service import UserService
from app.router.routes import UserRoutesEnum

class UserRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.user_service = UserService(self.app)
        self.user_routes_bp = Blueprint('user_routes', __name__)

    def register_routes(self):
        self.app.logger.info("Registering routes for User")
        self.app.logger.info(f"Registering route: {UserRoutesEnum.USER.value}")
        self.user_routes_bp.route(UserRoutesEnum.USER.value, methods=["GET"])(self.get_users)
        self.app.register_blueprint(self.user_routes_bp)
        
    def get_users(self):
        try:
            data = self.user_service.get_users()
            return render_template(self.app.router.get_template(UserRoutesEnum.USER.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_users: {e}")
            return "Internal Server Error", 500