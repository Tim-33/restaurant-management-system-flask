from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import RacunSqlRoutesEnum
from app.utils.decorators import with_db_connection

class RacunService():
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_racuni(self):
        try:
            sql_script = get_sql_script_from_file(RacunSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            racuni = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'broj_stola': row[5],
                    'naziv_restoran': row[6],
                    'naziv_zaposlenik': row[7],
                    'broj_racuna': row[8],
                    'napojnica': row[9],
                    'iznos': row[10],
                    'ukupna_vrijednost': row[11],
                }
            for row in data]
            return racuni
        except Exception as e:
            self.app.logger.error(f"Error in get_racuni: {e}")
            raise e
        
    @with_db_connection
    def get_racun(self, id):
        try:
            sql_script = get_sql_script_from_file(RacunSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            racun = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'broj_stola': data[5],
                'naziv_restoran': data[6],
                'naziv_zaposlenik': data[7],
                'broj_racuna': data[8],
                'napojnica': data[9],
                'iznos': data[10],
            }
            return racun
        except Exception as e:
            self.app.logger.error(f"Error in get_racun: {e}")
            raise e
        
    @with_db_connection
    def insert_racun_stavke(self, racun, stavke):
        try:
            sql_script = get_sql_script_from_file(RacunSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (racun['stol_id'], racun['restoran_id'], racun['zaposlenik_id'], racun['broj_racuna'], racun['napojnica']))
            racun_id = self.cursor.lastrowid
            for stavka in stavke:
                sql_script = get_sql_script_from_file(RacunSqlRoutesEnum.INSERT_STAVKE.value)
                self.cursor.execute(sql_script, (racun_id, stavka['stavka_id'], stavka['kolicina']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_racun_stavke: {e}")
            raise e
        
    @with_db_connection
    def get_racun_ukupna_vrijednost(self):
        try:
            sql_script = get_sql_script_from_file(RacunSqlRoutesEnum.SELECT_RACUN_UKUPNA_VRIJEDNOST.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            racun_ukupna_vrijednost = [{
                'id': row[0],
                'ukupna_vrijednost': row[1],
            } for row in data]
            return racun_ukupna_vrijednost
        except Exception as e:
            self.app.logger.error(f"Error in get_racun_ukupna_vrijednost: {e}")
            raise e
      
    @with_db_connection  
    def get_racun_by_zaposlenik(self, zaposlenik_id):
        try:
            sql_script = get_sql_script_from_file(RacunSqlRoutesEnum.SELECT_BY_ZAPOSLENIK.value)
            self.cursor.execute(sql_script, (zaposlenik_id,))
            data = self.cursor.fetchall()
            racuni = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'broj_stola': row[5],
                    'broj_racuna': row[6],
                    'napojnica': row[7],
                    'iznos': row[8],
                }
            for row in data]
            return racuni
        except Exception as e:
            self.app.logger.error(f"Error in get_racun_by_zaposlenik: {e}")
            raise e
        
    @with_db_connection
    def insert_racun_by_transaction(self, transaction):
        try:
            sql_script = get_sql_script_from_file(RacunSqlRoutesEnum.INSERT_BY_TRANSACTION.value)
            restoran_id = transaction['restoran_id']
            zaposlenik_id = transaction['zaposlenik_id']
            napojnica = transaction['napojnica']
            stol_id = transaction['stol_id']
            stavke = transaction['stavke']
            self.cursor.execute(sql_script, (
                restoran_id,
                zaposlenik_id,
                napojnica,
                stol_id,
                stavke
            ))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_racun_by_transaction: {e}")
            raise e