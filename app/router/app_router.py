from app.utils.routes_utils import generate_page_route
from app.router.routes import *

class AppRouter:
    def __init__(self):
        self.routes = {}

    def add_route(self, route, template):
        self.routes[route] = template

    def get_template(self, route):
        return generate_page_route(self.routes.get(route, None))
    
    def create_routes(self):
        # Add routes for App
        self.add_route(AppRoutesEnum.HOME.value, 'app/home.html')
        self.add_route(AppRoutesEnum.GET_LOGIN.value, 'app/login.html')
        
        # Add routes for Zaposlenik
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK.value, 'zaposlenik/zaposlenici.html')
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK_CREATE.value, 'zaposlenik/zaposlenik_create.html')
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK_ID.value, 'zaposlenik/zaposlenik.html')
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK_UPDATE.value, 'zaposlenik/zaposlenik_update.html')
        
        # Add routes for ZaposlenikPlaca
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE.value, 'zaposlenik_placa/zaposlenik_place.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_MONTH.value, 'zaposlenik_placa/zaposlenik_place_month.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_CREATE.value, 'zaposlenik_placa/zaposlenik_placa_create.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_ID.value, 'zaposlenik_placa/zaposlenik_placa.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_UPDATE.value, 'zaposlenik_placa/zaposlenik_place_update.html')
        
        # Add routes for Restoran
        self.add_route(RestoranRoutesEnum.RESTORAN.value, 'restoran/restorani.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_CREATE.value, 'restoran/restoran_create.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_ID.value, 'restoran/restoran.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_UPDATE.value, 'restoran/restoran_update.html')
        
        # Add routes for Skladiste
        self.add_route(SkladisteRoutesEnum.SKLADISTE.value, 'skladiste/skladista.html')
        self.add_route(SkladisteRoutesEnum.SKLADISTE_CREATE.value, 'skladiste/skladiste_create.html')
        self.add_route(SkladisteRoutesEnum.SKLADISTE_ID.value, 'skladiste/skladiste.html')
        self.add_route(SkladisteRoutesEnum.SKLADISTE_UPDATE.value, 'skladiste/skladiste_update.html')
        
        # Add routes for RestoranRacun
        self.add_route(RestoranRacunRoutesEnum.RESTORAN_RACUN.value, 'restoran_racun/restoran_racuni.html')
        self.add_route(RestoranRacunRoutesEnum.RESTORAN_RACUN_CREATE.value, 'restoran_racun/restoran_racun_create.html')
        self.add_route(RestoranRacunRoutesEnum.RESTORAN_RACUN_ID.value, 'restoran_racun/restoran_racun.html')
        self.add_route(RestoranRacunRoutesEnum.RESTORAN_RACUN_UPDATE.value, 'restoran_racun/restoran_racun_update.html')
        
        # Add routes for TransakcijaRestoran
        self.add_route(TransakcijaRestoranRoutesEnum.TRANSAKCIJA_RESTORAN.value, 'transakcija_restoran/transakcije_restoran.html')
        self.add_route(TransakcijaRestoranRoutesEnum.TRANSKACIJA_RESTORAN_ID.value, 'transakcija_restoran/transakcija_restoran.html')
        
        # Add routes for TransakcijaZaposlenik
        self.add_route(TransakcijaZaposlenikRoutesEnum.TRANSAKCIJA_ZAPOSLENIK.value, 'transakcija_zaposlenik/transakcije_zaposlenik.html')
        self.add_route(TransakcijaZaposlenikRoutesEnum.TRANSAKCIJA_ZAPOSLENIK_ID.value, 'transakcija_zaposlenik/transakcija_zaposlenik.html')
        
        # Add routes for Trosak
        self.add_route(TrosakRoutesEnum.TROSAK.value, 'trosak/troskovi.html')
        self.add_route(TrosakRoutesEnum.TROSAK_CREATE.value, 'trosak/trosak_create.html')
        self.add_route(TrosakRoutesEnum.TROSAK_ID.value, 'trosak/trosak.html')
        self.add_route(TrosakRoutesEnum.TROSAK_UPDATE.value, 'trosak/trosak_update.html')
        
        # Add routes for Stol
        self.add_route(StolRoutesEnum.STOL.value, 'stol/stolovi.html')
        self.add_route(StolRoutesEnum.STOL_CREATE.value, 'stol/stol_create.html')
        self.add_route(StolRoutesEnum.STOL_ID.value, 'stol/stol.html')
        self.add_route(StolRoutesEnum.STOL_UPDATE.value, 'stol/stol_update.html')   
        
        # Add routes for Rezervacija
        self.add_route(RezervacijaRoutesEnum.REZERVACIJA.value, 'rezervacija/rezervacije.html')
        self.add_route(RezervacijaRoutesEnum.REZERVACIJA_CREATE.value, 'rezervacija/rezervacija_create.html')
        self.add_route(RezervacijaRoutesEnum.REZERVACIJA_ID.value, 'rezervacija/rezervacija.html')
        self.add_route(RezervacijaRoutesEnum.REZERVACIJA_UPDATE.value, 'rezervacija/rezervacija_update.html')

        # Add routes for Racun
        self.add_route(RacunRoutesEnum.RACUN.value, 'racun/racuni.html')
        self.add_route(RacunRoutesEnum.RACUN_CREATE.value, 'racun/racun_create.html')
        self.add_route(RacunRoutesEnum.RACUN_ID.value, 'racun/racun.html')
        self.add_route(RacunRoutesEnum.RACUN_UPDATE.value, 'racun/racun_update.html')
        