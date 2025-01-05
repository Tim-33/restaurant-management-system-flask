from app.utils.routes_utils import generate_page_route
from app.router.routes import *

class AppRouter:
    def __init__(self):
        self.routes = {}

    def add_route(self, route, template):
        self.routes[route] = template

    def get_template(self, route):
        return generate_page_route(self.routes.get(route, None))
    
    def create_routes(self):
        # Add routes for App
        self.add_route(AppRoutesEnum.HOME.value, 'app/home.html')
        self.add_route(AppRoutesEnum.GET_LOGIN.value, 'app/login.html')
        
        # Add routes for Hello
        self.add_route(HelloRoutesEnum.HELLO.value, 'hello/hellos.html')
        self.add_route(HelloRoutesEnum.HELLO_CREATE.value, 'hello/hello_create.html')
        self.add_route(HelloRoutesEnum.HELLO_ID.value, 'hello/hello.html')
        self.add_route(HelloRoutesEnum.HELLO_UPDATE.value, 'hello/hello_update.html')
        