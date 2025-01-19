from flask import Flask
from app.router.sql_routes import StolSqlRoutesEnum
from app.utils.sql_utils import get_sql_script_from_file
from app.utils.decorators import with_db_connection

class StolService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_stolovi(self):
        try:
            sql_script = get_sql_script_from_file(StolSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            stolovi = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'broj': row[6],
                    'lokacija': row[7],
                    'broj_mjesta': row[8],
                } 
            for row in data]
            return stolovi
        except Exception as e:
            self.app.logger.error(f"Error in get_stolovi: {e}")
            raise e
        
    @with_db_connection
    def get_stol(self, id):
        try:
            sql_script = get_sql_script_from_file(StolSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            stol = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'broj': data[6],
                'lokacija': data[7],
                'broj_mjesta': data[8],
            }
            return stol
        except Exception as e:
            self.app.logger.error(f"Error in get_stol: {e}")
            raise e
        
    @with_db_connection
    def insert_stol(self, stol):
        try:
            sql_script = get_sql_script_from_file(StolSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (stol['restoran_id'], stol['broj'], stol['lokacija'], stol['broj_mjesta']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_stol: {e}")
            raise e
        
    @with_db_connection
    def update_stol(self, stol, id):
        try:
            sql_script = get_sql_script_from_file(StolSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (stol['restoran_id'], stol['broj'], stol['lokacija'], stol['broj_mjesta'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_stol: {e}")
            raise e
    
    @with_db_connection
    def delete_stol(self, id):
        try:
            sql_script = get_sql_script_from_file(StolSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_stol: {e}")
            raise e

    @with_db_connection
    def check_stol_is_avilable(self, stol_id, vrijeme):
        try:
            sql_script = get_sql_script_from_file(StolSqlRoutesEnum.CHECK_STOL_IS_AVAILABLE.value)
            self.cursor.execute(sql_script, (stol_id, vrijeme))
            data = self.cursor.fetchone()
            return data[0]
        except Exception as e:
            self.app.logger.error(f"Error in check_stol_is_avilable: {e}")
            raise e