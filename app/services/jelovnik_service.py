from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import JelovnikSqlRoutesEnum
from app.utils.decorators import with_db_connection

class JelovnikService():
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_jelovnici(self):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            jelovnici = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'naziv_restoran': row[5],
                    'naziv': row[6],
                    'jelovnik_tip': row[7],
                } 
            for row in data]
            return jelovnici
        except Exception as e:
            self.app.logger.error(f"Error in get_jelovnici: {e}")
            raise e
        
    @with_db_connection
    def get_jelovnik(self, id):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.SELECT_ONE.value)
            self.cursor.execute(sql_script, (id,))
            data = self.cursor.fetchone()
            jelovnik = {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'naziv_restoran': data[5],
                'naziv': data[6],
                'jelovnik_tip': data[7],
            }
            return jelovnik
        except Exception as e:
            self.app.logger.error(f"Error in get_jelovnik: {e}")
            raise e
        
    @with_db_connection
    def insert_jelovnik(self, jelovnik):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (jelovnik['restoran_id'], jelovnik['naziv'], jelovnik['jelovnik_tip']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_jelovnik: {e}")
            raise e
        
    @with_db_connection
    def update_jelovnik(self, jelovnik, id):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (jelovnik["restoran_id"], jelovnik['naziv'], jelovnik['jelovnik_tip'], id))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_jelovnik: {e}")
            raise e
        
    @with_db_connection
    def delete_jelovnik(self, id):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.DELETE.value)
            self.cursor.execute(sql_script, (id,))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in delete_jelovnik: {e}")
            raise e
        
    @with_db_connection
    def insert_jelovnik_stavke(self, jelovnik, stavke):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.INSERT.value)
            self.cursor.execute(sql_script, (jelovnik['restoran_id'], jelovnik['naziv'], jelovnik['jelovnik_tip']))
            racun_id = self.cursor.lastrowid
            for stavka in stavke:
                sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.INSERT_STAVKE.value)
                self.cursor.execute(sql_script, (racun_id, stavka['stavka_id']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_racun_stavke: {e}")
            raise e
        
    @with_db_connection
    def update_jelovnik_stavke(self, id, jelovnik, jelovnik_stavke, jelovnik_stavke_updated):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.UPDATE.value)
            self.cursor.execute(sql_script, (jelovnik["restoran_id"], jelovnik['naziv'], jelovnik['jelovnik_tip'], id))
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.DELETE_STAVKE.value)
            for jelovnik_stavka in jelovnik_stavke:
                self.cursor.execute(sql_script, (id, jelovnik_stavka['id']))
            for jelovnik_stavka_updated in jelovnik_stavke_updated:
                sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.INSERT_STAVKE.value)
                self.cursor.execute(sql_script, (id, jelovnik_stavka_updated['stavka_id']))
            self.app.mysql.commit()
            return True
        except Exception as e:
            self.app.logger.error(f"Error in update_jelovnik_stavke: {e}")
            raise e
        
    @with_db_connection
    def get_jelovnik_with_stavka_count(self):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.SELECT_WITH_STAVKA_COUNT.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            jelovnici = [
                {
                    'naziv': row[0],
                    'broj_stavki': row[1],
                } 
            for row in data]
            return jelovnici
        except Exception as e:
            self.app.logger.error(f"Error in get_jelovnik_with_stavka_count: {e}")
            raise e
        
    @with_db_connection
    def get_jelovnik_stavke_tipa_jela(self):
        try:
            sql_script = get_sql_script_from_file(JelovnikSqlRoutesEnum.SELECT_STAVKE_TYPE_JELA.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            jelovnici = [
                {
                    'naziv_stavke': row[0],
                    'cijena': row[1],
                    'naziv_jelovnika': row[2],
                } 
            for row in data]
            return jelovnici
        except Exception as e:
            self.app.logger.error(f"Error in get_jelovnik_stavke_tipa_jela: {e}")
            raise e