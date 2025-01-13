from flask import Flask
from app.router.sql_routes import SkladisteSqlRoutesEnum
from app.utils.sql_utils import get_sql_script_from_file

class SkladisteService():
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_skladista(self):
        try:
            sql_script = get_sql_script_from_file(SkladisteSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            skladista = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv': row[5],
                    'stanje': row[6],
                } 
            for row in data]
            return skladista
        except Exception as e:
            self.app.logger.error(f"Error in get_skladista: {e}")
            raise e
        
    def get_skladiste(self, id):
        try:
            sql_script = get_sql_script_from_file(SkladisteSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            skladiste = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv': data[5],
                'stanje': data[6],
            }
            return skladiste
        except Exception as e:
            self.app.logger.error(f"Error in get_skladiste: {e}")
            raise e
        
    def insert_skladiste(self, skladiste):
        try:
            sql_script = get_sql_script_from_file(SkladisteSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (skladiste['restoran_id'], ))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_skladiste: {e}")
            raise e
        
    def update_skladiste(self, skladiste, id):
        try:
            sql_script = get_sql_script_from_file(SkladisteSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (skladiste['restoran_id'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_skladiste: {e}")
            raise e
        
    def delete_skladiste(self, id):
        try:
            sql_script = get_sql_script_from_file(SkladisteSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_skladiste: {e}")
            raise e