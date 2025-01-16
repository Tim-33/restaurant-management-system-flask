from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import RacunSqlRoutesEnum

class RacunService():
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
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
                }
            for row in data]
            return racuni
        except Exception as e:
            self.app.logger.error(f"Error in get_racuni: {e}")
            raise e
        
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