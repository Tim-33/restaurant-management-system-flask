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
        
        # Add routes for Zaposlenik
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK.value, 'zaposlenik/zaposlenici.html')
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK_CREATE.value, 'zaposlenik/zaposlenik_create.html')
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK_ID.value, 'zaposlenik/zaposlenik.html')
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK_UPDATE.value, 'zaposlenik/zaposlenik_update.html')
        
        