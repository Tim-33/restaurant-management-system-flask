from app.interfaces.iroutes import IRoutes
from flask import Flask, request, redirect, url_for, render_template, Blueprint
from app.services.restoran_racun_service import RestoranRacunService
from app.services.restoran_service import RestoranService
from app.router.routes import RestoranRacunRoutesEnum

class RestoranRacunRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.restoran_racun_bp = Blueprint('restoran_racun_routes', __name__)
        self.restoran_racun_service = RestoranRacunService(app)
        self.restoran_service = RestoranService(app)
        self.valute = ['EUR', 'USD', 'CAD', 'GBP', 'AUD', 'JPY', 'CNY', 'CHF', 'SEK', 'NZD']
        
    def register_routes(self):
        self.app.logger.info("Registering routes for RestoranRacun")
        self.app.logger.info(f"Registering route: {RestoranRacunRoutesEnum.RESTORAN_RACUN.value}")
        self.restoran_racun_bp.route(RestoranRacunRoutesEnum.RESTORAN_RACUN.value, methods=["GET"])(self.get_restoran_racuni)
        self.app.logger.info(f"Registering route: {RestoranRacunRoutesEnum.RESTORAN_RACUN_ID.value}")
        self.restoran_racun_bp.route(RestoranRacunRoutesEnum.RESTORAN_RACUN_ID.value, methods=["GET"])(self.get_restoran_racun)
        self.app.logger.info(f"Registering route: {RestoranRacunRoutesEnum.RESTORAN_RACUN_CREATE.value}")
        self.restoran_racun_bp.route(RestoranRacunRoutesEnum.RESTORAN_RACUN_CREATE.value, methods=["GET"])(self.create_restoran_racun)
        self.app.logger.info(f"Registering route: {RestoranRacunRoutesEnum.RESTORAN_RACUN_CREATED.value}")
        self.restoran_racun_bp.route(RestoranRacunRoutesEnum.RESTORAN_RACUN_CREATED.value, methods=["POST"])(self.created_restoran_racun)
        self.app.logger.info(f"Registering route: {RestoranRacunRoutesEnum.RESTORAN_RACUN_UPDATE.value}")
        self.restoran_racun_bp.route(RestoranRacunRoutesEnum.RESTORAN_RACUN_UPDATE.value, methods=["GET"])(self.update_restoran_racun)
        self.app.logger.info(f"Registering route: {RestoranRacunRoutesEnum.RESTORAN_RACUN_UPDATED.value}")
        self.restoran_racun_bp.route(RestoranRacunRoutesEnum.RESTORAN_RACUN_UPDATED.value, methods=["POST"])(self.updated_restoran_racun)
        self.app.logger.info(f"Registering route: {RestoranRacunRoutesEnum.RESTORAN_RACUN_DELETE.value}")
        self.restoran_racun_bp.route(RestoranRacunRoutesEnum.RESTORAN_RACUN_DELETE.value, methods=["POST"])(self.delete_restoran_racun)
        self.app.register_blueprint(self.restoran_racun_bp)
        
    def get_restoran_racuni(self):
        try:
            data = self.restoran_racun_service.get_restoran_racuni()
            return render_template(self.app.router.get_template(RestoranRacunRoutesEnum.RESTORAN_RACUN.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_racuni: {e}")
            return "Internal Server Error", 500
        
    def get_restoran_racun(self, id):
        try:
            data = self.restoran_racun_service.get_restoran_racun(id)
            return render_template(self.app.router.get_template(RestoranRacunRoutesEnum.RESTORAN_RACUN_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_racun: {e}")
            return "Internal Server Error", 500
        
    def create_restoran_racun(self):
        try:
            data = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(RestoranRacunRoutesEnum.RESTORAN_RACUN_CREATE.value), data=data, valute=self.valute)
        except Exception as e:
            self.app.logger.error(f"Error in create_restoran_racun: {e}")
            return "Internal Server Error", 500
        
    def created_restoran_racun(self):
        try:
            form = request.form
            restoran_racun = {
                'restoran_id': form['restoran_id'],
                'valuta': form['valuta'],
            }
            self.restoran_racun_service.insert_restoran_racun(restoran_racun)
            return redirect(url_for('restoran_racun_routes.get_restoran_racuni'))
        except Exception as e:
            self.app.logger.error(f"Error in created_restoran_racun: {e}")
            return "Internal Server Error", 500
        
    def update_restoran_racun(self, id):
        try:
            data = self.restoran_racun_service.get_restoran_racun(id)
            restorani = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(RestoranRacunRoutesEnum.RESTORAN_RACUN_UPDATE.value), data=data, restorani=restorani, valute=self.valute)
        except Exception as e:
            self.app.logger.error(f"Error in update_restoran_racun: {e}")
            return "Internal Server Error", 500
        
    def updated_restoran_racun(self, id):
        try:
            form = request.form
            restoran_racun = {
                'restoran_id': form['restoran_id'],
                'valuta': form['valuta'],
            }
            self.restoran_racun_service.update_restoran_racun(restoran_racun)
            return redirect(url_for('restoran_racun_routes.get_restoran_racun', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_restoran_racun: {e}")
            return "Internal Server Error", 500
        
    def delete_restoran_racun(self, id):
        try:
            self.restoran_racun_service.delete_restoran_racun(id)
            return redirect(url_for('restoran_racun_routes.get_restoran_racuni'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_restoran_racun: {e}")
            return "Internal Server Error", 500