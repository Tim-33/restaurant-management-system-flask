from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import ZaposlenikSqlRoutesEnum
from flask import Flask
import base64
from app.utils.decorators import with_db_connection

class ZaposlenikService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
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
                    'slika': base64.b64encode(row[12]).decode('utf-8') if row[12] else None,
                    'ukupna_zarada': row[13]
                } 
            for row in data]
            return zaposlenici
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenici: {e}")
            raise e
        
    @with_db_connection
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
    
    @with_db_connection
    def insert_zaposlenik(self, zaposlenik):
        try:
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
            return True
        except Exception as e:
            self.app.logger.error(f"Error in insert_zaposlenik: {e}")
            raise e
    
    @with_db_connection
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
    
    @with_db_connection
    def delete_zaposlenik(self, id: int):
        sql_script = get_sql_script_from_file(ZaposlenikSqlRoutesEnum.DELETE.value)
        self.cursor.execute(sql_script, (id, ))
        self.app.mysql.commit()
        return self.cursor.rowcount
    
    @with_db_connection
    def get_zaposlenik_with_pay_for_january_and_june(self):
        sql_script = get_sql_script_from_file(ZaposlenikSqlRoutesEnum.SELECT_WITH_PAY_FOR_JANUARY_AND_JUNE.value)
        self.cursor.execute(sql_script)
        data = self.cursor.fetchall()
        zaposlenici = [
            {
                'ime': row[0],
                'prezime': row[1],
                'mjesecna_placa': row[2],
                'mjesec': row[3],
            } 
        for row in data]
        return zaposlenici
    
    @with_db_connection
    def get_zaposlenici_nezgode(self):
        try:
            sql_script = get_sql_script_from_file(ZaposlenikSqlRoutesEnum.SELECT_NEZGODE.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            zaposlenici = [
                {
                    'id': row[0],
                    'ime': row[1],
                    'prezime': row[2],
                    'ukupno_mala_nezgoda': row[3],
                    'ukupno_velika_nezgoda': row[4],
                    'ukupno_trosak': row[5]
                } 
            for row in data]
            return zaposlenici
        except Exception as e:
            self.app.logger.error(f"Error in get_zaposlenici_nezgode: {e}")
            raise e