from flask import Blueprint, render_template, Flask, redirect, url_for, request, jsonify
from app.interfaces.iroutes import IRoutes
from app.services.zaposlenik_service import ZaposlenikService
from app.services.restoran_service import RestoranService
from app.services.racun_service import RacunService
from app.router.routes import ZaposlenikRoutesEnum
import base64

class ZaposlenikRoutes(IRoutes):
    def __init__(self, app: Flask):
        self.app = app
        self.zaposlenik_routes_bp = Blueprint('zaposlenik_routes', __name__)
        self.zaposlenik_service = ZaposlenikService(self.app)
        self.restorna_service = RestoranService(self.app)
        self.racun_service = RacunService(self.app)
        
    def register_routes(self):
        self.app.logger.info("Registering routes for Zaposlenik")
        self.app.logger.info(f"Registering route: {ZaposlenikRoutesEnum.ZAPOSLENIK.value}")
        self.zaposlenik_routes_bp.route(ZaposlenikRoutesEnum.ZAPOSLENIK.value, methods=["GET"])(self.get_zaposlenici)
        self.app.logger.info(f"Registering route: {ZaposlenikRoutesEnum.ZAPOSLENIK_ID.value}")
        self.zaposlenik_routes_bp.route(ZaposlenikRoutesEnum.ZAPOSLENIK_ID.value, methods=["GET"])(self.get_zaposlenik)
        self.app.logger.info(f"Registering route: {ZaposlenikRoutesEnum.ZAPOSLENIK_CREATE.value}")
        self.zaposlenik_routes_bp.route(ZaposlenikRoutesEnum.ZAPOSLENIK_CREATE.value, methods=["GET"])(self.create_zaposlenik)
        self.app.logger.info(f"Registering route: {ZaposlenikRoutesEnum.ZAPOSLENIK_CREATED.value}")
        self.zaposlenik_routes_bp.route(ZaposlenikRoutesEnum.ZAPOSLENIK_CREATED.value, methods=["POST"])(self.created_zaposlenik)
        self.app.logger.info(f"Registering route: {ZaposlenikRoutesEnum.ZAPOSLENIK_UPDATE.value}")
        self.zaposlenik_routes_bp.route(ZaposlenikRoutesEnum.ZAPOSLENIK_UPDATE.value, methods=["GET"])(self.update_zaposlenik)
        self.app.logger.info(f"Registering route: {ZaposlenikRoutesEnum.ZAPOSLENIK_UPDATED.value}")
        self.zaposlenik_routes_bp.route(ZaposlenikRoutesEnum.ZAPOSLENIK_UPDATED.value, methods=["POST"])(self.updated_zaposlenik)
        self.app.logger.info(f"Registering route: {ZaposlenikRoutesEnum.ZAPOSLENIK_DELETE.value}")
        self.zaposlenik_routes_bp.route(ZaposlenikRoutesEnum.ZAPOSLENIK_DELETE.value, methods=["POST"])(self.delete_zaposlenik)
        self.app.register_blueprint(self.zaposlenik_routes_bp)
        
    def get_zaposlenici(self):
        try:
            data = self.zaposlenik_service.get_zaposlenici()
            return render_template(self.app.router.get_template(ZaposlenikRoutesEnum.ZAPOSLENIK.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenici: {e}")
            return "Internal Server Error", 500
        
    def get_zaposlenik(self, id):
        try:
            data = self.zaposlenik_service.get_zaposlenik(id)
            racuni = self.racun_service.get_racun_by_zaposlenik(id)
            return render_template(self.app.router.get_template(ZaposlenikRoutesEnum.ZAPOSLENIK_ID.value), data=data, racuni=racuni)
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenik: {e}")
            return "Internal Server Error", 500
        
    def create_zaposlenik(self):
        try:
            data = self.restorna_service.get_restorani()
            return render_template(self.app.router.get_template(ZaposlenikRoutesEnum.ZAPOSLENIK_CREATE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in create_zaposlenik: {e}")
            return "Internal Server Error", 500
        
    def created_zaposlenik(self):
        try:
            file = request.files['slika']
            file_data = file.read()
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            
            form = request.form

            body = {
                "restoran_id": form["restoran_id"],
                "zaposlenik_tip": form["zaposlenik_tip"],
                "ime": form["ime"],
                "prezime": form["prezime"],
                "email": form["email"],
                "datum_rodenja": form["datum_rodenja"],
                "iznos_place": form["iznos_place"],
                "slika": encoded_file
            }
            
            result = self.zaposlenik_service.insert_zaposlenik(body)
            
            if not result:
                return "Internal Server Error", 500
            
            return redirect(url_for('zaposlenik_routes.get_zaposlenici'))
        except Exception as e:
            self.app.logger.error(f"Error in created_zaposlenik: {e}")
            return "Internal Server Error", 500
        
    def update_zaposlenik(self, id):
        try:
            data = self.zaposlenik_service.get_zaposlenik(id)
            return render_template(self.app.router.get_template(ZaposlenikRoutesEnum.ZAPOSLENIK_UPDATE.value), data=data)
        except Exception as e:
            self.app.logger.error(f"Error in update_zaposlenik: {e}")
            return "Internal Server Error", 500
        
    def updated_zaposlenik(self, id):
        try:
            file = request.files['slika']
            file_data = file.read()
            encoded_file = base64.b64encode(file_data).decode('utf-8') if file else None
            
            body = {
                "restoran_id": request.form.get('restoran_id'),
                "zaposlenik_tip": request.form.get('zaposlenik_tip'),
                "ime": request.form.get('ime'),
                "prezime": request.form.get('prezime'),
                "email": request.form.get('email'),
                "datum_rodenja": request.form.get('datum_rodenja'),
                "iznos_place": request.form.get('iznos_place'),
                "slika": encoded_file
            }
            
            result = self.zaposlenik_service.update_zaposlenik(body, id)
            
            if not result:
                return "Internal Server Error", 500
            
            return redirect(url_for('zaposlenik_routes.get_zaposlenik', id=id))
        except Exception as e:
            self.app.logger.error(f"Error in updated_zaposlenik: {e}")
            return "Internal Server Error", 500
        
    def delete_zaposlenik(self, id):
        try:
            result = self.zaposlenik_service.delete_zaposlenik(id)
            
            if not result:
                return "Internal Server Error", 500
            
            return redirect(url_for('zaposlenik_routes.get_zaposlenici'))
        except Exception as e:
            self.app.logger.error(f"Error in delete_zaposlenik: {e}")
            return "Internal Server Error", 500