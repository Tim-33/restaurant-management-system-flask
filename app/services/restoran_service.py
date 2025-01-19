from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import RestoranSqlRoutesEnum
import base64
from app.utils.decorators import with_db_connection

class RestoranService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
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
                    'slika': base64.b64encode(row[8]).decode('utf-8') if row[8] else None,
                    'cijena_skladista': row[9]
                } 
            for row in data]
            return restorani
        except Exception as e:
            self.app.logger.error(f"Error in get_restorani: {e}")
            raise e
        
    @with_db_connection
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

    @with_db_connection
    def insert_restoran(self, restoran):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (restoran['naziv'], restoran['adresa'], restoran['broj_telefona'], restoran['slika']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_restoran: {e}")
            raise e
        
    @with_db_connection
    def update_restoran(self, restoran, id):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (restoran['naziv'], restoran['adresa'], restoran['broj_telefona'], restoran['slika'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_restoran: {e}")
            raise e
        
    @with_db_connection
    def delete_restoran(self, id):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_restoran: {e}")
            raise e
        
    @with_db_connection
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
        
    @with_db_connection
    def get_restoran_with_zaposlenik_pay_data(self):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.SELECT_RESTORAN_WITH_ZAPOSLENIK_PAY_DATA.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            restorani = [
                {
                    'restoran': row[0],
                    'broj_zaposlenika': row[1],
                    'ukupne_place': row[2]
                }
            for row in data]
            return restorani
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_with_zaposlenik_pay_data: {e}")
            raise e
        
    @with_db_connection
    def get_restoran_average_employee_pay(self):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.SELECT_AVERAGE_EMPLOYEE_PAY.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            restorani = [
                {
                    'id': row[0],
                    'restoran': row[1],
                    'prosjecna_placa': row[2]
                }
            for row in data]
            return restorani
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_average_employee_pay: {e}")
            raise e
        
    @with_db_connection
    def get_restorani_nezgode_ukupno(self):
        try:
            sql_script = get_sql_script_from_file(RestoranSqlRoutesEnum.SELECT_NEZGODE_UKUPNO.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            restorani = [{
                'id': row[0],
                'ukupna_steta': row[1]
            } for row in data]
            return restorani
        except Exception as e:
            self.app.logger.error(f"Error in get_restoran_nezgode_ukupno: {e}")
            raise e