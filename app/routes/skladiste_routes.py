from app.interfaces.iroutes import IRoutes
from flask import Blueprint, Flask, request, redirect, url_for, render_template
from app.services.skladiste_service import SkladisteService
from app.services.restoran_service import RestoranService
from app.router.routes import SkladisteRoutesEnum

class SkladisteRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.skladiste_routes_bp = Blueprint('skladiste_routes', __name__)
        self.skladiste_service = SkladisteService(self.app)
        self.restoran_service = RestoranService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Skladiste")
        self.app.logger.info(f"Registering route: {SkladisteRoutesEnum.SKLADISTE.value}")
        self.skladiste_routes_bp.route(SkladisteRoutesEnum.SKLADISTE.value, methods=["GET"])(self.get_skladista)
        self.app.logger.info(f"Registering route: {SkladisteRoutesEnum.SKLADISTE_ID.value}")
        self.skladiste_routes_bp.route(SkladisteRoutesEnum.SKLADISTE_ID.value, methods=["GET"])(self.get_skladiste)
        self.app.logger.info(f"Registering route: {SkladisteRoutesEnum.SKLADISTE_CREATE.value}")
        self.skladiste_routes_bp.route(SkladisteRoutesEnum.SKLADISTE_CREATE.value, methods=["GET"])(self.create_skladiste)
        self.app.logger.info(f"Registering route: {SkladisteRoutesEnum.SKLADISTE_CREATED.value}")
        self.skladiste_routes_bp.route(SkladisteRoutesEnum.SKLADISTE_CREATED.value, methods=["POST"])(self.created_skladiste)
        self.app.logger.info(f"Registering route: {SkladisteRoutesEnum.SKLADISTE_UPDATE.value}")
        self.skladiste_routes_bp.route(SkladisteRoutesEnum.SKLADISTE_UPDATE.value, methods=["GET"])(self.update_skladiste)
        self.app.logger.info(f"Registering route: {SkladisteRoutesEnum.SKLADISTE_UPDATED.value}")
        self.skladiste_routes_bp.route(SkladisteRoutesEnum.SKLADISTE_UPDATED.value, methods=["POST"])(self.updated_skladiste)
        self.app.logger.info(f"Registering route: {SkladisteRoutesEnum.SKLADISTE_DELETE.value}")
        self.skladiste_routes_bp.route(SkladisteRoutesEnum.SKLADISTE_DELETE.value, methods=["POST"])(self.delete_skladiste)
        self.app.register_blueprint(self.skladiste_routes_bp)
        
    def get_skladista(self):
        try:
            data = self.skladiste_service.get_skladista()
            return render_template(self.app.router.get_template(SkladisteRoutesEnum.SKLADISTE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_skladista: {e}")
            return "Internal Server Error", 500
        
    def get_skladiste(self, id):
        try:
            data = self.skladiste_service.get_skladiste(id)
            return render_template(self.app.router.get_template(SkladisteRoutesEnum.SKLADISTE_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_skladiste: {e}")
            return "Internal Server Error", 500
        
    def create_skladiste(self):
        try:
            data = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(SkladisteRoutesEnum.SKLADISTE_CREATE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in create_skladiste: {e}")
            return "Internal Server Error", 500
        
    def created_skladiste(self):
        try:
            form = request.form
            skladiste = {
                'restoran_id': form['restoran_id'],
            }
            
            self.skladiste_service.insert_skladiste(skladiste)
            return redirect(url_for('skladiste_routes.get_skladista'))
        except Exception as e:
            self.app.logger.error(f"Error in created_skladiste: {e}")
            return "Internal Server Error", 500
        
    def update_skladiste(self, id):
        try:
            data = self.skladiste_service.get_skladiste(id)
            restorani = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(SkladisteRoutesEnum.SKLADISTE_UPDATE.value), data=data, restorani=restorani)
        except Exception as e:
            self.app.logger.error(f"Error in update_skladiste: {e}")
            return "Internal Server Error", 500
        
    def updated_skladiste(self, id):
        try:
            form = request.form
            skladiste = {
                'restoran_id': form['restoran_id'],
            }
            self.skladiste_service.update_skladiste(skladiste, id)
            return redirect(url_for('skladiste_routes.get_skladiste', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_skladiste: {e}")
            return "Internal Server Error", 500
        
    def delete_skladiste(self, id):
        try:
            self.skladiste_service.delete_skladiste(id)
            return redirect(url_for('skladiste_routes.get_skladista'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_skladiste: {e}")
            return "Internal Server Error", 500