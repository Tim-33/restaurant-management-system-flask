from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import RestoranSqlRoutesEnum
import base64

class RestoranService:
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_restorani(self):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            restorani = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv': row[5],
                    'adresa': row[6],
                    'broj_telefona': row[7],
                    'slika': base64.b64encode(row[8]).decode('utf-8') if row[8] else None
                } 
            for row in data]
            return restorani
        except Exception as e:
            self.app.logger.error(f"Error in get_restorani: {e}")
            raise e
        
    def get_restoran(self, id):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            restoran = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv': data[5],
                'adresa': data[6],
                'broj_telefona': data[7],
                'slika': base64.b64encode(data[8]).decode('utf-8') if data[8] else None
            }
            return restoran
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran: {e}")
            raise e
        
    def insert_restoran(self, restoran):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (restoran['naziv'], restoran['adresa'], restoran['broj_telefona'], restoran['slika']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_restoran: {e}")
            raise e
        
    def update_restoran(self, restoran, id):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (restoran['naziv'], restoran['adresa'], restoran['broj_telefona'], restoran['slika'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_restoran: {e}")
            raise e
        
    def delete_restoran(self, id):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_restoran: {e}")
            raise e
        
    def get_restoran_with_least_revenue(self):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.SELECT_RESTORAN_WITH_LEAST_REVENUE.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchone()
            restoran = {
                'restoran': data[0],
                'iznos_na_racunu': data[1],
                'valuta': data[2]
            }
            return restoran
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_with_least_revenue: {e}")
            raise e