from app.interfaces.iroutes import IRoutes
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from app.router.routes import StolRoutesEnum
from app.services.stol_service import StolService
from app.services.restoran_service import RestoranService

class StolRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.stol_routes_bp = Blueprint('stol_routes', __name__)
        self.stol_service = StolService(self.app)
        self.restoran_service = RestoranService(self.app)
        self.lokacije = ['unutra', 'vani', 'vip']
    
    def register_routes(self):
        self.app.logger.info("Registering routes for Stol")
        self.app.logger.info(f"Registering route: {StolRoutesEnum.STOL.value}")
        self.stol_routes_bp.route(StolRoutesEnum.STOL.value, methods=["GET"])(self.get_stolovi)
        self.app.logger.info(f"Registering route: {StolRoutesEnum.STOL_ID.value}")
        self.stol_routes_bp.route(StolRoutesEnum.STOL_ID.value, methods=["GET"])(self.get_stol)
        self.app.logger.info(f"Registering route: {StolRoutesEnum.STOL_CREATE.value}")
        self.stol_routes_bp.route(StolRoutesEnum.STOL_CREATE.value, methods=["GET"])(self.create_stol)
        self.app.logger.info(f"Registering route: {StolRoutesEnum.STOL_CREATED.value}")
        self.stol_routes_bp.route(StolRoutesEnum.STOL_CREATED.value, methods=["POST"])(self.created_stol)
        self.app.logger.info(f"Registering route: {StolRoutesEnum.STOL_UPDATE.value}")
        self.stol_routes_bp.route(StolRoutesEnum.STOL_UPDATE.value, methods=["GET"])(self.update_stol)
        self.app.logger.info(f"Registering route: {StolRoutesEnum.STOL_UPDATED.value}")
        self.stol_routes_bp.route(StolRoutesEnum.STOL_UPDATED.value, methods=["POST"])(self.updated_stol)
        self.app.logger.info(f"Registering route: {StolRoutesEnum.STOL_DELETE.value}")
        self.stol_routes_bp.route(StolRoutesEnum.STOL_DELETE.value, methods=["POST"])(self.delete_stol)
        self.app.register_blueprint(self.stol_routes_bp)
        
    def get_stolovi(self):
        try:
            data = self.stol_service.get_stolovi()
            return render_template(self.app.router.get_template(StolRoutesEnum.STOL.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_stolovi: {e}")
            return "Internal Server Error", 500
        
    def get_stol(self, id):
        try:
            data = self.stol_service.get_stol(id)
            return render_template(self.app.router.get_template(StolRoutesEnum.STOL_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_stol: {e}")
            return "Internal Server Error", 500
        
    def create_stol(self):
        try:
            restorani = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(StolRoutesEnum.STOL_CREATE.value), restorani=restorani, lokacije=self.lokacije)
        except Exception as e:
            self.app.logger.error(f"Error in create_stol: {e}")
            return "Internal Server Error", 500
        
    def created_stol(self):
        try:
            form = request.form
            stol = {
                'restoran_id': form['restoran_id'],
                'broj': form['broj'],
                'lokacija': form['lokacija'],
                'broj_mjesta': form['broj_mjesta'],
            }
            self.stol_service.insert_stol(stol)
            return redirect(url_for('stol_routes.get_stolovi'))
        except Exception as e:
            self.app.logger.error(f"Error in created_stol: {e}")
            return "Internal Server Error", 500
        
    def update_stol(self, id):
        try:
            data = self.stol_service.get_stol(id)
            restorani = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(StolRoutesEnum.STOL_UPDATE.value), data=data, restorani=restorani, lokacije=self.lokacije)
        except Exception as e:
            self.app.logger.error(f"Error in update_stol: {e}")
            return "Internal Server Error", 500
        
    def updated_stol(self, id):
        try:
            form = request.form
            stol = {
                'restoran_id': form['restoran_id'],
                'broj': form['broj'],
                'lokacija': form['lokacija'],
                'broj_mjesta': form['broj_mjesta'],
            }
            self.stol_service.update_stol(stol, id)
            return redirect(url_for('stol_routes.get_stol', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_stol: {e}")
            return "Internal Server Error", 500
        
    def delete_stol(self, id):
        try:
            self.stol_service.delete_stol(id)
            return redirect(url_for('stol_routes.get_stolovi'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_stol: {e}")
            return "Internal Server Error", 500
        