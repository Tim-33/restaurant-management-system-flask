from flask import Flask, request, Blueprint, render_template, redirect, url_for
from app.interfaces.iroutes import IRoutes
from app.router.routes import JelovnikRoutesEnum
from app.services.jelovnik_service import JelovnikService
from app.services.restoran_service import RestoranService
from app.services.stavka_service import StavkaService

class JelovnikRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.jelovnik_routes_bp = Blueprint("jelovnik_routes", __name__)
        self.jelovnik_service = JelovnikService(self.app)
        self.restoran_service = RestoranService(self.app)
        self.stavka_service = StavkaService(self.app)
        self.tipovi = ["pica", "jela", "desert"]
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Jelovnik")
        self.app.logger.info(f"Registering route: {JelovnikRoutesEnum.JELOVNIK.value}")
        self.jelovnik_routes_bp.route(JelovnikRoutesEnum.JELOVNIK.value, methods=["GET"])(self.get_jelovnici)
        self.app.logger.info(f"Registering route: {JelovnikRoutesEnum.JELOVNIK_ID.value}")
        self.jelovnik_routes_bp.route(JelovnikRoutesEnum.JELOVNIK_ID.value, methods=["GET"])(self.get_jelovnik)
        self.app.logger.info(f"Registering route: {JelovnikRoutesEnum.JELOVNIK_CREATE.value}")
        self.jelovnik_routes_bp.route(JelovnikRoutesEnum.JELOVNIK_CREATE.value, methods=["GET"])(self.create_jelovnik)
        self.app.logger.info(f"Registering route: {JelovnikRoutesEnum.JELOVNIK_CREATED.value}")
        self.jelovnik_routes_bp.route(JelovnikRoutesEnum.JELOVNIK_CREATED.value, methods=["POST"])(self.created_jelovnik)
        self.app.logger.info(f"Registering route: {JelovnikRoutesEnum.JELOVNIK_UPDATE.value}")
        self.jelovnik_routes_bp.route(JelovnikRoutesEnum.JELOVNIK_UPDATE.value, methods=["GET"])(self.update_jelovnik)
        self.app.logger.info(f"Registering route: {JelovnikRoutesEnum.JELOVNIK_UPDATED.value}")
        self.jelovnik_routes_bp.route(JelovnikRoutesEnum.JELOVNIK_UPDATED.value, methods=["POST"])(self.updated_jelovnik)
        self.app.logger.info(f"Registering route: {JelovnikRoutesEnum.JELOVNIK_DELETE.value}")
        self.jelovnik_routes_bp.route(JelovnikRoutesEnum.JELOVNIK_DELETE.value, methods=["POST"])(self.delete_jelovnik)
        self.app.register_blueprint(self.jelovnik_routes_bp)
        
    def get_jelovnici(self):
        try:
            data = self.jelovnik_service.get_jelovnici()
            return render_template(self.app.router.get_template(JelovnikRoutesEnum.JELOVNIK.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_jelovnici: {e}")
            return "Internal Server Error", 500
        
    def get_jelovnik(self, id):
        try:
            data = self.jelovnik_service.get_jelovnik(id)
            stavke = self.stavka_service.get_stavke_by_jelovnik(id)
            return render_template(self.app.router.get_template(JelovnikRoutesEnum.JELOVNIK_ID.value), data=data, stavke=stavke)
        except Exception as e:
            self.app.logger.error(f"Error in get_jelovnik: {e}")
            return "Internal Server Error", 500
        
    def create_jelovnik(self):
        try:
            restorani = self.restoran_service.get_restorani()
            stavke = self.stavka_service.get_stavke()
            return render_template(self.app.router.get_template(JelovnikRoutesEnum.JELOVNIK_CREATE.value), restorani=restorani, tipovi=self.tipovi, stavke=stavke)
        except Exception as e:
            self.app.logger.error(f"Error in create_jelovnik: {e}")
            return "Internal Server Error", 500
        
    def created_jelovnik(self):
        try:
            jelovnik = {
                'restoran_id': request.form['restoran_id'],
                'naziv': request.form['naziv'],
                'jelovnik_tip': request.form['jelovnik_tip']
            }
            
            stavke = []
            for key, value in request.form.items():
                if key.startswith('stavka_') and value == "on":
                    stavka_id = key.split('_')[1]
                    stavke.append({
                        'stavka_id': stavka_id,
                    })
                       
            self.jelovnik_service.insert_jelovnik_stavke(jelovnik, stavke)
            return redirect(url_for('jelovnik_routes.get_jelovnici'))
        except Exception as e:
            self.app.logger.error(f"Error in created_jelovnik: {e}")
            return "Internal Server Error", 500
        
    def update_jelovnik(self, id):
        try:
            data = self.jelovnik_service.get_jelovnik(id)
            restorani = self.restoran_service.get_restorani()
            stavke = self.stavka_service.get_stavke()
            jelovnik_stavke = self.stavka_service.get_stavke_by_jelovnik(id)
            return render_template(self.app.router.get_template(JelovnikRoutesEnum.JELOVNIK_UPDATE.value), data=data, restorani=restorani, tipovi=self.tipovi, stavke=stavke, jelovnik_stavke_ids = [stavka['id'] for stavka in jelovnik_stavke])
        except Exception as e:
            self.app.logger.error(f"Error in update_jelovnik: {e}")
            return "Internal Server Error", 500
        
    def updated_jelovnik(self, id):
        try:
            jelovnik = {
                'restoran_id': request.form['restoran_id'],
                'naziv': request.form['naziv'],
                'jelovnik_tip': request.form['jelovnik_tip']
            }
            
            jelvonik_stavke_update = []
            for key, value in request.form.items():
                if key.startswith('stavka_') and value == "on":
                    stavka_id = key.split('_')[1]
                    jelvonik_stavke_update.append({
                        'stavka_id': stavka_id,
                    })
                    
            jelovnik_stavke = self.stavka_service.get_stavke_by_jelovnik(id)
                       
            self.jelovnik_service.update_jelovnik_stavke(id, jelovnik, jelovnik_stavke, jelvonik_stavke_update)
            return redirect(url_for('jelovnik_routes.get_jelovnik', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_jelovnik: {e}")
            return "Internal Server Error", 500
        
    def delete_jelovnik(self, id):
        try:
            self.jelovnik_service.delete_jelovnik(id)
            return redirect(url_for('jelovnik_routes.get_jelovnici'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_jelovnik: {e}")
            return "Internal Server Error", 500