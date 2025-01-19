from flask import Flask, Blueprint, render_template, request, redirect, url_for
from app.router.routes import VelikaNezgodaRoutesEnum
from app.services.velika_nezgoda_service import VelikaNezgodaService
from app.services.restoran_service import RestoranService
from app.services.zaposlenik_service import ZaposlenikService
from app.services.stavka_service import StavkaService
from app.interfaces.iroutes import IRoutes
import json

class VelikaNezgodaRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.velika_nezgoda_routes_bp = Blueprint('velika_nezgoda_routes', __name__)
        self.velika_nezgoda_service = VelikaNezgodaService(self.app)
        self.restoran_service = RestoranService(self.app)
        self.zaposlenik_service = ZaposlenikService(self.app)
        self.stavka_service = StavkaService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for VelikaNezgoda")
        self.app.logger.info(f"Registering route: {VelikaNezgodaRoutesEnum.VELIKA_NEZGODA.value}")
        self.velika_nezgoda_routes_bp.route(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA.value, methods=["GET"])(self.get_velike_nezgode)
        self.app.logger.info(f"Registering route: {VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_ID.value}")
        self.velika_nezgoda_routes_bp.route(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_ID.value, methods=["GET"])(self.get_velika_nezgoda)
        self.app.logger.info(f"Registering route: {VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_CREATE.value}")
        self.velika_nezgoda_routes_bp.route(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_CREATE.value, methods=["GET"])(self.create_velika_nezgoda)
        self.app.logger.info(f"Registering route: {VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_CREATED.value}")
        self.velika_nezgoda_routes_bp.route(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_CREATED.value, methods=["POST"])(self.created_velika_nezgoda)
        self.app.logger.info(f"Registering route: {VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_DETAILS.value}")
        self.velika_nezgoda_routes_bp.route(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_DETAILS.value, methods=["GET"])(self.get_velike_nezgode_with_details)
        self.app.register_blueprint(self.velika_nezgoda_routes_bp)
        
    def get_velike_nezgode(self):
        try:
            data = self.velika_nezgoda_service.get_velike_nezgode()
            return render_template(self.app.router.get_template(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_velike_nezgode: {e}")
            return "Internal Server Error", 500
        
    def get_velika_nezgoda(self, id):
        try:
            data = self.velika_nezgoda_service.get_velika_nezgoda(id)
            stavke = self.stavka_service.get_stavke_by_velika_nezgoda(id)
            return render_template(self.app.router.get_template(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_ID.value), data=data, stavke=stavke)
        except Exception as e:
            self.app.logger.error(f"Error in get_velika_nezgoda: {e}")
            return "Internal Server Error", 500
        
    def create_velika_nezgoda(self):
        try:
            restorani = self.restoran_service.get_restorani()
            zaposlenici = self.zaposlenik_service.get_zaposlenici()
            stavke = self.stavka_service.get_stavke()
            return render_template(self.app.router.get_template(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_CREATE.value), restorani=restorani, zaposlenici=zaposlenici, stavke=stavke)
        except Exception as e:
            self.app.logger.error(f"Error in create_velika_nezgoda: {e}")
            return "Internal Server Error", 500
        
    def created_velika_nezgoda(self):
        try:
            velika_nezgoda = {
                'restoran_id': request.form['restoran_id'],
                'zaposlenik_id': request.form['zaposlenik_id']
            }
            
            stavke = []
            for key, value in request.form.items():
                if key.startswith('stavka_') and int(value) > 0:
                    stavke.append({
                        'stavka_id': key.split('_')[1],
                        'kolicina': value
                    })
                    
            velika_nezgoda["stavke"] = json.dumps(stavke)
                    
            self.velika_nezgoda_service.insert_by_transaction(velika_nezgoda)
            return redirect(url_for('velika_nezgoda_routes.get_velike_nezgode'))
        except Exception as e:
            self.app.logger.error(f"Error in created_velika_nezgoda: {e}")
            return "Internal Server Error", 500
        
    def get_velike_nezgode_with_details(self):
        try:
            data = self.velika_nezgoda_service.get_velike_nezgode_with_details()
            return render_template(self.app.router.get_template(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_DETAILS.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_velike_nezgode_with_details: {e}")
            return "Internal Server Error", 500