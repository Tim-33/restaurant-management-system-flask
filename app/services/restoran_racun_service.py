from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import RestoranRacunSqlRoutesEnum

class RestoranRacunService():
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_restoran_racuni(self):
        try:
            sql_script = get_sql_script_from_file(RestoranRacunSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            restoran_racuni = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv': row[5],
                    'stanje': row[6],
                    'valuta': row[7],
                } 
            for row in data]
            return restoran_racuni
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_racuni: {e}")
            raise e
        
    def get_restoran_racun(self, id):
        try:
            sql_script = get_sql_script_from_file(RestoranRacunSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            restoran_racun = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv': data[5],
                'stanje': data[6],
                'valuta': data[7],
            }
            return restoran_racun
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_racun: {e}")
            raise e
        
    def insert_restoran_racun(self, restoran_racun):
        try:
            sql_script = get_sql_script_from_file(RestoranRacunSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (restoran_racun['restoran_id'], restoran_racun['valuta']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_restoran_racun: {e}")
            raise e
        
    def update_restoran_racun(self, restoran_racun):
        try:
            sql_script = get_sql_script_from_file(RestoranRacunSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (restoran_racun['restoran_id'], restoran_racun['valuta']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_restoran_racun: {e}")
            raise e
        
    def delete_restoran_racun(self, id):
        try:
            sql_script = get_sql_script_from_file(RestoranRacunSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_restoran_racun: {e}")
            raise e