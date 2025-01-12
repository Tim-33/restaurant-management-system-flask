from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import ZaposlenikSqlRoutesEnum
from flask import Flask
import base64

class ZaposlenikService:
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.mysql.cursor()
        
    def get_zaposlenici(self):
        try:
            sql_script = get_sql_script_from_file(ZaposlenikSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            zaposlenici = [
                {
                    'id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'deleted_at': row[3],
                    'disabled': row[4],
                    'restoran_id': row[5],
                    'zaposlenik_tip': row[6],
                    'ime': row[7],
                    'prezime': row[8],
                    'email': row[9],
                    'datum_rodenja': row[10],
                    'iznos_place': row[11],
                    'slika': base64.b64encode(row[12]).decode('utf-8') if row[12] else None
                } 
            for row in data]
            return zaposlenici
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenici: {e}")
            raise e
        
    def get_zaposlenik(self, id):
        sql_script = get_sql_script_from_file(ZaposlenikSqlRoutesEnum.SELECT_ONE.value)
        self.cursor.execute(sql_script, (id,))
        data = self.cursor.fetchone()
        zaposlenik =  {
                'id': data[0],
                'created_at': data[1],
                'updated_at': data[2],
                'deleted_at': data[3],
                'disabled': data[4],
                'restoran_id': data[5],
                'zaposlenik_tip': data[6],
                'ime': data[7],
                'prezime': data[8],
                'email': data[9],
                'datum_rodenja': data[10],
                'iznos_place': data[11],
                'slika': base64.b64encode(data[12]).decode('utf-8') if data[12] else None
            } 
        return zaposlenik
    
    def insert_zaposlenik(self, zaposlenik):
        sql_script = get_sql_script_from_file(ZaposlenikSqlRoutesEnum.INSERT.value)
        values = (
            zaposlenik["restoran_id"],
            zaposlenik["zaposlenik_tip"],
            zaposlenik["ime"],
            zaposlenik["prezime"],
            zaposlenik["email"],
            zaposlenik["datum_rodenja"],
            zaposlenik["iznos_place"],
            base64.b64decode(zaposlenik["slika"]) if zaposlenik["slika"] else None
        )
        self.cursor.execute(sql_script, values)
        self.app.mysql.commit()
        return self.cursor.lastrowid
    
    def update_zaposlenik(self, zaposlenik, id: int):
        sql_script = get_sql_script_from_file(ZaposlenikSqlRoutesEnum.UPDATE.value)
        values = (
            zaposlenik["restoran_id"],
            zaposlenik["zaposlenik_tip"],
            zaposlenik["ime"],
            zaposlenik["prezime"],
            zaposlenik["email"],
            zaposlenik["datum_rodenja"],
            zaposlenik["iznos_place"],
            base64.b64decode(zaposlenik["slika"]) if zaposlenik["slika"] else None,
            id
        )
        self.cursor.execute(sql_script, values)
        self.app.mysql.commit()
        return self.cursor.rowcount
    
    def delete_zaposlenik(self, id: int):
        sql_script = get_sql_script_from_file(ZaposlenikSqlRoutesEnum.DELETE.value)
        self.cursor.execute(sql_script, (id, ))
        self.app.mysql.commit()
        return self.cursor.rowcount