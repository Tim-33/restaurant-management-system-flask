from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import ZaposlenikPlacaSqlRoutesEnum
from app.utils.decorators import with_db_connection

class ZaposlenikPlacaService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_zaposlenik_place_months(self):
        try:
            sql_script = get_sql_script_from_file(ZaposlenikPlacaSqlRoutesEnum.SELECT_MONTHS.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            zaposlenik_place_months = [
                {
                    'mjesec': row[0].strftime('%Y-%m'),
                    'iznos': row[1]
                }
            for row in data]
            return zaposlenik_place_months
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenik_place_months: {e}")
            raise
        
    @with_db_connection
    def get_zaposlenik_place_by_month(self, month):
        try:
            sql_script = get_sql_script_from_file(ZaposlenikPlacaSqlRoutesEnum.SELECT_BY_MONTH.value)
            self.cursor.execute(sql_script, (month,))
            data = self.cursor.fetchall()
            zaposlenik_place = [
                {
                    'id': row[0],
                    'ime': row[1],
                    'prezime': row[2],
                    'iznos': row[3],
                    'mjesec': row[4],
                }
            for row in data]
            return zaposlenik_place
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenik_place_by_month: {e}")
            raise e
        
    @with_db_connection
    def get_zaposlenik_placa(self, id):
        try:
            sql_script = get_sql_script_from_file(ZaposlenikPlacaSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            zaposlenik_place = {
                'id': data[0],
                'ime': data[1],
                'prezime': data[2],
                'iznos': data[3],
                'mjesec': data[4],
            }
            return zaposlenik_place
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenik_placa: {e}")
            raise e
        
    @with_db_connection
    def insert_zaposlenik_placa(self, zaposlenik_id, iznos_place, datum):
        try:
            sql_script = get_sql_script_from_file(ZaposlenikPlacaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (zaposlenik_id, iznos_place, datum, ))
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            inserted_id = self.cursor.fetchone()[0]
            self.app.mysql.commit()
            return inserted_id
        except Exception as e:
            self.app.logger.error(f"Error in insert_zaposlenik_placa: {e}")
            raise e
        
    @with_db_connection
    def get_zaposlenik_place_all(self):
        try:
            sql_script = get_sql_script_from_file(ZaposlenikPlacaSqlRoutesEnum.SELECT_ALL_WITH_ZAPOSLENIK.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            zaposlenik_place = [
                {
                    'ime': row[0],
                    'prezime': row[1],
                    'placa': row[2],
                    'mjesec': row[3],
                    'restoran': row[4]
                }
            for row in data]
            return zaposlenik_place
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenik_place_all: {e}")
            raise e
        
    @with_db_connection
    def process_zaposlenik_placa_transaction(self, id):
        try:
            sql_script = get_sql_script_from_file(ZaposlenikPlacaSqlRoutesEnum.PROCESS_ZAPOSLENIK_PLACA_TRANSACTION.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
        except Exception as e:
            self.app.logger.error(f"Error in process_zaposlenik_placa_transaction: {e}")
            raise e