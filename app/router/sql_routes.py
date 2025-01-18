from enum import Enum

class AuthSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/auth/select-all.sql'
    SELECT_ONE = 'sql/auth/select-one.sql'
    INSERT = 'sql/auth/insert.sql'
    UPDATE = 'sql/auth/update.sql'
    DELETE = 'sql/auth/delete.sql'
    
class ZaposlenikSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/zaposlenik/select-all.sql'
    SELECT_ONE = 'sql/zaposlenik/select-one.sql'
    INSERT = 'sql/zaposlenik/insert.sql'
    UPDATE = 'sql/zaposlenik/update.sql'
    DELETE = 'sql/zaposlenik/delete.sql'
    
class ZaposlenikPlacaSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/zaposlenik_placa/select-all.sql'
    SELECT_ONE = 'sql/zaposlenik_placa/select-one.sql'
    INSERT = 'sql/zaposlenik_placa/insert.sql'
    UPDATE = 'sql/zaposlenik_placa/update.sql'
    DELETE = 'sql/zaposlenik_placa/delete.sql'
    SELECT_BY_MONTH = "sql/zaposlenik_placa/select-by-month.sql"
    SELECT_MONTHS = "sql/zaposlenik_placa/select-months.sql"
    
class RestoranSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/restoran/select-all.sql'
    SELECT_ONE = 'sql/restoran/select-one.sql'
    INSERT = 'sql/restoran/insert.sql'
    UPDATE = 'sql/restoran/update.sql'
    DELETE = 'sql/restoran/delete.sql'
    
class SkladisteSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/skladiste/select-all.sql'
    SELECT_ONE = 'sql/skladiste/select-one.sql'
    INSERT = 'sql/skladiste/insert.sql'
    UPDATE = 'sql/skladiste/update.sql'
    DELETE = 'sql/skladiste/delete.sql'
    
class RestoranRacunSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/restoran_racun/select-all.sql'
    SELECT_ONE = 'sql/restoran_racun/select-one.sql'
    INSERT = 'sql/restoran_racun/insert.sql'
    UPDATE = 'sql/restoran_racun/update.sql'
    DELETE = 'sql/restoran_racun/delete.sql'
    
class TransakcijaRestoranSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/transakcija_restoran/select-all.sql'
    SELECT_ONE = 'sql/transakcija_restoran/select-one.sql'

class TransakcijaZaposlenikSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/transakcija_zaposlenik/select-all.sql'
    SELECT_ONE = 'sql/transakcija_zaposlenik/select-one.sql'

class TrosakSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/trosak/select-all.sql'
    SELECT_ONE = 'sql/trosak/select-one.sql'
    INSERT = 'sql/trosak/insert.sql'
    UPDATE = 'sql/trosak/update.sql'
    DELETE = 'sql/trosak/delete.sql'
    
class StolSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/stol/select-all.sql'
    SELECT_ONE = 'sql/stol/select-one.sql'
    INSERT = 'sql/stol/insert.sql'
    UPDATE = 'sql/stol/update.sql'
    DELETE = 'sql/stol/delete.sql'
    
class RezervacijaSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/rezervacija/select-all.sql'
    SELECT_ONE = 'sql/rezervacija/select-one.sql'
    INSERT = 'sql/rezervacija/insert.sql'
    UPDATE = 'sql/rezervacija/update.sql'
    DELETE = 'sql/rezervacija/delete.sql'
    
class RacunSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/racun/select-all.sql'
    SELECT_ONE = 'sql/racun/select-one.sql'
    INSERT = 'sql/racun/insert.sql'
    INSERT_STAVKE = 'sql/racun/insert-stavke.sql'
    
class ReceptSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/recept/select-all.sql'
    SELECT_ONE = 'sql/recept/select-one.sql'
    INSERT = 'sql/recept/insert.sql'
    UPDATE = 'sql/recept/update.sql'
    DELETE = 'sql/recept/delete.sql'
    INSERT_SASTOJCI = 'sql/recept/insert-sastojci.sql'
    DELETE_SASTOJCI = 'sql/recept/delete-sastojci.sql'
    SELECT_UKUPNI_PRIHOD = 'sql/recept/select-ukupni-prihod.sql'
    
class StavkaSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/stavka/select-all.sql'
    SELECT_ONE = 'sql/stavka/select-one.sql'
    INSERT = 'sql/stavka/insert.sql'
    UPDATE = 'sql/stavka/update.sql'
    DELETE = 'sql/stavka/delete.sql'
    SELECT_BY_RACUN = 'sql/stavka/select-by-racun.sql'
    SELECT_BY_JELOVNIK = 'sql/stavka/select-by-jelovnik.sql'
    SELECT_BY_VELIKA_NEZGODA = 'sql/stavka/select-by-velika-nezgoda.sql'
    
class JelovnikSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/jelovnik/select-all.sql'
    SELECT_ONE = 'sql/jelovnik/select-one.sql'
    INSERT = 'sql/jelovnik/insert.sql'
    INSERT_STAVKE = 'sql/jelovnik/insert-stavke.sql'
    UPDATE = 'sql/jelovnik/update.sql'
    DELETE = 'sql/jelovnik/delete.sql'
    DELETE_STAVKE = 'sql/jelovnik/delete-stavke.sql'
    
class SastojakSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/sastojak/select-all.sql'
    SELECT_ONE = 'sql/sastojak/select-one.sql'
    INSERT = 'sql/sastojak/insert.sql'
    UPDATE = 'sql/sastojak/update.sql'
    DELETE = 'sql/sastojak/delete.sql'
    SELECT_BY_RECEPT = 'sql/sastojak/select-by-recept.sql'
    SELECT_BY_NARUDZBA = 'sql/sastojak/select-by-narudzba.sql'
    SELECT_BY_SKLADISTE = 'sql/sastojak/select-by-skladiste.sql'
    SELECT_BY_MALA_NEZGODA = 'sql/sastojak/select-by-mala-nezgoda.sql'
    
class NarudzbaSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/narudzba/select-all.sql'
    SELECT_ONE = 'sql/narudzba/select-one.sql'
    INSERT = 'sql/narudzba/insert.sql'
    UPDATE = 'sql/narudzba/update.sql'
    DELETE = 'sql/narudzba/delete.sql'
    INSERT_SASTOJCI = 'sql/narudzba/insert-sastojci.sql'
    DELETE_SASTOJCI = 'sql/narudzba/delete-sastojci.sql'
    
class MalaNezgodaSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/mala_nezgoda/select-all.sql'
    SELECT_ONE = 'sql/mala_nezgoda/select-one.sql'
    INSERT = 'sql/mala_nezgoda/insert.sql'
    INSERT_SASTOJCI = 'sql/mala_nezgoda/insert-sastojci.sql'
    
class VelikaNezgodaSqlRoutesEnum(Enum):
    SELECT_ALL = 'sql/velika_nezgoda/select-all.sql'
    SELECT_ONE = 'sql/velika_nezgoda/select-one.sql'
    INSERT = 'sql/velika_nezgoda/insert.sql'
    INSERT_STAVKE = 'sql/velika_nezgoda/insert-stavke.sql'