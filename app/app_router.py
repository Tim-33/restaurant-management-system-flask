from app.utils.routes_utils import generate_page_route
from app.routes.app_routes import AppRoutesRoutesEnum
from app.routes.hello_routes import HelloRoutesRoutesEnum

class AppRouter:
    def __init__(self):
        self.routes = {}

    def add_route(self, route, template):
        self.routes[route] = template

    def get_template(self, route):
        return generate_page_route(self.routes.get(route, None))
    
    def create_routes(self):
        self.add_route(AppRoutesRoutesEnum.HOME.value, 'home.html')
        self.add_route(HelloRoutesRoutesEnum.HELLO.value, 'hello.html')