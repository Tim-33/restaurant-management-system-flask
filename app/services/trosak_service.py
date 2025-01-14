from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import TrosakSqlRoutesEnum

class TrosakService():
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_troskovi(self):
        try:
            sql_script = get_sql_script_from_file(TrosakSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            troskovi = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv': row[6],
                    'iznos': row[7],
                    'mjesecno': row[8],
                } 
            for row in data]
            return troskovi
        except Exception as e:
            self.app.logger.error(f"Error in get_troskovi: {e}")
            raise e
        
    def get_trosak(self, id):
        try:
            sql_script = get_sql_script_from_file(TrosakSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            trosak = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'naziv': data[6],
                'iznos': data[7],
                'mjesecno': data[8],
            }
            return trosak
        except Exception as e:
            self.app.logger.error(f"Error in get_trosak: {e}")
            raise e
        
    def insert_trosak(self, trosak):
        try:
            sql_script = get_sql_script_from_file(TrosakSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (trosak['restoran_id'], trosak['naziv'], trosak['iznos'], trosak['mjesecno']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_trosak: {e}")
            raise e
        
    def update_trosak(self, trosak, id):
        try:
            sql_script = get_sql_script_from_file(TrosakSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (trosak['restoran_id'], trosak['naziv'], trosak['iznos'], trosak['mjesecno'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_trosak: {e}")
            raise e
        
    def delete_trosak(self, id):
        try:
            sql_script = get_sql_script_from_file(TrosakSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_trosak: {e}")
            raise e
        