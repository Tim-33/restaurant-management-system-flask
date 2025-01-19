from flask import Flask, Blueprint, request, redirect, render_template, url_for
from app.interfaces.iroutes import IRoutes
from app.services.rezervacija_service import RezervacijaService
from app.services.restoran_service import RestoranService
from app.services.stol_service import StolService
from app.router.routes import RezervacijaRoutesEnum

class RezervacijaRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.rezervacija_service = RezervacijaService(self.app)
        self.restoran_service = RestoranService(self.app)
        self.stol_service = StolService(self.app)
        self.rezervacija_routes_bp = Blueprint('rezervacija_routes', __name__)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Rezervacija")
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA.value, methods=["GET"])(self.get_rezervacije)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_ID.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_ID.value, methods=["GET"])(self.get_rezervacija)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_CREATE.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_CREATE.value, methods=["GET"])(self.create_rezervacija)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_CREATED.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_CREATED.value, methods=["POST"])(self.created_rezervacija)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_UPDATE.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_UPDATE.value, methods=["GET"])(self.update_rezervacija)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_UPDATED.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_UPDATED.value, methods=["POST"])(self.updated_rezervacija)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_DELETE.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_DELETE.value, methods=["POST"])(self.delete_rezervacija)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_BY_LOCATION_WITH_COUNT.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_BY_LOCATION_WITH_COUNT.value, methods=["GET"])(self.get_rezervacija_by_location_with_count)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_WITH_STOL_DATA.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_WITH_STOL_DATA.value, methods=["GET"])(self.get_rezervacija_with_stol_data)
        self.app.logger.info(f"Registering route: {RezervacijaRoutesEnum.REZERVACIJA_COUNT_BY_STOL_LOCATION.value}")
        self.rezervacija_routes_bp.route(RezervacijaRoutesEnum.REZERVACIJA_COUNT_BY_STOL_LOCATION.value, methods=["GET"])(self.get_rezervacija_count_by_stol_location)
        self.app.register_blueprint(self.rezervacija_routes_bp)
        
    def get_rezervacije(self):
        try:
            data = self.rezervacija_service.get_rezervacije()
            return render_template(self.app.router.get_template(RezervacijaRoutesEnum.REZERVACIJA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_rezervacije: {e}")
            return "Internal Server Error", 500
        
    def get_rezervacija(self, id):
        try:
            data = self.rezervacija_service.get_rezervacija(id)
            return render_template(self.app.router.get_template(RezervacijaRoutesEnum.REZERVACIJA_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_rezervacija: {e}")
            return "Internal Server Error", 500
        
    def create_rezervacija(self):
        try:
            restorani = self.restoran_service.get_restorani()
            stolovi = self.stol_service.get_stolovi()
            return render_template(self.app.router.get_template(RezervacijaRoutesEnum.REZERVACIJA_CREATE.value), restorani=restorani, stolovi=stolovi)
        except Exception as e:
            self.app.logger.error(f"Error in create_rezervacija: {e}")
            return "Internal Server Error", 500
        
    def created_rezervacija(self):
        try:
            form = request.form
            rezervacija = {
                "restoran_id": form['restoran_id'],
                "stol_id": form['stol_id'],
                "ime": form['ime'],
                "vrijeme": form['vrijeme'],
                "broj_osoba": form['broj_osoba'],
            }
            self.rezervacija_service.insert_rezervacija(rezervacija)
            return redirect(url_for('rezervacija_routes.get_rezervacije'))
        except Exception as e:
            self.app.logger.error(f"Error in created_rezervacija: {e}")
            return "Internal Server Error", 500
        
    def update_rezervacija(self, id):
        try:
            data = self.rezervacija_service.get_rezervacija(id)
            restorani = self.restoran_service.get_restorani()
            stolovi = self.stol_service.get_stolovi()
            return render_template(self.app.router.get_template(RezervacijaRoutesEnum.REZERVACIJA_UPDATE.value), data=data, restorani=restorani, stolovi=stolovi)
        except Exception as e:
            self.app.logger.error(f"Error in update_rezervacija: {e}")
            return "Internal Server Error", 500
        
    def updated_rezervacija(self, id):
        try:
            form = request.form
            rezervacija = {
                "restoran_id": form['restoran_id'],
                "stol_id": form['stol_id'],
                "ime": form['ime'],
                "vrijeme": form['vrijeme'],
                "broj_osoba": form['broj_osoba'],
            }
            self.rezervacija_service.update_rezervacija(rezervacija, id)
            return redirect(url_for('rezervacija_routes.get_rezervacija', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_rezervacija: {e}")
            return "Internal Server Error", 500
        
    def delete_rezervacija(self, id):
        try:
            self.rezervacija_service.delete_rezervacija(id)
            return redirect(url_for('rezervacija_routes.get_rezervacije'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_rezervacija: {e}")
            return "Internal Server Error", 500
        
    def get_rezervacija_by_location_with_count(self):
        try:
            data = self.rezervacija_service.get_rezervacija_by_location_with_count()
            return render_template(self.app.router.get_template(RezervacijaRoutesEnum.REZERVACIJA_BY_LOCATION_WITH_COUNT.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_rezervacija_by_location_with_count: {e}")
            return "Internal Server Error", 500
        
    def get_rezervacija_with_stol_data(self):
        try:
            data = self.rezervacija_service.get_rezervacija_with_stol_data()
            return render_template(self.app.router.get_template(RezervacijaRoutesEnum.REZERVACIJA_WITH_STOL_DATA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_rezervacija_with_stol_data: {e}")
            return "Internal Server Error", 500
        
    def get_rezervacija_count_by_stol_location(self):
        try:
            data = self.rezervacija_service.get_rezervacija_count_by_stol_location()
            return render_template(self.app.router.get_template(RezervacijaRoutesEnum.REZERVACIJA_COUNT_BY_STOL_LOCATION.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_rezervacija_count_by_stol_location: {e}")
            return "Internal Server Error", 500