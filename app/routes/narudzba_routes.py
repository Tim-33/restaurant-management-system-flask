from flask import Flask, Blueprint, render_template, request, redirect, url_for
from app.router.routes import NarudzbaRoutesEnum
from app.services.narudzba_service import NarudzbaService
from app.services.skladiste_service import SkladisteService
from app.services.sastojak_service import SastojakService
from app.interfaces.iroutes import IRoutes

class NarudzbaRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.narudzba_routes_bp = Blueprint('narudzba_routes', __name__)
        self.narudzba_service = NarudzbaService(self.app)
        self.skladiste_service = SkladisteService(self.app)
        self.sastojak_service = SastojakService(self.app)
        self.statusi = ['ZAVRSENO', 'PONISTENO', 'NERIJESENO']
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Narudzba")
        self.app.logger.info(f"Registering route: {NarudzbaRoutesEnum.NARUDZBA.value}")
        self.narudzba_routes_bp.route(NarudzbaRoutesEnum.NARUDZBA.value, methods=["GET"])(self.get_narudzbe)
        self.app.logger.info(f"Registering route: {NarudzbaRoutesEnum.NARUDZBA_ID.value}")
        self.narudzba_routes_bp.route(NarudzbaRoutesEnum.NARUDZBA_ID.value, methods=["GET"])(self.get_narudzba)
        self.app.logger.info(f"Registering route: {NarudzbaRoutesEnum.NARUDZBA_CREATE.value}")
        self.narudzba_routes_bp.route(NarudzbaRoutesEnum.NARUDZBA_CREATE.value, methods=["GET"])(self.create_narudzba)
        self.app.logger.info(f"Registering route: {NarudzbaRoutesEnum.NARUDZBA_CREATED.value}")
        self.narudzba_routes_bp.route(NarudzbaRoutesEnum.NARUDZBA_CREATED.value, methods=["POST"])(self.created_narudzba)
        self.app.logger.info(f"Registering route: {NarudzbaRoutesEnum.NARUDZBA_UPDATE.value}")
        self.narudzba_routes_bp.route(NarudzbaRoutesEnum.NARUDZBA_UPDATE.value, methods=["GET"])(self.update_narudzba)
        self.app.logger.info(f"Registering route: {NarudzbaRoutesEnum.NARUDZBA_UPDATED.value}")
        self.narudzba_routes_bp.route(NarudzbaRoutesEnum.NARUDZBA_UPDATED.value, methods=["POST"])(self.updated_narudzba)
        self.app.logger.info(f"Registering route: {NarudzbaRoutesEnum.NARUDZBA_DELETE.value}")
        self.narudzba_routes_bp.route(NarudzbaRoutesEnum.NARUDZBA_DELETE.value, methods=["POST"])(self.delete_narudzba)
        self.app.logger.info(f"Registering route: {NarudzbaRoutesEnum.NARUDZBA_FINISH.value}")
        self.narudzba_routes_bp.route(NarudzbaRoutesEnum.NARUDZBA_FINISH.value, methods=["POST"])(self.finish_narudzba)
        self.app.register_blueprint(self.narudzba_routes_bp)
        
    def get_narudzbe(self):
        try:
            data = self.narudzba_service.get_narudzbe()
            return render_template(self.app.router.get_template(NarudzbaRoutesEnum.NARUDZBA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_narudzbe: {e}")
            return "Internal Server Error", 500
        
    def get_narudzba(self, id):
        try:
            data = self.narudzba_service.get_narudzba(id)
            sastojci = self.sastojak_service.get_sastojak_by_narudzba(id)
            return render_template(self.app.router.get_template(NarudzbaRoutesEnum.NARUDZBA_ID.value), data=data, sastojci=sastojci)
        except Exception as e:
            self.app.logger.error(f"Error in get_narudzba: {e}")
            return "Internal Server Error", 500
        
    def create_narudzba(self):
        try:
            skladista = self.skladiste_service.get_skladista()
            sastojci = self.sastojak_service.get_sastojci()
            return render_template(self.app.router.get_template(NarudzbaRoutesEnum.NARUDZBA_CREATE.value), skladista=skladista, sastojci=sastojci)
        except Exception as e:
            self.app.logger.error(f"Error in create_narudzba: {e}")
            return "Internal Server Error", 500
        
    def created_narudzba(self):
        try:
            form = request.form
            narudzba = {
                'skladiste_id': form['skladiste_id'],
                'naziv': form['naziv']
            }
            
            sastojci = []
            for key in form.keys():
                if "sastojak" in key:
                    sastojak = {
                        'id': key.split("_")[1],
                        'kolicina': form[key]
                    }
                    sastojci.append(sastojak)
                    
            self.narudzba_service.insert_narudzbe_sastojci(narudzba, sastojci)
            return redirect(url_for('narudzba_routes.get_narudzbe'))
        except Exception as e:
            self.app.logger.error(f"Error in created_narudzba: {e}")
            return "Internal Server Error", 500
        
    def update_narudzba(self, id):
        try:
            data = self.narudzba_service.get_narudzba(id)
            skladista = self.skladiste_service.get_skladista()
            sastojci = self.sastojak_service.get_sastojak_by_skladiste(data['skladiste_id'])
            sastojci_narudzbe = self.sastojak_service.get_sastojak_by_narudzba(id)
            return render_template(self.app.router.get_template(NarudzbaRoutesEnum.NARUDZBA_UPDATE.value), data=data, skladista=skladista, sastojci=sastojci, sastojci_narudzbe=sastojci_narudzbe)
        except Exception as e:
            self.app.logger.error(f"Error in update_narudzba: {e}")
            return "Internal Server Error", 500
        
    def updated_narudzba(self, id):
        try:
            form = request.form
            narudzba = {
                'skladiste_id': form['skladiste_id'],
                'naziv': form['naziv']
            }
            
            sastojci_updated = []
            for key, value in form.items():
                if key.startswith('sastojak_') and int(value) > 0:
                    sastojak_id = key.split('_')[1]
                    kolicina = value
                    sastojci_updated.append({
                        'sastojak_id': sastojak_id,
                        'kolicina': kolicina
                    })
                    
            sastojci = self.sastojak_service.get_sastojak_by_narudzba(id)
            self.narudzba_service.update_narudzbe_sastojci(id, narudzba, sastojci, sastojci_updated)
            return redirect(url_for('narudzba_routes.get_narudzba', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_narudzba: {e}")
            return "Internal Server Error", 500
        
    def delete_narudzba(self, id):
        try:
            self.narudzba_service.delete_narudzba(id)
            return redirect(url_for('narudzba_routes.get_narudzbe'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_narudzba: {e}")
            return "Internal Server Error", 500
        
    def finish_narudzba(self, id):
        try:
            self.narudzba_service.finish_narudzba(id)
            return redirect(url_for('narudzba_routes.get_narudzbe'))
        except Exception as e:
            self.app.logger.error(f"Error in finish_narudzba: {e}")
            return "Internal Server Error", 500