from flask import Flask
from app.router.sql_routes import SastojakSqlRoutesEnum
from app.utils.sql_utils import get_sql_script_from_file
import base64
from app.utils.decorators import with_db_connection

class SastojakService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_sastojci(self):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            sastojci = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restorana': row[5],
                    'skladiste_id': row[6],
                    'naziv': row[7],
                    'cijena': row[8],
                    'kolicina_tip': row[9],
                    'slika': base64.b64encode(row[10]).decode('utf-8') if row[10] else None,
                    'potrebna_kolicina': row[11],
                    'trenutna_kolicina': row[12],
                    'treba_li_naruciti': row[13],
                } 
            for row in data]
            return sastojci
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojci: {e}")
            raise e
        
    @with_db_connection
    def get_sastojak(self, id):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            sastojak = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restorana': data[5],
                'skladiste_id': data[6],
                'naziv': data[7],
                'cijena': data[8],
                'kolicina_tip': data[9],
                'slika': base64.b64encode(data[10]).decode('utf-8') if data[10] else None,
                'potrebna_kolicina': data[11],
                'trenutna_kolicina': data[12],
            }
            return sastojak
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak: {e}")
            raise e
        
    @with_db_connection
    def insert_sastojak(self, sastojak):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.INSERT.value)
            values = (
                sastojak["skladiste_id"],
                sastojak["naziv"],
                sastojak["cijena"],
                sastojak["kolicina_tip"],
                sastojak["slika"],
                sastojak["potrebna_kolicina"],
                sastojak["trenutna_kolicina"],
            )
            self.cursor.execute(sql_script, values)
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_sastojak: {e}")
            raise e
        
    @with_db_connection
    def update_sastojak(self, sastojak, id):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.UPDATE.value)
            values = (
                sastojak["skladiste_id"],
                sastojak["naziv"],
                sastojak["cijena"],
                sastojak["kolicina_tip"],
                sastojak["slika"],
                sastojak["potrebna_kolicina"],
                sastojak["trenutna_kolicina"],
                id
            )
            self.cursor.execute(sql_script, values)
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_sastojak: {e}")
            raise e
        
    @with_db_connection
    def delete_sastojak(self, id):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_sastojak: {e}")
            raise e
        
    @with_db_connection
    def get_sastojak_by_recept(self, recept_id):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.SELECT_BY_RECEPT.value)
            self.cursor.execute(sql_script, (recept_id,))
            data = self.cursor.fetchall()
            sastojci = [
                {
                    'id': row[0],
                    'naziv': row[1],
                    'kolicina': row[2],
                    'kolicina_tip': row[3],
                    'slika': base64.b64encode(row[4]).decode('utf-8') if row[4] else None,
                } 
            for row in data]
            return sastojci
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak_by_recept: {e}")
            raise e
        
    @with_db_connection
    def get_sastojak_by_narudzba(self, narudzba_id):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.SELECT_BY_NARUDZBA.value)
            self.cursor.execute(sql_script, (narudzba_id,))
            data = self.cursor.fetchall()
            sastojci = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv': row[5],
                    'cijena': row[6],
                    'kolicina_tip': row[7],
                    'kolicina': row[8],
                    'slika': base64.b64encode(row[9]).decode('utf-8') if row[9] else None,
                } 
            for row in data]
            return sastojci
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak_by_narudzba: {e}")
            raise e
        
    @with_db_connection
    def get_sastojak_by_skladiste(self, skladiste_id):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.SELECT_BY_SKLADISTE.value)
            self.cursor.execute(sql_script, (skladiste_id,))
            data = self.cursor.fetchall()
            sastojci = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv': row[5],
                    'cijena': row[6],
                    'kolicina_tip': row[7],
                    'slika': base64.b64encode(row[8]).decode('utf-8') if row[8] else None,
                    'potrebna_kolicina': row[9],
                    'trenutna_kolicina': row[10],
                } 
            for row in data]
            return sastojci
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak_by_skladiste: {e}")
            raise e
        
    @with_db_connection
    def get_sastojak_by_mala_nezgoda(self, mala_nezgoda_id):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.SELECT_BY_MALA_NEZGODA.value)
            self.cursor.execute(sql_script, (mala_nezgoda_id,))
            data = self.cursor.fetchall()
            sastojci = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv': row[5],
                    'cijena': row[6],
                    'kolicina_tip': row[7],
                    'kolicina': row[8],
                    'slika': base64.b64encode(row[9]).decode('utf-8') if row[9] else None,
                } 
            for row in data]
            return sastojci
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak_by_mala_nezgoda: {e}")
            raise e
        
    @with_db_connection
    def get_sastojak_ukupna_kolicina(self):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.SELECT_UKUPNA_KOLICINA.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            sastojci = [
                {
                    'naziv': row[0],
                    'ukupna_kolicina': row[1],
                }
            for row in data]
            return sastojci
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojak_ukupna_kolicina: {e}")
            raise e
        
    @with_db_connection
    def get_sastojci_most_common(self):
        try:
            sql_script = get_sql_script_from_file(SastojakSqlRoutesEnum.SELECT_MOST_COMMON.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            sastojci = [
                {
                    'naziv': row[0],
                    'ukupna_kolicina': row[1],
                }
            for row in data]
            return sastojci
        except Exception as e:
            self.app.logger.error(f"Error in get_sastojci_most_common: {e}")
            raise e