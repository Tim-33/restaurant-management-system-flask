from flask import Flask
from app.router.sql_routes import TransakcijaRestoranSqlRoutesEnum
from app.utils.sql_utils import get_sql_script_from_file
from app.utils.decorators import with_db_connection

class TransakcijaRestoranService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_transakcije_restorana(self):
        try:
            sql_script = get_sql_script_from_file(TransakcijaRestoranSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            transakcije_restorana = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv': row[6],
                    'iznos': row[7],
                }
            for row in data]
            return transakcije_restorana
        except Exception as e:
            self.app.logger.error(f"Error in get_transakcije_restorana: {e}")
            raise e
    
    @with_db_connection
    def get_transakcija_restorana(self, id):
        try:
            sql_script = get_sql_script_from_file(TransakcijaRestoranSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            transakcija_restorana = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'naziv': data[6],
                'iznos': data[7],
            }
            return transakcija_restorana
        except Exception as e:
            self.app.logger.error(f"Error in get_transakcija_restorana: {e}")
            raise e