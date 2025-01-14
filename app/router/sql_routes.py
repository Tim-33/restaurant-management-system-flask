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
