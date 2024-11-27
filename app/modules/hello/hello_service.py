from app.router.sql_routes import HelloSqlRoutesEnum
from app.utils.sql_utils import get_sql_script_from_file
from app.database import Database

class HelloService:
    def __init__(self, db: Database):
        self.cursor = db.cursor
    
    def get_hello_messages(self):
        sql_script = get_sql_script_from_file(HelloSqlRoutesEnum.SELECT_ALL.value)
        self.cursor.execute(sql_script, 1)
        data = self.cursor.fetchall()
        return data
    
    def get_hello_message(self, id):
        sql_script = get_sql_script_from_file(HelloSqlRoutesEnum.SELECT_ONE.value)
        self.cursor.execute(sql_script, id)
        data = self.cursor.fetchone()
        return data
    
    def insert_hello_message(self, message):
        sql_script = get_sql_script_from_file(HelloSqlRoutesEnum.INSERT.value)
        self.cursor.execute(sql_script, message)
        return self.cursor.lastrowid
    
    def update_hello_message(self, message, id):
        sql_script = get_sql_script_from_file(HelloSqlRoutesEnum.UPDATE.value)
        self.cursor.execute(sql_script, message, id)
        return self.cursor.rowcount
    
    def delete_hello_message(self, id):
        sql_script = get_sql_script_from_file(HelloSqlRoutesEnum.DELETE.value)
        self.cursor.execute(sql_script, id)
        return self.cursor.rowcount