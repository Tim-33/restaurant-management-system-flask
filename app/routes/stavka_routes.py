from flask import Flask, Blueprint, request, render_template, redirect, url_for
from app.interfaces.iroutes import IRoutes
from app.services.stavka_service import StavkaService
from app.services.recept_service import ReceptService
from app.services.restoran_service import RestoranService
from app.router.routes import StavkaRoutesEnum
import base64

class StavkaRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.stavka_routes_bp = Blueprint('stavka_routes', __name__)
        self.stavka_service = StavkaService(self.app)
        self.recept_service = ReceptService(self.app)
        self.restoran_service = RestoranService(self.app)
        self.tipovi = ['riba', 'salata', 'meso', 'alkohol', 'gazirano', 'kava', 'prilog', 'juha']
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Stavka")
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA.value, methods=["GET"])(self.get_stavke)
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA_ID.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA_ID.value, methods=["GET"])(self.get_stavka)
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA_CREATE.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA_CREATE.value, methods=["GET"])(self.create_stavka)
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA_CREATED.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA_CREATED.value, methods=["POST"])(self.created_stavka)
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA_UPDATE.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA_UPDATE.value, methods=["GET"])(self.update_stavka)
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA_UPDATED.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA_UPDATED.value, methods=["POST"])(self.updated_stavka)
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA_DELETE.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA_DELETE.value, methods=["POST"])(self.delete_stavka)
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA_MOST_EXPENSIVE.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA_MOST_EXPENSIVE.value, methods=["GET"])(self.get_stavke_most_expensive)
        self.app.logger.info(f"Registering route: {StavkaRoutesEnum.STAVKA_COUNT_BY_TIP_AND_RESTORAN.value}")
        self.stavka_routes_bp.route(StavkaRoutesEnum.STAVKA_COUNT_BY_TIP_AND_RESTORAN.value, methods=["GET"])(self.get_stavka_count_by_tip_and_restoran)
        self.app.register_blueprint(self.stavka_routes_bp)
        
    def get_stavke(self):
        try:
            data = self.stavka_service.get_stavke()
            return render_template(self.app.router.get_template(StavkaRoutesEnum.STAVKA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_stavke: {e}")
            return "Internal Server Error", 500
        
    def get_stavka(self, id):
        try:
            data = self.stavka_service.get_stavka(id)
            return render_template(self.app.router.get_template(StavkaRoutesEnum.STAVKA_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_stavka: {e}")
            return "Internal Server Error", 500
        
    def create_stavka(self):
        try:
            restorani = self.restoran_service.get_restorani()
            recepti = self.recept_service.get_recepti()
            return render_template(self.app.router.get_template(StavkaRoutesEnum.STAVKA_CREATE.value), restorani=restorani, recepti=recepti, tipovi=self.tipovi)
        except Exception as e:
            self.app.logger.error(f"Error in create_stavka: {e}")
            return "Internal Server Error", 500
        
    def created_stavka(self):
        try:
            file = request.files['slika']
            file_data = file.read()
            slika = base64.b64encode(file_data).decode('utf-8')
            body = {
                "restoran_id": request.form["restoran_id"],
                "recept_id": request.form["recept_id"],
                "naziv": request.form["naziv"],
                "stavka_tip": request.form["stavka_tip"],
                "cijena": request.form["cijena"],
                "opis": request.form["opis"],
                "slika": slika
            }
            self.stavka_service.insert_stavka(body)
            return redirect(url_for('stavka_routes.get_stavke'))
        except Exception as e:
            self.app.logger.error(f"Error in created_stavka: {e}")
            return "Internal Server Error", 500
        
    def update_stavka(self, id):
        try:
            data = self.stavka_service.get_stavka(id)
            restorani = self.restoran_service.get_restorani()
            recepti = self.recept_service.get_recepti()
            return render_template(self.app.router.get_template(StavkaRoutesEnum.STAVKA_UPDATE.value), data=data, restorani=restorani, recepti=recepti, tipovi=self.tipovi)
        except Exception as e:
            self.app.logger.error(f"Error in update_stavka: {e}")
            return "Internal Server Error", 500
        
    def updated_stavka(self, id):
        try:
            file = request.files['slika']
            file_data = file.read()
            slika = base64.b64encode(file_data).decode('utf-8')
            body = {
                "restoran_id": request.form["restoran_id"],
                "recept_id": request.form["recept_id"],
                "naziv": request.form["naziv"],
                "stavka_tip": request.form["stavka_tip"],
                "cijena": request.form["cijena"],
                "opis": request.form["opis"],
                "slika": slika
            }
            self.stavka_service.update_stavka(body, id)
            return redirect(url_for('stavka_routes.get_stavka', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_stavka: {e}")
            return "Internal Server Error", 500
        
    def delete_stavka(self, id):
        try:
            self.stavka_service.delete_stavka(id)
            return redirect(url_for('stavka_routes.get_stavke'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_stavka: {e}")
            return "Internal Server Error", 500
        
    def get_stavke_most_expensive(self):
        try:
            data = self.stavka_service.get_stavke_most_expensive()
            return render_template(self.app.router.get_template(StavkaRoutesEnum.STAVKA_MOST_EXPENSIVE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_stavke_most_expensive: {e}")
            return "Internal Server Error", 500
        
    def get_stavka_count_by_tip_and_restoran(self):
        try:
            data = self.stavka_service.get_stavka_count_by_tip_and_restoran()
            return render_template(self.app.router.get_template(StavkaRoutesEnum.STAVKA_COUNT_BY_TIP_AND_RESTORAN.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_stavka_count_by_tip_and_restoran: {e}")
            return "Internal Server Error", 500