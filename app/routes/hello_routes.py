from flask import Blueprint, render_template, Flask, redirect, url_for, request
from app.interfaces.iroutes import IRoutes
from app.utils.api_utils import build_api_route
from app.router.api_routes import HelloApiRoutesEnum
from app.router.routes import HelloRoutesEnum
from app.utils.api_utils import make_api_request, ApiMethodsEnum
    
class HelloRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.hello_routes_bp = Blueprint('hello_routes', __name__)
        self.base_url = self.app.config['API_BASE_URL']
        self.port = self.app.config['API_PORT']
        
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
            url = build_api_route(self.base_url, self.port, HelloApiRoutesEnum.HELLO.value)
            self.app.logger.info(f"Request URL: {url}")
            headers = {"Content-type": "application/json"}
            data = make_api_request(url, headers, self.app, ApiMethodsEnum.GET)
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
    
    def created_hello(self, body):
        try:
            data = request.form
            message = data.get('message')
            
            url = build_api_route(self.base_url, self.port, HelloApiRoutesEnum.HELLO.value)
            headers = {"Content-type": "application/json"}
            make_api_request(url, headers, self.app, ApiMethodsEnum.POST)
            return redirect(url_for(HelloRoutesEnum.HELLO.value))
        except Exception as e:
            self.app.logger.error(f"Error in created_hello: {e}")
            return "Internal Server Error", 500
        
    def get_hello(self, id):
        try:
            endpoint = HelloApiRoutesEnum.HELLO_ID.value.replace("<int:id>", str(id))
            url = build_api_route(self.base_url, self.port, endpoint)
            headers = {"Content-type": "application/json"}
            data = make_api_request(url, headers, self.app, ApiMethodsEnum.GET)
            return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_hello: {e}")
            return "Internal Server Error", 500
        
    def update_hello(self, id):
        try:
            endpoint = HelloApiRoutesEnum.HELLO_ID.value.replace("<int:id>", str(id))
            url = build_api_route(self.base_url, self.port, endpoint)
            headers = {"Content-type": "application/json"}
            data = make_api_request(url, headers, self.app, ApiMethodsEnum.GET)
            return render_template(self.app.router.get_template(HelloRoutesEnum.HELLO_UPDATE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in update_hello: {e}")
            return "Internal Server Error", 500
        
    def updated_hello(self, id):
        try:
            endpoint = HelloApiRoutesEnum.HELLO_ID.value.replace("<int:id>", str(id))
            url = build_api_route(self.base_url, self.port, endpoint)
            headers = {"Content-type": "application/json"}
            make_api_request(url, headers, self.app, ApiMethodsEnum.PUT)
            return redirect(url_for(HelloRoutesEnum.HELLO_ID.value, id=id))
        except Exception as e:
            self.app.logger.error(f"Error in update_hello: {e}")
            return "Internal Server Error", 500

    def delete_hello(self, id):
        try:
            endpoint = HelloApiRoutesEnum.HELLO_ID.value.replace("<int:id>", str(id))
            url = build_api_route(self.base_url, self.port, endpoint)
            headers = {"Content-type": "application/json"}
            make_api_request(url, headers, self.app, ApiMethodsEnum.DELETE)
            return redirect(url_for(HelloRoutesEnum.HELLO.value))
        except Exception as e:
            self.app.logger.error(f"Error in delete_hello: {e}")
            return "Internal Server Error", 500