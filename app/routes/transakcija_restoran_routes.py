from flask import request, redirect, url_for, render_template, Blueprint, Flask
from app.services.transakcija_restoran_service import TransakcijaRestoranService
from app.interfaces.iroutes import IRoutes
from app.router.routes import TransakcijaRestoranRoutesEnum

class TransakcijaRestoranRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.transakcija_restoran_service = TransakcijaRestoranService(app)
        self.transakcija_restoran_bp = Blueprint("transakcija_restoran_routes", __name__)
        
    def register_routes(self):
        self.app.logger.info("Registering transakcija restoran routes")
        self.app.logger.info(f"Registering route: {TransakcijaRestoranRoutesEnum.TRANSAKCIJA_RESOTRAN.value}")
        self.transakcija_restoran_bp.route(TransakcijaRestoranRoutesEnum.TRANSAKCIJA_RESOTRAN.value, methods=["GET"])(self.get_transakcije_restorana)
        self.app.logger.info(f"Registering route: {TransakcijaRestoranRoutesEnum.TRANSKACIJA_RESTORAN_ID.value}")
        self.transakcija_restoran_bp.route(TransakcijaRestoranRoutesEnum.TRANSKACIJA_RESTORAN_ID.value, methods=["GET"])(self.get_transakcija_restorana)
        self.app.register_blueprint(self.transakcija_restoran_bp)
        
    def get_transakcije_restorana(self):
        try:
            data = self.transakcija_restoran_service.get_transakcije_restorana()
            return render_template(self.app.router.get_template(TransakcijaRestoranRoutesEnum.TRANSAKCIJA_RESOTRAN.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_transakcije_restorana: {e}")
            return "Internal Server Error", 500
        
    def get_transakcija_restorana(self, id):
        try:
            data = self.transakcija_restoran_service.get_transakcija_restorana(id)
            return render_template(self.app.router.get_template(TransakcijaRestoranRoutesEnum.TRANSKACIJA_RESTORAN_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_transakcija_restorana: {e}")
            return "Internal Server Error", 500    
        
    