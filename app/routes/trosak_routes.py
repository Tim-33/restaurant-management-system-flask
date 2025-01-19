from flask import Flask, Blueprint, request, redirect, render_template, url_for
from app.services.trosak_service import TrosakService
from app.services.restoran_service import RestoranService
from app.interfaces.iroutes import IRoutes
from app.router.routes import TrosakRoutesEnum

class TrosakRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.trosak_routes_bp = Blueprint('trosak_routes', __name__)
        self.trosak_service = TrosakService(self.app)
        self.restoran_service = RestoranService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Trosak")
        self.app.logger.info(f"Registering route: {TrosakRoutesEnum.TROSAK.value}")
        self.trosak_routes_bp.route(TrosakRoutesEnum.TROSAK.value, methods=["GET"])(self.get_troskovi)
        self.app.logger.info(f"Registering route: {TrosakRoutesEnum.TROSAK_ID.value}")
        self.trosak_routes_bp.route(TrosakRoutesEnum.TROSAK_ID.value, methods=["GET"])(self.get_trosak)
        self.app.logger.info(f"Registering route: {TrosakRoutesEnum.TROSAK_CREATE.value}")
        self.trosak_routes_bp.route(TrosakRoutesEnum.TROSAK_CREATE.value, methods=["GET"])(self.create_trosak)
        self.app.logger.info(f"Registering route: {TrosakRoutesEnum.TROSAK_CREATED.value}")
        self.trosak_routes_bp.route(TrosakRoutesEnum.TROSAK_CREATED.value, methods=["POST"])(self.created_trosak)
        self.app.logger.info(f"Registering route: {TrosakRoutesEnum.TROSAK_UPDATE.value}")
        self.trosak_routes_bp.route(TrosakRoutesEnum.TROSAK_UPDATE.value, methods=["GET"])(self.update_trosak)
        self.app.logger.info(f"Registering route: {TrosakRoutesEnum.TROSAK_UPDATED.value}")
        self.trosak_routes_bp.route(TrosakRoutesEnum.TROSAK_UPDATED.value, methods=["POST"])(self.updated_trosak)
        self.app.logger.info(f"Registering route: {TrosakRoutesEnum.TROSAK_DELETE.value}")
        self.trosak_routes_bp.route(TrosakRoutesEnum.TROSAK_DELETE.value, methods=["POST"])(self.delete_trosak)
        self.app.logger.info(f"Registering route: {TrosakRoutesEnum.TROSAK_TOTAL.value}")
        self.trosak_routes_bp.route(TrosakRoutesEnum.TROSAK_TOTAL.value, methods=["GET"])(self.get_troskovi_total)
        self.app.register_blueprint(self.trosak_routes_bp)
        
    def get_troskovi(self):
        try:
            data = self.trosak_service.get_troskovi()
            return render_template(self.app.router.get_template(TrosakRoutesEnum.TROSAK.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_troskovi: {e}")
            return "Internal Server Error", 500
        
    def get_trosak(self, id):
        try:
            data = self.trosak_service.get_trosak(id)
            return render_template(self.app.router.get_template(TrosakRoutesEnum.TROSAK_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_trosak: {e}")
            return "Internal Server Error", 500
        
    def create_trosak(self):
        try:
            data = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(TrosakRoutesEnum.TROSAK_CREATE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in create_trosak: {e}")
            return "Internal Server Error", 500
        
    def created_trosak(self):
        try:
            form = request.form
            trosak = {
                'restoran_id': form['restoran_id'],
                'naziv': form['naziv'],
                'iznos': form['iznos'],
                'mjesecno': 1 if form.get('mjesecno') else 0,
            }
            id = self.trosak_service.insert_trosak(trosak)
            self.trosak_service.process_trosak_transaction(id)
            return redirect(url_for('trosak_routes.get_troskovi'))
        except Exception as e:
            self.app.logger.error(f"Error in created_trosak: {e}")
            return "Internal Server Error", 500
        
    def update_trosak(self, id):
        try:
            data = self.trosak_service.get_trosak(id)
            restorani = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(TrosakRoutesEnum.TROSAK_UPDATE.value), data=data, restorani=restorani)
        except Exception as e:
            self.app.logger.error(f"Error in update_trosak: {e}")
            return "Internal Server Error", 500
        
    def updated_trosak(self, id):
        try:
            form = request.form
            trosak = {
                'restoran_id': form['restoran_id'],
                'naziv': form['naziv'],
                'iznos': form['iznos'],
                'mjesecno': 1 if form.get('mjesecno') else 0,
            }
            self.trosak_service.update_trosak(trosak, id)
            return redirect(url_for('trosak_routes.get_trosak', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_trosak: {e}")
            return "Internal Server Error", 500
        
    def delete_trosak(self, id):
        try:
            self.trosak_service.delete_trosak(id)
            return redirect(url_for('trosak_routes.get_troskovi'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_trosak: {e}")
            return "Internal Server Error", 500
        
    def get_troskovi_total(self):
        try:
            data = self.trosak_service.get_troskovi_total()
            return render_template(self.app.router.get_template(TrosakRoutesEnum.TROSAK_TOTAL.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_troskovi_total: {e}")
            return "Internal Server Error", 500