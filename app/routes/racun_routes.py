from flask import Flask, Blueprint, request, redirect, render_template, url_for
from app.interfaces.iroutes import IRoutes
from app.router.routes import RacunRoutesEnum
from app.services.racun_service import RacunService
from app.services.restoran_service import RestoranService
from app.services.zaposlenik_service import ZaposlenikService
from app.services.stol_service import StolService
from app.services.stavka_service import StavkaService

class RacunRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.racun_routes_bp = Blueprint("racun_routes", __name__)
        self.racun_service = RacunService(self.app)
        self.restoran_service = RestoranService(self.app)
        self.zaposlenik_service = ZaposlenikService(self.app)
        self.stol_service = StolService(self.app)
        self.stavka_service = StavkaService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Racun")
        self.app.logger.info(f"Registering route: {RacunRoutesEnum.RACUN.value}")
        self.racun_routes_bp.route(RacunRoutesEnum.RACUN.value, methods=["GET"])(self.get_racuni)
        self.app.logger.info(f"Registering route: {RacunRoutesEnum.RACUN_ID.value}")
        self.racun_routes_bp.route(RacunRoutesEnum.RACUN_ID.value, methods=["GET"])(self.get_racun)
        self.app.logger.info(f"Registering route: {RacunRoutesEnum.RACUN_CREATE.value}")
        self.racun_routes_bp.route(RacunRoutesEnum.RACUN_CREATE.value, methods=["GET"])(self.create_racun)
        self.app.logger.info(f"Registering route: {RacunRoutesEnum.RACUN_CREATED.value}")
        self.racun_routes_bp.route(RacunRoutesEnum.RACUN_CREATED.value, methods=["POST"])(self.created_racun)
        self.app.logger.info(f"Registering route: {RacunRoutesEnum.RACUN_UKUPNA_VRIJEDNOST.value}")
        self.racun_routes_bp.route(RacunRoutesEnum.RACUN_UKUPNA_VRIJEDNOST.value, methods=["GET"])(self.get_racun_ukupna_vrijednost)
        self.app.register_blueprint(self.racun_routes_bp)
        
    def get_racuni(self):
        try:
            data = self.racun_service.get_racuni()
            return render_template(self.app.router.get_template(RacunRoutesEnum.RACUN.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_racuni: {e}")
            return "Internal Server Error", 500
        
    def get_racun(self, id):
        try:
            data = self.racun_service.get_racun(id)
            stavke = self.stavka_service.get_stavke_by_racun(id)
            return render_template(self.app.router.get_template(RacunRoutesEnum.RACUN_ID.value), data=data, stavke=stavke)
        except Exception as e:
            self.app.logger.error(f"Error in get_racun: {e}")
            return "Internal Server Error", 500
        
    def create_racun(self):
        try:
            restorani = self.restoran_service.get_restorani()
            zaposlenici = self.zaposlenik_service.get_zaposlenici()
            stolovi = self.stol_service.get_stolovi()
            stavke = self.stavka_service.get_stavke()
            return render_template(self.app.router.get_template(RacunRoutesEnum.RACUN_CREATE.value), restorani=restorani, zaposlenici=zaposlenici, stolovi=stolovi, stavke=stavke)
        except Exception as e:
            self.app.logger.error(f"Error in create_racun: {e}")
            return "Internal Server Error", 500
        
    def created_racun(self):
        try:
            form = request.form
            racun = {
                'restoran_id': form['restoran_id'],
                'zaposlenik_id': form['zaposlenik_id'],
                'stol_id': form['stol_id'],
                'broj_racuna': form['broj_racuna'],
                'napojnica': form['napojnica'],
            }
            stavke = []
            for key, value in form.items():
                if key.startswith('stavka_') and int(value) > 0:
                    stavka_id = key.split('_')[1]
                    kolicina = value
                    stavke.append({
                        'stavka_id': stavka_id,
                        'kolicina': kolicina
                    })
                        
            self.racun_service.insert_racun_stavke(racun, stavke)
            return redirect(url_for('racun_routes.get_racuni'))
        except Exception as e:
            self.app.logger.error(f"Error in created_racun: {e}")
            return "Internal Server Error", 500
        
    def get_racun_ukupna_vrijednost(self):
        try:
            data = self.racun_service.get_racun_ukupna_vrijednost()
            return render_template(self.app.router.get_template(RacunRoutesEnum.RACUN_UKUPNA_VRIJEDNOST.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_racun_ukupna_vrijednost: {e}")
            return "Internal Server Error", 500