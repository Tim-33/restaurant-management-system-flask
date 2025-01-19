from app.interfaces.iroutes import IRoutes
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from app.router.routes import RestoranRoutesEnum
from app.services.restoran_service import RestoranService

class RestoranRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.restoran_routes_bp = Blueprint('restoran_routes', __name__)
        self.restoran_service = RestoranService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Restoran")
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN.value, methods=["GET"])(self.get_restorani)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_ID.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_ID.value, methods=["GET"])(self.get_restoran)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_CREATE.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_CREATE.value, methods=["GET"])(self.create_restoran)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_CREATED.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_CREATED.value, methods=["POST"])(self.created_restoran)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_UPDATE.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_UPDATE.value, methods=["GET"])(self.update_restoran)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_UPDATED.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_UPDATED.value, methods=["POST"])(self.updated_restoran)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_DELETE.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_DELETE.value, methods=["POST"])(self.delete_restoran)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_WITH_LEAST_REVENUE.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_WITH_LEAST_REVENUE.value, methods=["GET"])(self.get_restoran_with_least_revenue)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_WITH_ZAPOSLENIK_PAY_DATA.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_WITH_ZAPOSLENIK_PAY_DATA.value, methods=["GET"])(self.get_restoran_with_zaposlenik_pay_data)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_AVERAGE_EMPLOYEE_PAY.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_AVERAGE_EMPLOYEE_PAY.value, methods=["GET"])(self.get_restoran_average_employee_pay)
        self.app.logger.info(f"Registering route: {RestoranRoutesEnum.RESTORAN_NEZGODE_UKUPNO.value}")
        self.restoran_routes_bp.route(RestoranRoutesEnum.RESTORAN_NEZGODE_UKUPNO.value, methods=["GET"])(self.get_restorani_nezgode_ukupno)
        self.app.register_blueprint(self.restoran_routes_bp)
        
    def get_restorani(self):
        try:
            data = self.restoran_service.get_restorani()
            return render_template(self.app.router.get_template(RestoranRoutesEnum.RESTORAN.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_restorani: {e}")
            return "Internal Server Error", 500
        
    def get_restoran(self, id):
        try:
            data = self.restoran_service.get_restoran(id)
            return render_template(self.app.router.get_template(RestoranRoutesEnum.RESTORAN_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran: {e}")
            return "Internal Server Error", 500
    
    def create_restoran(self):
        try:
            return render_template(self.app.router.get_template(RestoranRoutesEnum.RESTORAN_CREATE.value))
        except Exception as e:
            self.app.logger.error(f"Error in create_restoran: {e}")
            return "Internal Server Error", 500
        
    def created_restoran(self):
        try:
            form = request.form
            file = request.files['slika']
            file_data = file.read()
            restoran = {
                'naziv': form['naziv'],
                'adresa': form['adresa'],
                'broj_telefona': form['broj_telefona'],
                'slika': file_data
            }
            self.restoran_service.insert_restoran(restoran)
            return redirect(RestoranRoutesEnum.RESTORAN.value)
        except Exception as e:
            self.app.logger.error(f"Error in created_restoran: {e}")
            return "Internal Server Error", 500
        
    def update_restoran(self, id):
        try:
            data = self.restoran_service.get_restoran(id)
            return render_template(self.app.router.get_template(RestoranRoutesEnum.RESTORAN_UPDATE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in update_restoran: {e}")
            return "Internal Server Error", 500
        
    def updated_restoran(self, id):
        try:
            form = request.form
            file = request.files['slika']
            file_data = file.read()
            restoran = {
                'naziv': form['naziv'],
                'adresa': form['adresa'],
                'broj_telefona': form['broj_telefona'],
                'slika': file_data
            }
            self.restoran_service.update_restoran(restoran, id)
            return redirect(url_for('restoran_routes.get_restoran', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_restoran: {e}")
            return "Internal Server Error", 500
        
    def delete_restoran(self, id):
        try:
            self.restoran_service.delete_restoran(id)
            return redirect(url_for('restoran_routes.get_restorani'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_restoran: {e}")
            return "Internal Server Error", 500
        
    def get_restoran_with_least_revenue(self):
        try:
            data = self.restoran_service.get_restoran_with_least_revenue()
            return render_template(self.app.router.get_template(RestoranRoutesEnum.RESTORAN_WITH_LEAST_REVENUE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_with_least_revenue: {e}")
            return "Internal Server Error", 500
        
    def get_restoran_with_zaposlenik_pay_data(self):
        try:
            data = self.restoran_service.get_restoran_with_zaposlenik_pay_data()
            return render_template(self.app.router.get_template(RestoranRoutesEnum.RESTORAN_WITH_ZAPOSLENIK_PAY_DATA.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_with_zaposlenik_pay_data: {e}")
            return "Internal Server Error", 500
        
    def get_restoran_average_employee_pay(self):
        try:
            data = self.restoran_service.get_restoran_average_employee_pay()
            return render_template(self.app.router.get_template(RestoranRoutesEnum.RESTORAN_AVERAGE_EMPLOYEE_PAY.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_average_employee_pay: {e}")
            return "Internal Server Error", 500
        
    def get_restorani_nezgode_ukupno(self):
        try:
            data = self.restoran_service.get_restorani_nezgode_ukupno()
            return render_template(self.app.router.get_template(RestoranRoutesEnum.RESTORAN_NEZGODE_UKUPNO.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_restorani_nezgode_ukupno: {e}")
            return "Internal Server Error", 500