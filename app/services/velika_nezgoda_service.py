from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import VelikaNezgodaSqlRoutesEnum

class VelikaNezgodaService:
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_velike_nezgode(self):
        try:
            sql_script = get_sql_script_from_file(VelikaNezgodaSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            velike_nezgode = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv_zaposlenik': row[6],
                    'ukupno': row[7]
                } 
            for row in data]
            return velike_nezgode
        except Exception as e:
            self.app.logger.error(f"Error in get_velike_nezgode: {e}")
            raise e
        
    def get_velika_nezgoda(self, id):
        try:
            sql_script = get_sql_script_from_file(VelikaNezgodaSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            velika_nezgoda = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'naziv_zaposlenik': data[6],
                'ukupno': data[7]
            }
            return velika_nezgoda
        except Exception as e:
            self.app.logger.error(f"Error in get_velika_nezgoda: {e}")
            raise e
        
    def insert_velika_nezgoda(self, velika_nezgoda):
        try:
            sql_script = get_sql_script_from_file(VelikaNezgodaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (velika_nezgoda['restoran_id'], velika_nezgoda['zaposlenik_id']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_velika_nezgoda: {e}")
            raise e
        
    def insert_velika_nezgoda_stavke(self, velika_nezgoda, stavke):
        try:
            sql_script = get_sql_script_from_file(VelikaNezgodaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (velika_nezgoda['restoran_id'], velika_nezgoda['zaposlenik_id']))
            velika_nezgoda_id = self.cursor.lastrowid
            sql_script = get_sql_script_from_file(VelikaNezgodaSqlRoutesEnum.INSERT_STAVKE.value)
            for stavka in stavke:
                self.cursor.execute(sql_script, (velika_nezgoda_id, stavka['stavka_id'], stavka['kolicina']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_velika_nezgoda_stavke: {e}")
            raise e