from flask import Flask, Blueprint, render_template, request, redirect, url_for
from app.router.routes import MalaNezgodaRoutesEnum
from app.services.mala_nezgoda_service import MalaNezgodaService
from app.services.restoran_service import RestoranService
from app.services.zaposlenik_service import ZaposlenikService
from app.services.sastojak_service import SastojakService
from app.interfaces.iroutes import IRoutes

class MalaNezgodaRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.mala_nezgoda_routes_bp = Blueprint('mala_nezgoda_routes', __name__)
        self.mala_nezgoda_service = MalaNezgodaService(self.app)
        self.restoran_service = RestoranService(self.app)
        self.zaposlenik_service = ZaposlenikService(self.app)
        self.sastojak_service = SastojakService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for MalaNezgoda")
        self.app.logger.info(f"Registering route: {MalaNezgodaRoutesEnum.MALA_NEZGODA.value}")
        self.mala_nezgoda_routes_bp.route(MalaNezgodaRoutesEnum.MALA_NEZGODA.value, methods=["GET"])(self.get_male_nezgode)
        self.app.logger.info(f"Registering route: {MalaNezgodaRoutesEnum.MALA_NEZGODA_ID.value}")
        self.mala_nezgoda_routes_bp.route(MalaNezgodaRoutesEnum.MALA_NEZGODA_ID.value, methods=["GET"])(self.get_mala_nezgoda)
        self.app.logger.info(f"Registering route: {MalaNezgodaRoutesEnum.MALA_NEZGODA_CREATE.value}")
        self.mala_nezgoda_routes_bp.route(MalaNezgodaRoutesEnum.MALA_NEZGODA_CREATE.value, methods=["GET"])(self.create_mala_nezgoda)
        self.app.logger.info(f"Registering route: {MalaNezgodaRoutesEnum.MALA_NEZGODA_CREATED.value}")
        self.mala_nezgoda_routes_bp.route(MalaNezgodaRoutesEnum.MALA_NEZGODA_CREATED.value, methods=["POST"])(self.created_mala_nezgoda)
        self.app.logger.info(f"Registering route: {MalaNezgodaRoutesEnum.MALA_NEZGODA_UKUPNO.value}")
        self.mala_nezgoda_routes_bp.route(MalaNezgodaRoutesEnum.MALA_NEZGODA_UKUPNO.value, methods=["GET"])(self.get_mala_nezgoda_total)
        self.app.register_blueprint(self.mala_nezgoda_routes_bp)
        
    def get_male_nezgode(self):
        try:
            data = self.mala_nezgoda_service.get_male_nezgode()
            return render_template(self.app.router.get_template(MalaNezgodaRoutesEnum.MALA_NEZGODA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_male_nezgode: {e}")
            return "Internal Server Error", 500
        
    def get_mala_nezgoda(self, id):
        try:
            data = self.mala_nezgoda_service.get_mala_nezgoda(id)
            sastojci = self.sastojak_service.get_sastojak_by_mala_nezgoda(id)
            return render_template(self.app.router.get_template(MalaNezgodaRoutesEnum.MALA_NEZGODA_ID.value), data=data, sastojci=sastojci)
        except Exception as e:
            self.app.logger.error(f"Error in get_mala_nezgoda: {e}")
            return "Internal Server Error", 500
        
    def create_mala_nezgoda(self):
        try:
            restorani = self.restoran_service.get_restorani()
            zaposlenici = self.zaposlenik_service.get_zaposlenici()
            sastojci = self.sastojak_service.get_sastojci()
            return render_template(self.app.router.get_template(MalaNezgodaRoutesEnum.MALA_NEZGODA_CREATE.value), restorani=restorani, zaposlenici=zaposlenici, sastojci=sastojci)
        except Exception as e:
            self.app.logger.error(f"Error in create_mala_nezgoda: {e}")
            return "Internal Server Error", 500
        
    def created_mala_nezgoda(self):
        try:
            mala_nezgoda = {
                'restoran_id': request.form['restoran_id'],
                'zaposlenik_id': request.form['zaposlenik_id']
            }
            
            sastojci = []
            for key, value in request.form.items():
                if key.startswith('sastojak_') and int(value) > 0:
                    sastojak_id = key.split('_')[1]
                    kolicina = value
                    sastojci.append({'sastojak_id': sastojak_id, 'kolicina': kolicina})
                    
            self.mala_nezgoda_service.insert_mala_negoda_sastojci(mala_nezgoda, sastojci)
            return redirect(url_for('mala_nezgoda_routes.get_male_nezgode'))
        except Exception as e:
            self.app.logger.error(f"Error in created_mala_nezgoda: {e}")
            return "Internal Server Error", 500
        
    def get_mala_nezgoda_total(self):
        try:
            data = self.mala_nezgoda_service.get_total()
            return render_template(self.app.router.get_template(MalaNezgodaRoutesEnum.MALA_NEZGODA_UKUPNO.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_mala_nezgoda_total: {e}")
            return "Internal Server Error", 500