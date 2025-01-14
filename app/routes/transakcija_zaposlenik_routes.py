from flask import request, redirect, url_for, render_template, Blueprint, Flask
from app.services.transakcija_zaposlenik_service import TransakcijaZaposlenikService
from app.interfaces.iroutes import IRoutes
from app.router.routes import TransakcijaZaposlenikRoutesEnum

class TransakcijaZaposlenikRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.transakcija_zaposlenik_service = TransakcijaZaposlenikService(app)
        self.transakcija_zaposlenik_bp = Blueprint("transakcija_zaposlenik_routes", __name__)
        
    def register_routes(self):
        self.app.logger.info("Registering transakcija zaposlenik routes")
        self.app.logger.info(f"Registering route: {TransakcijaZaposlenikRoutesEnum.TRANSAKCIJA_ZAPOSLENIK.value}")
        self.transakcija_zaposlenik_bp.route(TransakcijaZaposlenikRoutesEnum.TRANSAKCIJA_ZAPOSLENIK.value, methods=["GET"])(self.get_transakcije_zaposlenika)
        self.app.logger.info(f"Registering route: {TransakcijaZaposlenikRoutesEnum.TRANSAKCIJA_ZAPOSLENIK_ID.value}")
        self.transakcija_zaposlenik_bp.route(TransakcijaZaposlenikRoutesEnum.TRANSAKCIJA_ZAPOSLENIK_ID.value, methods=["GET"])(self.get_transakcija_zaposlenika)
        self.app.register_blueprint(self.transakcija_zaposlenik_bp)
        
    def get_transakcije_zaposlenika(self):
        try:
            data = self.transakcija_zaposlenik_service.get_transakcije_zaposlenika()
            return render_template(self.app.router.get_template(TransakcijaZaposlenikRoutesEnum.TRANSAKCIJA_ZAPOSLENIK.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_transakcije_zaposlenika: {e}")
            return "Internal Server Error", 500
        
    def get_transakcija_zaposlenika(self, id):
        try:
            data = self.transakcija_zaposlenik_service.get_transakcija_zaposlenika(id)
            return render_template(self.app.router.get_template(TransakcijaZaposlenikRoutesEnum.TRANSAKCIJA_ZAPOSLENIK_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_transakcija_zaposlenika: {e}")
            return "Internal Server Error", 500    
        
    