from enum import Enum

class AppRoutesEnum(Enum):
    HOME = "/"
    GET_LOGIN = "/get-login"
    LOGIN = "/login"
    
class ZaposlenikRoutesEnum(Enum):
    ZAPOSLENIK = "/zaposlenici"
    ZAPOSLENIK_CREATE = "/zaposlenici/create"
    ZAPOSLENIK_CREATED = "/zaposlenici/created"
    ZAPOSLENIK_ID = "/zaposlenici/<int:id>"
    ZAPOSLENIK_UPDATE = "/zaposlenici/<int:id>/update"
    ZAPOSLENIK_UPDATED = "/zaposlenici/<int:id>/updated"
    ZAPOSLENIK_DELETE = "/zaposlenici/<int:id>/delete"
    ZAPOSLENIK_SELECT_WITH_PAY_FOR_JANUARY_AND_JUNE = "/zaposlenici/select-with-pay-for-january-and-june"
    
class ZaposlenikPlacaRoutesEnum(Enum):
    ZAPOSLENIK_PLACE = "/zaposlenik-place"
    ZAPOSLENIK_PLACE_MONTH = "/zaposlenik-place/month"
    ZAPOSLENIK_PLACE_CREATE = "/zaposlenik-place/create"
    ZAPOSLENIK_PLACE_CREATED = "/zaposlenik-place/created"
    ZAPOSLENIK_PLACE_ID = "/zaposlenik-place/<int:id>"
    ZAPOSLENIK_PLACE_UPDATE = "/zaposlenik-place/<int:id>/update"
    ZAPOSLENIK_PLACE_UPDATED = "/zaposlenik-place/<int:id>/updated"
    ZAPOSLENIK_PLACE_DELETE = "/zaposlenik-place/<int:id>/delete"
    
class RestoranRoutesEnum(Enum):
    RESTORAN = "/restorani"
    RESTORAN_CREATE = "/restorani/create"
    RESTORAN_CREATED = "/restorani/created"
    RESTORAN_ID = "/restorani/<int:id>"
    RESTORAN_UPDATE = "/restorani/<int:id>/update"
    RESTORAN_UPDATED = "/restorani/<int:id>/updated"
    RESTORAN_DELETE = "/restorani/<int:id>/delete"
    
class SkladisteRoutesEnum(Enum):
    SKLADISTE = "/skladista"
    SKLADISTE_CREATE = "/skladista/create"
    SKLADISTE_CREATED = "/skladista/created"
    SKLADISTE_ID = "/skladista/<int:id>"
    SKLADISTE_UPDATE = "/skladista/<int:id>/update"
    SKLADISTE_UPDATED = "/skladista/<int:id>/updated"
    SKLADISTE_DELETE = "/skladista/<int:id>/delete"
    
class RestoranRacunRoutesEnum(Enum):
    RESTORAN_RACUN = "/restoran-racuni"
    RESTORAN_RACUN_CREATE = "/restoran-racuni/create"
    RESTORAN_RACUN_CREATED = "/restoran-racuni/created"
    RESTORAN_RACUN_ID = "/restoran-racuni/<int:id>"
    RESTORAN_RACUN_UPDATE = "/restoran-racuni/<int:id>/update"
    RESTORAN_RACUN_UPDATED = "/restoran-racuni/<int:id>/updated"
    RESTORAN_RACUN_DELETE = "/restoran-racuni/<int:id>/delete"
    
class TransakcijaRestoranRoutesEnum(Enum):
    TRANSAKCIJA_RESTORAN = "/transakcije-restoran"
    TRANSKACIJA_RESTORAN_ID = "/transakcije-restoran/<int:id>"
    
class TransakcijaZaposlenikRoutesEnum(Enum):
    TRANSAKCIJA_ZAPOSLENIK = "/transakcije-zaposlenik"
    TRANSAKCIJA_ZAPOSLENIK_ID = "/transakcije-zaposlenik/<int:id>"
    
class TrosakRoutesEnum(Enum):
    TROSAK = "/troskovi"
    TROSAK_CREATE = "/troskovi/create"
    TROSAK_CREATED = "/troskovi/created"
    TROSAK_ID = "/troskovi/<int:id>"
    TROSAK_UPDATE = "/troskovi/<int:id>/update"
    TROSAK_UPDATED = "/troskovi/<int:id>/updated"
    TROSAK_DELETE = "/troskovi/<int:id>/delete"
    
class StolRoutesEnum(Enum):
    STOL = "/stolovi"
    STOL_CREATE = "/stolovi/create"
    STOL_CREATED = "/stolovi/created"
    STOL_ID = "/stolovi/<int:id>"
    STOL_UPDATE = "/stolovi/<int:id>/update"
    STOL_UPDATED = "/stolovi/<int:id>/updated"
    STOL_DELETE = "/stolovi/<int:id>/delete"
    
