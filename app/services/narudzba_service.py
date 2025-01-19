from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import NarudzbaSqlRoutesEnum
from app.utils.decorators import with_db_connection

class NarudzbaService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_narudzbe(self):
        try:
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            narudzbe = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'skladiste_id': row[6],
                    'naziv': row[7],
                    'status_narudzbe': row[8]
                } 
            for row in data]
            return narudzbe
        except Exception as e:
            self.app.logger.error(f"Error in get_narudzbe: {e}")
            raise e
        
    @with_db_connection
    def get_narudzba(self, id):
        try:
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            narudzba = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'skladiste_id': data[6],
                'naziv': data[7],
                'status_narudzbe': data[8]
            }
            return narudzba
        except Exception as e:
            self.app.logger.error(f"Error in get_narudzba: {e}")
            raise e
        
    @with_db_connection
    def insert_narudzba(self, narudzba):
        try:
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (narudzba['skladiste_id'], narudzba['naziv']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_narudzba: {e}")
            raise e
        
    @with_db_connection
    def update_narudzba(self, narudzba, id):
        try:
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (narudzba['skladiste_id'], narudzba['naziv'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_narudzba: {e}")
            raise e
        
    @with_db_connection
    def delete_narudzba(self, id):
        try:
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_narudzba: {e}")
            raise e
        
    @with_db_connection
    def insert_narudzbe_sastojci(self, narudzba, sastojci):
        try:
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (narudzba['skladiste_id'], narudzba['naziv']))
            narudzba_id = self.cursor.lastrowid
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.INSERT_SASTOJCI.value)
            for sastojak in sastojci:
                self.cursor.execute(sql_script, (narudzba_id, sastojak['id'], sastojak['kolicina']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_narudzbe_sastojci: {e}")
            raise e
        
    @with_db_connection
    def update_narudzbe_sastojci(self, id, narudzba, sastojci, sastojci_updated):
        try:
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (narudzba['skladiste_id'], narudzba['naziv'], id))
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.DELETE_SASTOJCI.value)
            for sastojak in sastojci:
                self.cursor.execute(sql_script, (id, sastojak['id']))
            sql_script = get_sql_script_from_file(NarudzbaSqlRoutesEnum.INSERT_SASTOJCI.value)
            for sastojak in sastojci_updated:
                self.cursor.execute(sql_script, (id, sastojak['sastojak_id'], sastojak['kolicina']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_narudzbe_sastojci: {e}")
            raise e