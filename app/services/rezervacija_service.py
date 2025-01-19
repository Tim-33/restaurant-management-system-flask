from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import RezervacijaSqlRoutesEnum

class RezervacijaService():
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_rezervacije(self):
        try:
            sql_script = get_sql_script_from_file(RezervacijaSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            rezervacije = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'broj_stola': row[6],
                    'broj_mjesta_stola': row[7],
                    'ime': row[8],
                    'vrijeme': row[9],
                    'broj_osoba': row[10],
                } 
            for row in data]
            return rezervacije
        except Exception as e:
            self.app.logger.error(f"Error in get_rezervacije: {e}")
            raise e
        
    def get_rezervacija(self, id):
        try:
            sql_script = get_sql_script_from_file(RezervacijaSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            rezervacija = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'broj_stola': data[6],
                'broj_mjesta_stola': data[7],
                'ime': data[8],
                'vrijeme': data[9],
                'broj_osoba': data[10],
            }
            return rezervacija
        except Exception as e:
            self.app.logger.error(f"Error in get_rezervacija: {e}")
            raise e
        
    def insert_rezervacija(self, rezervacija):
        try:
            sql_script = get_sql_script_from_file(RezervacijaSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (rezervacija['restoran_id'], rezervacija['stol_id'], rezervacija['ime'], rezervacija['vrijeme'], rezervacija['broj_osoba']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_rezervacija: {e}")
            raise e
        
    def update_rezervacija(self, rezervacija, id):
        try:
            sql_script = get_sql_script_from_file(RezervacijaSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (rezervacija['restoran_id'], rezervacija['stol_id'], rezervacija['ime'], rezervacija['vrijeme'], rezervacija['broj_osoba'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_rezervacija: {e}")
            raise e
        
    def delete_rezervacija(self, id):
        try:
            sql_script = get_sql_script_from_file(RezervacijaSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_rezervacija: {e}")
            raise e
        
    def get_rezervacija_by_location_with_count(self):
        try:
            sql_script = get_sql_script_from_file(RezervacijaSqlRoutesEnum.SELECT_BY_TYPE_WITH_LOCATION.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            rezervacije = [
                {
                    'restoran_id': row[0],
                    'lokacija': row[1],
                    'broj_rezervacija': row[2],
                }
            for row in data]
            return rezervacije
        except Exception as e:
            self.app.logger.error(f"Error in get_rezervacija_by_location_with_count: {e}")
            raise e