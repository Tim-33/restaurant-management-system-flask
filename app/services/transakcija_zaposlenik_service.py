from flask import Flask
from app.router.sql_routes import TransakcijaZaposlenikSqlRoutesEnum
from app.utils.sql_utils import get_sql_script_from_file

class TransakcijaZaposlenikService:
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_transakcije_zaposlenika(self):
        try:
            sql_script = get_sql_script_from_file(TransakcijaZaposlenikSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            transakcije_zaposlenika = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_zaposlenik': row[5],
                    'naziv': row[6],
                    'iznos': row[7],
                }
            for row in data]
            return transakcije_zaposlenika
        except Exception as e:
            self.app.logger.error(f"Error in get_transakcije_zaposlenika: {e}")
            raise e
        
    def get_transakcija_zaposlenika(self, id):
        try:
            sql_script = get_sql_script_from_file(TransakcijaZaposlenikSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            transakcija_zaposlenika = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_zaposlenik': data[5],
                'naziv': data[6],
                'iznos': data[7],
            }
            return transakcija_zaposlenika
        except Exception as e:
            self.app.logger.error(f"Error in get_transakcija_zaposlenika: {e}")
            raise e