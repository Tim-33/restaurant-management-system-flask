from flask import Flask, Blueprint, render_template, redirect, request
from app.interfaces.iroutes import IRoutes
from app.services.zaposlenik_placa_service import ZaposlenikPlacaService
from app.services.zaposlenik_service import ZaposlenikService
from app.router.routes import ZaposlenikPlacaRoutesEnum

class ZaposlenikPlacaRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.zaposlenik_placa_routes_bp = Blueprint('zaposlenik_placa_routes', __name__)
        self.zaposlenik_placa_service = ZaposlenikPlacaService(self.app)
        self.zaposlenik_service = ZaposlenikService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for ZaposlenikPlaca")
        self.app.logger.info(f"Registering route: {ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE.value}")
        self.zaposlenik_placa_routes_bp.route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE.value, methods=["GET"])(self.get_zaposlenik_place_months)
        self.app.logger.info(f"Registering route: {ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_MONTH.value}")
        self.zaposlenik_placa_routes_bp.route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_MONTH.value, methods=["GET"])(self.get_zaposlenik_place_by_month)
        self.app.logger.info(f"Registering route: {ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_ID.value}")
        self.zaposlenik_placa_routes_bp.route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_ID.value, methods=["GET"])(self.get_zaposlenik_placa)
        self.app.logger.info(f"Registering route: {ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_CREATE.value}")
        self.zaposlenik_placa_routes_bp.route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_CREATE.value, methods=["GET"])(self.create_zaposlenik_place)
        self.app.logger.info(f"Registering route: {ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_CREATED.value}")
        self.zaposlenik_placa_routes_bp.route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_CREATED.value, methods=["POST"])(self.created_zaposlenik_place)
        self.app.register_blueprint(self.zaposlenik_placa_routes_bp)  
        
    def get_zaposlenik_place_months(self):
        try:
            data = self.zaposlenik_placa_service.get_zaposlenik_place_months()
            return render_template(self.app.router.get_template(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenik_place_month: {e}")
            return "Internal Server Error", 500
        
    def get_zaposlenik_place_by_month(self):
        try:
            month = request.args.get('mjesec')
            month = f"{month}-01"
            data = self.zaposlenik_placa_service.get_zaposlenik_place_by_month(month)
            return render_template(self.app.router.get_template(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_MONTH.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenik_place_by_month: {e}")
            return "Internal Server Error", 500
       
    def get_zaposlenik_placa(self, id):
        try:
            data = self.zaposlenik_placa_service.get_zaposlenik_placa(id)
            return render_template(self.app.router.get_template(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_ID.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenik_placa: {e}")
            return "Internal Server Error", 500   
        
    def create_zaposlenik_place(self):
        try:
            data = self.zaposlenik_service.get_zaposlenici()
            return render_template(self.app.router.get_template(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_CREATE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in create_zaposlenik_place: {e}")
            return "Internal Server Error", 500
        
    def created_zaposlenik_place(self):
        try:
            form = request.form
            month = form["mjesec"]
            month = f"{month}-01"
            
            for key, value in form.items():
                if key.startswith('iznos_place_'):
                    zaposlenik_id = key.split('_')[2]
                    iznos_place = value
                    self.zaposlenik_placa_service.insert_zaposlenik_placa(zaposlenik_id, iznos_place, month)
            
            return redirect(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE.value)
        except Exception as e:
            self.app.logger.error(f"Error in created_zaposlenik_place: {e}")
            return "Internal Server Error", 500