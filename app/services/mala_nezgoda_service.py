from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import MalaNezgodaSqlRoutesEnum
from app.utils.decorators import with_db_connection

class MalaNezgodaService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_male_nezgode(self):
        try:
            sql_script = get_sql_script_from_file(MalaNezgodaSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            male_nezgode = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv_zaposlenik': row[6],
                    'ukupno': row[7],
                    'broj_sastojaka': row[8]
                } 
            for row in data]
            return male_nezgode
        except Exception as e:
            self.app.logger.error(f"Error in get_mala_nezgode: {e}")
            raise e
        
    @with_db_connection
    def get_mala_nezgoda(self, id):
        try:
            sql_script = get_sql_script_from_file(MalaNezgodaSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            mala_nezgoda = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'naziv_zaposlenik': data[6],
                'ukupno': data[7]
            }
            return mala_nezgoda
        except Exception as e:
            self.app.logger.error(f"Error in get_mala_nezgoda: {e}")
            raise e
        
    @with_db_connection
    def insert_mala_nezgoda(self, mala_nezgoda):
        try:
            sql_script = get_sql_script_from_file(MalaNezgodaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (mala_nezgoda['restoran_id'], mala_nezgoda['zaposlenik_id']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_mala_nezgoda: {e}")
            raise e
        
    @with_db_connection
    def insert_mala_negoda_sastojci(self, mala_nezgoda, sastojci):
        try:
            sql_script = get_sql_script_from_file(MalaNezgodaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (mala_nezgoda['restoran_id'], mala_nezgoda['zaposlenik_id']))
            mala_nezgoda_id = self.cursor.lastrowid
            sql_script = get_sql_script_from_file(MalaNezgodaSqlRoutesEnum.INSERT_SASTOJCI.value)
            for sastojak in sastojci:
                self.cursor.execute(sql_script, (mala_nezgoda_id, sastojak['sastojak_id'], sastojak['kolicina']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_mala_nezgoda_sastojci: {e}")
            raise e
        
    @with_db_connection
    def get_total(self):
        try:
            sql_script = get_sql_script_from_file(MalaNezgodaSqlRoutesEnum.SELECT_TOTAL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            male_nezgode = [
                {
                    'id': row[0],
                    'naziv_restoran': row[1],
                    'ukupno': row[2]
                } 
            for row in data]
            return male_nezgode
        except Exception as e:
            self.app.logger.error(f"Error in get_total: {e}")
            raise e
        
    @with_db_connection
    def get_mala_nezgoda_details(self, id):
        try:
            sql_script = get_sql_script_from_file(MalaNezgodaSqlRoutesEnum.SELECT_DETAILS.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchall()
            sastojci = [
                {
                    'sastojak': row[0],
                    'kolicina': row[1]
                }
            for row in data]
            return sastojci
        except Exception as e:
            self.app.logger.error(f"Error in get_mala_nezgoda_details: {e}")
            raise e
        
    @with_db_connection
    def insert_mala_nezgoda_by_transaction(self, mala_nezgoda):
        try:
            sql_script = get_sql_script_from_file(MalaNezgodaSqlRoutesEnum.INSERT_BY_TRANSACTION.value)
            self.cursor.execute(sql_script, (mala_nezgoda['restoran_id'], mala_nezgoda['zaposlenik_id'], mala_nezgoda['sastojci']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_mala_nezgoda_by_transaction: {e}")
            raise e