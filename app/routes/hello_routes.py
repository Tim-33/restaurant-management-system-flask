from flask import Blueprint, render_template, Flask, redirect, url_for, request
from app.interfaces.iroutes import IRoutes
from app.services.hello_service import HelloService
from app.router.routes import HelloRoutesEnum

class HelloRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.hello_routes_bp = Blueprint('hello_routes', __name__)
        self.base_url = self.app.config['API_BASE_URL']
        self.port = self.app.config['API_PORT']
        self.hello_service = HelloService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for HelloRoutes")
        self.app.logger.info(f"Registering route: {HelloRoutesEnum.HELLO.value}")
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO.value, methods=["GET"])(self.get_hellos)
        self.app.logger.info(f"Registering route: {HelloRoutesEnum.HELLO_ID.value}")
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO_ID.value, methods=["GET"])(self.get_hello)
        self.app.logger.info(f"Registering route: {HelloRoutesEnum.HELLO_CREATE.value}")
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO_CREATE.value, methods=["GET"])(self.create_hello)
        self.app.logger.info(f"Registering route: {HelloRoutesEnum.HELLO_CREATED.value}")
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO_CREATED.value, methods=["POST"])(self.created_hello)
        self.app.logger.info(f"Registering route: {HelloRoutesEnum.HELLO_UPDATE.value}")
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO_UPDATE.value, methods=["GET"])(self.update_hello)
        self.app.logger.info(f"Registering route: {HelloRoutesEnum.HELLO_UPDATED.value}")
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO_UPDATED.value, methods=["POST"])(self.updated_hello)
        self.app.logger.info(f"Registering route: {HelloRoutesEnum.HELLO_DELETE.value}")
        self.hello_routes_bp.route(HelloRoutesEnum.HELLO_DELETE.value, methods=["POST"])(self.delete_hello)
        self.app.register_blueprint(self.hello_routes_bp)
        
    def get_hellos(self):
        try:
            data = self.hello_service.get_hello_messages()
            return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_hellos: {e}")
            return "Internal Server Error", 500
        
    def create_hello(self):
        try:
            return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO_CREATE.value))
        except Exception as e:
            self.app.logger.error(f"Error in create_hello: {e}")
            return "Internal Server Error", 500
    
    def created_hello(self):
        try:
            data = request.form
            message = data.get('message')
            
            body = {
                "message": message
            }
            
            result = self.hello_service.insert_hello_message(body)
            if not result:
                return "Internal Server Error", 500
                       
            return redirect(url_for('hello_routes.get_hellos'))
        except Exception as e:
            self.app.logger.error(f"Error in created_hello: {e}")
            return "Internal Server Error", 500
        
    def get_hello(self, id):
        try:
            data = self.hello_service.get_hello_message(id)
            return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_hello: {e}")
            return "Internal Server Error", 500
        
    def update_hello(self, id):
        try:
            data = self.hello_service.get_hello_message(id)
            return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO_UPDATE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in update_hello: {e}")
            return "Internal Server Error", 500
        
    def updated_hello(self, id):
        try:
            data = request.form
            message = data.get('message')
            
            body = {
                "message": message
            }
            
            result = self.hello_service.update_hello_message(body, id)
            if not result:
                return "Internal Server Error", 500
            return redirect(url_for('hello_routes.get_hello', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in update_hello: {e}")
            return "Internal Server Error", 500

    def delete_hello(self, id):
        try:
            result = self.hello_service.delete_hello_message(id)
            if not result:
                return "Internal Server Error", 500
            return redirect(url_for('hello_routes.get_hellos'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_hello: {e}")
            return "Internal Server Error", 500