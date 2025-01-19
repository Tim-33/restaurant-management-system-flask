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
        self.add_route(ZaposlenikRoutesEnum.ZAPOSLENIK_SELECT_WITH_PAY_FOR_JANUARY_AND_JUNE.value, 'zaposlenik/zaposlenik_select_with_pay_for_january_and_june.html')
        
        # Add routes for ZaposlenikPlaca
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE.value, 'zaposlenik_placa/zaposlenik_place.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_MONTH.value, 'zaposlenik_placa/zaposlenik_place_month.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_CREATE.value, 'zaposlenik_placa/zaposlenik_placa_create.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_ID.value, 'zaposlenik_placa/zaposlenik_placa.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACE_UPDATE.value, 'zaposlenik_placa/zaposlenik_place_update.html')
        self.add_route(ZaposlenikPlacaRoutesEnum.ZAPOSLENIK_PLACA_ALL.value, 'zaposlenik_placa/zaposlenik_placa_all.html')
        
        # Add routes for Restoran
        self.add_route(RestoranRoutesEnum.RESTORAN.value, 'restoran/restorani.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_CREATE.value, 'restoran/restoran_create.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_ID.value, 'restoran/restoran.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_UPDATE.value, 'restoran/restoran_update.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_WITH_LEAST_REVENUE.value, 'restoran/restoran_with_least_revenue.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_WITH_ZAPOSLENIK_PAY_DATA.value, 'restoran/restoran_with_zaposlenik_pay_data.html')
        self.add_route(RestoranRoutesEnum.RESTORAN_AVERAGE_EMPLOYEE_PAY.value, 'restoran/restoran_average_employee_pay.html')
        
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
        self.add_route(TrosakRoutesEnum.TROSAK_TOTAL.value, 'trosak/trosak_total.html')
        
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
        self.add_route(RezervacijaRoutesEnum.REZERVACIJA_BY_LOCATION_WITH_COUNT.value, 'rezervacija/rezervacija_by_location_with_count.html')
        self.add_route(RezervacijaRoutesEnum.REZERVACIJA_WITH_STOL_DATA.value, 'rezervacija/rezervacija_with_stol_data.html')
        self.add_route(RezervacijaRoutesEnum.REZERVACIJA_COUNT_BY_STOL_LOCATION.value, 'rezervacija/rezervacija_count_by_stol_location.html')
        self.add_route(RezervacijaRoutesEnum.REZERVACIJA_ACTIVE_WITH_STOL_DATA.value, 'rezervacija/rezervacija_active_with_stol_data.html')

        # Add routes for Racun
        self.add_route(RacunRoutesEnum.RACUN.value, 'racun/racuni.html')
        self.add_route(RacunRoutesEnum.RACUN_CREATE.value, 'racun/racun_create.html')
        self.add_route(RacunRoutesEnum.RACUN_ID.value, 'racun/racun.html')
        self.add_route(RacunRoutesEnum.RACUN_UKUPNA_VRIJEDNOST.value, 'racun/racun_ukupna_vrijednost.html')
        
        # Add routes for Recept
        self.add_route(ReceptRoutesEnum.RECEPT.value, 'recept/recepti.html')
        self.add_route(ReceptRoutesEnum.RECEPT_CREATE.value, 'recept/recept_create.html')
        self.add_route(ReceptRoutesEnum.RECEPT_ID.value, 'recept/recept.html')
        self.add_route(ReceptRoutesEnum.RECEPT_UPDATE.value, 'recept/recept_update.html')
        self.add_route(ReceptRoutesEnum.RECEPT_UKUPNI_PRIHOD.value, 'recept/recept_ukupni_prihod.html')
        self.add_route(ReceptRoutesEnum.RECEPT_PRIHOD_PRVOG_RACUNA.value, 'recept/recept_prihod_prvog_racuna.html')
        self.add_route(ReceptRoutesEnum.RECEPT_SASTOJCI_PO_RECEPTU.value, 'recept/recept_sastojci_po_receptu.html')
        
        # Add routes for Stavka
        self.add_route(StavkaRoutesEnum.STAVKA.value, 'stavka/stavke.html')
        self.add_route(StavkaRoutesEnum.STAVKA_CREATE.value, 'stavka/stavka_create.html')
        self.add_route(StavkaRoutesEnum.STAVKA_ID.value, 'stavka/stavka.html')
        self.add_route(StavkaRoutesEnum.STAVKA_UPDATE.value, 'stavka/stavka_update.html')
        self.add_route(StavkaRoutesEnum.STAVKA_MOST_EXPENSIVE.value, 'stavka/stavka_most_expensive.html')
        self.add_route(StavkaRoutesEnum.STAVKA_COUNT_BY_TIP_AND_RESTORAN.value, 'stavka/stavka_count_by_tip_and_restoran.html')
        
        # Add routes for Jelovnik
        self.add_route(JelovnikRoutesEnum.JELOVNIK.value, 'jelovnik/jelovnici.html')
        self.add_route(JelovnikRoutesEnum.JELOVNIK_CREATE.value, 'jelovnik/jelovnik_create.html')
        self.add_route(JelovnikRoutesEnum.JELOVNIK_ID.value, 'jelovnik/jelovnik.html')
        self.add_route(JelovnikRoutesEnum.JELOVNIK_UPDATE.value, 'jelovnik/jelovnik_update.html')
        self.add_route(JelovnikRoutesEnum.JELOVNIK_WITH_STAVKA_COUNT.value, 'jelovnik/jelovnik_with_stavka_count.html')
        self.add_route(JelovnikRoutesEnum.JELOVNIK_STAVKE_TIPA_JELA.value, 'jelovnik/jelovnik_stavke_tipa_jela.html')
        
        # Add routes for Sastojak
        self.add_route(SastojakRoutesEnum.SASTOJAK.value, 'sastojak/sastojci.html')
        self.add_route(SastojakRoutesEnum.SASTOJAK_CREATE.value, 'sastojak/sastojak_create.html')
        self.add_route(SastojakRoutesEnum.SASTOJAK_ID.value, 'sastojak/sastojak.html')
        self.add_route(SastojakRoutesEnum.SASTOJAK_UPDATE.value, 'sastojak/sastojak_update.html')
        self.add_route(SastojakRoutesEnum.SASTOJAK_UKUPNA_KOLICINA.value, 'sastojak/sastojak_ukupna_kolicina.html')
        self.add_route(SastojakRoutesEnum.SASTOJAK_MOST_COMMON.value, 'sastojak/sastojak_most_common.html')
        
        # Add routes for Narudzba
        self.add_route(NarudzbaRoutesEnum.NARUDZBA.value, 'narudzba/narudzbe.html')
        self.add_route(NarudzbaRoutesEnum.NARUDZBA_CREATE.value, 'narudzba/narudzba_create.html')
        self.add_route(NarudzbaRoutesEnum.NARUDZBA_ID.value, 'narudzba/narudzba.html')
        self.add_route(NarudzbaRoutesEnum.NARUDZBA_UPDATE.value, 'narudzba/narudzba_update.html')
        
        # Add routes for MalaNezgoda
        self.add_route(MalaNezgodaRoutesEnum.MALA_NEZGODA.value, 'mala_nezgoda/male_nezgode.html')
        self.add_route(MalaNezgodaRoutesEnum.MALA_NEZGODA_CREATE.value, 'mala_nezgoda/mala_nezgoda_create.html')
        self.add_route(MalaNezgodaRoutesEnum.MALA_NEZGODA_ID.value, 'mala_nezgoda/mala_nezgoda.html')
        
        # Add routes for VelikaNezgoda
        self.add_route(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA.value, 'velika_nezgoda/velike_nezgode.html')
        self.add_route(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_CREATE.value, 'velika_nezgoda/velika_nezgoda_create.html')
        self.add_route(VelikaNezgodaRoutesEnum.VELIKA_NEZGODA_ID.value, 'velika_nezgoda/velika_nezgoda.html')
        
        # Add routes for User
        self.add_route(UserRoutesEnum.USER.value, 'user/users.html')