class RezervacijaRoutesEnum(Enum):
    REZERVACIJA = "/rezervacije"
    REZERVACIJA_CREATE = "/rezervacije/create"
    REZERVACIJA_CREATED = "/rezervacije/created"
    REZERVACIJA_ID = "/rezervacije/<int:id>"
    REZERVACIJA_UPDATE = "/rezervacije/<int:id>/update"
    REZERVACIJA_UPDATED = "/rezervacije/<int:id>/updated"
    REZERVACIJA_DELETE = "/rezervacije/<int:id>/delete"
    
class RacunRoutesEnum(Enum):
    RACUN = "/racuni"
    RACUN_CREATE = "/racuni/create"
    RACUN_CREATED = "/racuni/created"
    RACUN_ID = "/racuni/<int:id>"
    RACUN_UKUPNA_VRIJEDNOST = "/racuni/ukupna-vrijednost"
    
class ReceptRoutesEnum(Enum):
    RECEPT = "/recepti"
    RECEPT_CREATE = "/recepti/create"
    RECEPT_CREATED = "/recepti/created"
    RECEPT_ID = "/recepti/<int:id>"
    RECEPT_UPDATE = "/recepti/<int:id>/update"
    RECEPT_UPDATED = "/recepti/<int:id>/updated"
    RECEPT_DELETE = "/recepti/<int:id>/delete"
    RECEPT_UKUPNI_PRIHOD = "/recepti/ukupni-prihod"
    RECEPT_PRIHOD_PRVOG_RACUNA = "/recepti/prihod-prvog-racuna"
    RECEPT_SASTOJCI_PO_RECEPTU = "/recepti/sastojci-po-receptu"
    
class StavkaRoutesEnum(Enum):
    STAVKA = "/stavke"
    STAVKA_CREATE = "/stavke/create"
    STAVKA_CREATED = "/stavke/created"
    STAVKA_ID = "/stavke/<int:id>"
    STAVKA_UPDATE = "/stavke/<int:id>/update"
    STAVKA_UPDATED = "/stavke/<int:id>/updated"
    STAVKA_DELETE = "/stavke/<int:id>/delete"
    
class JelovnikRoutesEnum(Enum):
    JELOVNIK = "/jelovnici"
    JELOVNIK_CREATE = "/jelovnici/create"
    JELOVNIK_CREATED = "/jelovnici/created"
    JELOVNIK_ID = "/jelovnici/<int:id>"
    JELOVNIK_UPDATE = "/jelovnici/<int:id>/update"
    JELOVNIK_UPDATED = "/jelovnici/<int:id>/updated"
    JELOVNIK_DELETE = "/jelovnici/<int:id>/delete"
    
class SastojakRoutesEnum(Enum):
    SASTOJAK = "/sastojci"
    SASTOJAK_CREATE = "/sastojci/create"
    SASTOJAK_CREATED = "/sastojci/created"
    SASTOJAK_ID = "/sastojci/<int:id>"
    SASTOJAK_UPDATE = "/sastojci/<int:id>/update"
    SASTOJAK_UPDATED = "/sastojci/<int:id>/updated"
    SASTOJAK_DELETE = "/sastojci/<int:id>/delete"
    SASTOJAK_UKUPNA_KOLICINA = "/sastojci/ukupna-kolicina"
    
class NarudzbaRoutesEnum(Enum):
    NARUDZBA = "/narudzbe"
    NARUDZBA_CREATE = "/narudzbe/create"
    NARUDZBA_CREATED = "/narudzbe/created"
    NARUDZBA_ID = "/narudzbe/<int:id>"
    NARUDZBA_UPDATE = "/narudzbe/<int:id>/update"
    NARUDZBA_UPDATED = "/narudzbe/<int:id>/updated"
    NARUDZBA_DELETE = "/narudzbe/<int:id>/delete"
    
class MalaNezgodaRoutesEnum(Enum):
    MALA_NEZGODA = "/mala-nezgoda"
    MALA_NEZGODA_CREATE = "/mala-nezgoda/create"
    MALA_NEZGODA_CREATED = "/mala-nezgoda/created"
    MALA_NEZGODA_ID = "/mala-nezgoda/<int:id>"
    
class VelikaNezgodaRoutesEnum(Enum):
    VELIKA_NEZGODA = "/velika-nezgoda"
    VELIKA_NEZGODA_CREATE = "/velika-nezgoda/create"
    VELIKA_NEZGODA_CREATED = "/velika-nezgoda/created"
    VELIKA_NEZGODA_ID = "/velika-nezgoda/<int:id>"
    
class UserRoutesEnum(Enum):
    USER = "/users"