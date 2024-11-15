from app.utils.routes_utils import generate_page_route
from app.routes.app_routes import AppRoutesEnum
from app.routes.hello_routes import HelloRoutesEnum

class AppRouter:
    def __init__(self):
        self.routes = {}

    def add_route(self, route, template):
        self.routes[route] = template

    def get_template(self, route):
        return generate_page_route(self.routes.get(route, None))
    
    def create_routes(self):
        self.add_route(AppRoutesEnum.HOME.value, 'home.html')
        self.add_route(HelloRoutesEnum.HELLO.value, 'hello.html')