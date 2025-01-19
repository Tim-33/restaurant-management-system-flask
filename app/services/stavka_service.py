from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import StavkaSqlRoutesEnum
import base64
from app.utils.decorators import with_db_connection

class StavkaService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_stavke(self):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            stavke = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv_recept': row[6],
                    'naziv': row[7],
                    'stavka_tip': row[8],
                    'cijena': row[9],
                    'opis': row[10],
                    'slika': base64.b64encode(row[11]).decode('utf-8') if row[11] else None
                } 
            for row in data]
            return stavke
        except Exception as e:
            self.app.logger.error(f"Error in get_stavke: {e}")
            raise e
        
    @with_db_connection
    def get_stavka(self, id):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            stavka = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'naziv_recept': data[6],
                'naziv': data[7],
                'stavka_tip': data[8],
                'cijena': data[9],
                'opis': data[10],
                'slika': base64.b64encode(data[11]).decode('utf-8') if data[11] else None
            }
            return stavka
        except Exception as e:
            self.app.logger.error(f"Error in get_stavka: {e}")
            raise e
        
    @with_db_connection
    def insert_stavka(self, stavka):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (stavka['restoran_id'], stavka['recept_id'], stavka['naziv'], stavka['stavka_tip'], stavka['cijena'], stavka['opis'], stavka['slika']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_stavka: {e}")
            raise e

    @with_db_connection        
    def update_stavka(self, stavka, id):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (stavka['restoran_id'], stavka['recept_id'], stavka['naziv'], stavka['stavka_tip'], stavka['cijena'], stavka['opis'], stavka['slika'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_stavka: {e}")
            raise e
    
    @with_db_connection    
    def delete_stavka(self, id):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_stavka: {e}")
            raise e
        
    @with_db_connection
    def get_stavke_by_racun(self, recun_id):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.SELECT_BY_RACUN.value)
            self.cursor.execute(sql_script, (recun_id,))
            data = self.cursor.fetchall()
            stavke = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv_recept': row[6],
                    'naziv': row[7],
                    'stavka_tip': row[8],
                    'cijena': row[9],
                    'opis': row[10],
                    'slika': base64.b64encode(row[11]).decode('utf-8') if row[11] else None,
                    'kolicina': row[12]
                } 
            for row in data]
            return stavke
        except Exception as e:
            self.app.logger.error(f"Error in get_stavke_by_racun: {e}")
            raise e
        
    @with_db_connection
    def get_stavke_by_jelovnik(self, jelovnik_id):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.SELECT_BY_JELOVNIK.value)
            self.cursor.execute(sql_script, (jelovnik_id,))
            data = self.cursor.fetchall()
            stavke = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv_recept': row[6],
                    'naziv': row[7],
                    'stavka_tip': row[8],
                    'cijena': row[9],
                    'opis': row[10],
                    'slika': base64.b64encode(row[11]).decode('utf-8') if row[11] else None,
                }
            for row in data]
            return stavke
        except Exception as e:
            self.app.logger.error(f"Error in get_stavke_by_jelovnik: {e}")
            raise e
        
    @with_db_connection
    def get_stavke_by_velika_nezgoda(self, velika_nezgoda_id):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.SELECT_BY_VELIKA_NEZGODA.value)
            self.cursor.execute(sql_script, (velika_nezgoda_id,))
            data = self.cursor.fetchall()
            stavke = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv_recept': row[6],
                    'naziv': row[7],
                    'stavka_tip': row[8],
                    'cijena': row[9],
                    'opis': row[10],
                    'slika': base64.b64encode(row[11]).decode('utf-8') if row[11] else None,
                    "kolicina": row[12]
                }
            for row in data]
            return stavke
        except Exception as e:
            self.app.logger.error(f"Error in get_stavke_by_velika_nezgoda: {e}")
            raise e
        
    @with_db_connection
    def get_stavke_most_expensive(self):
        try:
            sql_script = get_sql_script_from_file(StavkaSqlRoutesEnum.SELECT_MOST_EXPENSIVE.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            stavke = [
                {
                    'naziv_restoran': row[0],
                    'najskuplja_stavka': row[1],
                    'najvisa_cijena': row[2]
                }
            for row in data]
            return stavke
        except Exception as e:
            self.app.logger.error(f"Error in get_stavke_most_expensive: {e}")
            raise e