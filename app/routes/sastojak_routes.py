from flask import Flask, Blueprint, redirect, render_template, request, url_for
from app.interfaces.iroutes import IRoutes
from app.router.routes import SastojakRoutesEnum
from app.services.sastojak_service import SastojakService
from app.services.skladiste_service import SkladisteService
import base64

class SastojakRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.sastojak_routes_bp = Blueprint('sastojak_routes', __name__)
        self.sastojak_service = SastojakService(self.app)
        self.skladiste_service = SkladisteService(self.app)
        self.tipovi = ['g', 'mg', 'kg', 'l', 'ml', 'kol', 'tsp', 'tbsp']
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Sastojak")
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK.value, methods=["GET"])(self.get_sastojci)
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK_ID.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK_ID.value, methods=["GET"])(self.get_sastojak)
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK_CREATE.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK_CREATE.value, methods=["GET"])(self.create_sastojak)
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK_CREATED.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK_CREATED.value, methods=["POST"])(self.created_sastojak)
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK_UPDATE.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK_UPDATE.value, methods=["GET"])(self.update_sastojak)
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK_UPDATED.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK_UPDATED.value, methods=["POST"])(self.updated_sastojak)
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK_DELETE.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK_DELETE.value, methods=["POST"])(self.delete_sastojak)
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK_UKUPNA_KOLICINA.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK_UKUPNA_KOLICINA.value, methods=["GET"])(self.get_sastojak_ukupna_kolicina)
        self.app.logger.info(f"Registering route: {SastojakRoutesEnum.SASTOJAK_MOST_COMMON.value}")
        self.sastojak_routes_bp.route(SastojakRoutesEnum.SASTOJAK_MOST_COMMON.value, methods=["GET"])(self.get_sastojak_most_common)
        self.app.register_blueprint(self.sastojak_routes_bp)
        
    def get_sastojci(self):
        try:
            data = self.sastojak_service.get_sastojci()
            return render_template(self.app.router.get_template(SastojakRoutesEnum.SASTOJAK.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojci: {e}")
            return "Internal Server Error", 500
        
    def get_sastojak(self, id):
        try:
            data = self.sastojak_service.get_sastojak(id)
            skladista = self.skladiste_service.get_skladista()
            return render_template(self.app.router.get_template(SastojakRoutesEnum.SASTOJAK_ID.value), data=data, skladista=skladista)
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak: {e}")
            return "Internal Server Error", 500
        
    def create_sastojak(self):
        try:
            skladista = self.skladiste_service.get_skladista()
            return render_template(self.app.router.get_template(SastojakRoutesEnum.SASTOJAK_CREATE.value), skladista=skladista, tipovi=self.tipovi)
        except Exception as e:
            self.app.logger.error(f"Error in create_sastojak: {e}")
            return "Internal Server Error", 500
        
    def created_sastojak(self):
        try:
            form = request.form
            file = request.files['slika']
            file_data = file.read()
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            
            sastojak = {
                'naziv': form['naziv'],
                'cijena': form['cijena'],
                'kolicina_tip': form['kolicina_tip'],
                'slika': encoded_file,
                'potrebna_kolicina': form['potrebna_kolicina'],
                'trenutna_kolicina': form['trenutna_kolicina'],
                'skladiste_id': form['skladiste_id'],
            }
            self.sastojak_service.insert_sastojak(sastojak)
            return redirect(url_for('sastojak_routes.get_sastojci'))
        except Exception as e:
            self.app.logger.error(f"Error in created_sastojak: {e}")
            return "Internal Server Error", 500
        
    def update_sastojak(self, id):
        try:
            data = self.sastojak_service.get_sastojak(id)
            skladista = self.skladiste_service.get_skladista()
            return render_template(self.app.router.get_template(SastojakRoutesEnum.SASTOJAK_UPDATE.value), data=data, skladista=skladista, tipovi=self.tipovi)
        except Exception as e:
            self.app.logger.error(f"Error in update_sastojak: {e}")
            return "Internal Server Error", 500
        
    def updated_sastojak(self, id):
        try:
            form = request.form
            file = request.files['slika']
            file_data = file.read()
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            
            sastojak = {
                'naziv': form['naziv'],
                'cijena': form['cijena'],
                'kolicina_tip': form['kolicina_tip'],
                'slika': encoded_file,
                'potrebna_kolicina': form['potrebna_kolicina'],
                'skladiste_id': form['skladiste_id'],
            }
            self.sastojak_service.update_sastojak(sastojak, id)
            return redirect(url_for('sastojak_routes.get_sastojak', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_sastojak: {e}")
            return "Internal Server Error", 500
        
    def delete_sastojak(self, id):
        try:
            self.sastojak_service.delete_sastojak(id)
            return redirect(url_for('sastojak_routes.get_sastojci'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_sastojak: {e}")
            return "Internal Server Error", 500
        
    def get_sastojak_ukupna_kolicina(self):
        try:
            data = self.sastojak_service.get_sastojak_ukupna_kolicina()
            return render_template(self.app.router.get_template(SastojakRoutesEnum.SASTOJAK_UKUPNA_KOLICINA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak_ukupna_kolicina: {e}")
            return "Internal Server Error", 500
        
    def get_sastojak_most_common(self):
        try:
            data = self.sastojak_service.get_sastojci_most_common()
            return render_template(self.app.router.get_template(SastojakRoutesEnum.SASTOJAK_MOST_COMMON.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak_most_common: {e}")
            return "Internal Server Error", 500