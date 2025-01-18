from app.interfaces.iroutes import IRoutes
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from app.router.routes import ReceptRoutesEnum
from app.services.recept_service import ReceptService
from app.services.restoran_service import RestoranService
from app.services.sastojak_service import SastojakService

class ReceptRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.recept_routes_bp = Blueprint('recept_routes', __name__)
        self.recept_service = ReceptService(self.app)
        self.restoran_service = RestoranService(self.app)
        self.sastojak_service = SastojakService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Recept")
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT.value, methods=["GET"])(self.get_recepti)
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT_ID.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT_ID.value, methods=["GET"])(self.get_recept)
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT_CREATE.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT_CREATE.value, methods=["GET"])(self.create_recept)
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT_CREATED.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT_CREATED.value, methods=["POST"])(self.created_recept)
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT_UPDATE.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT_UPDATE.value, methods=["GET"])(self.update_recept)
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT_UPDATED.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT_UPDATED.value, methods=["POST"])(self.updated_recept)
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT_DELETE.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT_DELETE.value, methods=["POST"])(self.delete_recept)
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT_UKUPNI_PRIHOD.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT_UKUPNI_PRIHOD.value, methods=["GET"])(self.get_recept_ukupni_prihod)
        self.app.logger.info(f"Registering route: {ReceptRoutesEnum.RECEPT_PRIHOD_PRVOG_RACUNA.value}")
        self.recept_routes_bp.route(ReceptRoutesEnum.RECEPT_PRIHOD_PRVOG_RACUNA.value, methods=["GET"])(self.get_recept_prihod_prvog_racuna)
        self.app.register_blueprint(self.recept_routes_bp)
        
    def get_recepti(self):
        try:
            data = self.recept_service.get_recepti()
            return render_template(self.app.router.get_template(ReceptRoutesEnum.RECEPT.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_recepti: {e}")
            return "Internal Server Error", 500
        
    def get_recept(self, id):
        try:
            data = self.recept_service.get_recept(id)
            sastojci = self.sastojak_service.get_sastojak_by_recept(id)
            return render_template(self.app.router.get_template(ReceptRoutesEnum.RECEPT_ID.value), data=data, sastojci=sastojci)
        except Exception as e:
            self.app.logger.error(f"Error in get_recept: {e}")
            return "Internal Server Error", 500
        
    def create_recept(self):
        try:
            restorani = self.restoran_service.get_restorani()
            sastojci = self.sastojak_service.get_sastojci()
            return render_template(self.app.router.get_template(ReceptRoutesEnum.RECEPT_CREATE.value), restorani=restorani, sastojci=sastojci)
        except Exception as e:
            self.app.logger.error(f"Error in create_recept: {e}")
            return "Internal Server Error", 500
        
    def created_recept(self):
        try:
            form = request.form
            recept = {
                'restoran_id': form['restoran_id'],
                'naziv': form['naziv'],
                'upute': form['upute']
            }
            
            sastojci = []
            for key, value in form.items():
                if key.startswith('sastojak_') and int(value) > 0:
                    sastojak_id = key.split('_')[1]
                    kolicina = value
                    sastojci.append({
                        'sastojak_id': sastojak_id,
                        'kolicina': kolicina
                    })
                       
            self.recept_service.insert_recept_sastojci(recept, sastojci)
            return redirect(url_for('recept_routes.get_recepti'))
        except Exception as e:
            self.app.logger.error(f"Error in created_recept: {e}")
            return "Internal Server Error", 500
        
    def update_recept(self, id):
        try:
            data = self.recept_service.get_recept(id)
            restorani = self.restoran_service.get_restorani()
            sastojci = self.sastojak_service.get_sastojci()
            sastojci_recepta = self.sastojak_service.get_sastojak_by_recept(id)
            return render_template(self.app.router.get_template(ReceptRoutesEnum.RECEPT_UPDATE.value), data=data, restorani=restorani, sastojci=sastojci, sastojci_recepta=sastojci_recepta)
        except Exception as e:
            self.app.logger.error(f"Error in update_recept: {e}")
            return "Internal Server Error", 500
        
    def updated_recept(self, id):
        try:
            form = request.form
            recept = {
                'restoran_id': form['restoran_id'],
                'naziv': form['naziv'],
                'upute': form['upute']
            }
            
            sastojci = []
            for key, value in form.items():
                if key.startswith('sastojak_') and int(value) > 0:
                    sastojak_id = key.split('_')[1]
                    kolicina = value
                    sastojci.append({
                        'sastojak_id': sastojak_id,
                        'kolicina': kolicina
                    })
                    
            sastojci_updated = self.sastojak_service.get_sastojak_by_recept(id)
                    
            self.recept_service.update_recept_sastojci(id, recept, sastojci, sastojci_updated)
            return redirect(url_for('recept_routes.get_recept', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_recept: {e}")
            return "Internal Server Error", 500
        
    def delete_recept(self, id):
        try:
            self.recept_service.delete_recept(id)
            return redirect(url_for('recept_routes.get_recepti'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_recept: {e}")
            return "Internal Server Error", 500
        
    def get_recept_ukupni_prihod(self):
        try:
            data = self.recept_service.get_recept_ukupni_prihod()
            return render_template(self.app.router.get_template(ReceptRoutesEnum.RECEPT_UKUPNI_PRIHOD.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_recept_ukupni_prihod: {e}")
            return "Internal Server Error", 500
        
    def get_recept_prihod_prvog_racuna(self):
        try:
            data = self.recept_service.get_recept_prihod_prvog_racuna()
            return render_template(self.app.router.get_template(ReceptRoutesEnum.RECEPT_PRIHOD_PRVOG_RACUNA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_recept_prihod_prvog_racuna: {e}")
            return "Internal Server Error", 500