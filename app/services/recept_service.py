from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import ReceptSqlRoutesEnum

class ReceptService:
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_recepti(self):
        try:
            sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            recepti = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv': row[6],
                    'upute': row[7]
                } 
            for row in data]
            return recepti
        except Exception as e:
            self.app.logger.error(f"Error in get_recepti: {e}")
            raise e
        
    def get_recept(self, id):
        try:
            sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            recept = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'naziv': data[6],
                'upute': data[7]
            }
            return recept
        except Exception as e:
            self.app.logger.error(f"Error in get_recept: {e}")
            raise e
        
    def insert_recept(self, recept):
        try:
            sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (recept['restoran_id'], recept['naziv'], recept['upute']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_recept: {e}")
            raise e
        
    def update_recept(self, recept, id):
        try:
            sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (recept['restoran_id'], recept['naziv'], recept['upute'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_recept: {e}")
            raise e
        
    def delete_recept(self, id):
        try:
            sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_recept: {e}")
            raise e
        
    def insert_recept_sastojci(self, recept, sastojci):
        try:
            sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (recept['restoran_id'], recept['naziv'], recept['upute']))
            recept_id = self.cursor.lastrowid
            for sastojak in sastojci:
                sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.INSERT_SASTOJCI.value)
                self.cursor.execute(sql_script, (recept_id, sastojak['sastojak_id'], sastojak['kolicina']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_recept_sastojci: {e}")
            raise e
        
    def update_recept_sastojci(self, id, recept, sastojci, sastojci_updated):
        try:
            sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (recept['restoran_id'], recept['naziv'], recept['upute'], id))
            for sastojak in sastojci:
                sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.INSERT_SASTOJCI.value)
                self.cursor.execute(sql_script, (id, sastojak['sastojak_id'], sastojak['kolicina']))
            for sastojak in sastojci_updated:
                sql_script = get_sql_script_from_file(ReceptSqlRoutesEnum.DELETE_SASTOJCI.value)
                self.cursor.execute(sql_script, (id, sastojak['id']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_recept_sastojci: {e}")
            raise e