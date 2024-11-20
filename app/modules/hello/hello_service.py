from app.router.sql_routes import HelloSqlRoutesEnum
from app.utils.sql_utils import get_sql_script_from_file
from app.database import Database

class HelloService:
    def __init__(self, db: Database):
        self.cursor = db.cursor
    
    def get_hello_message(self):
        sql_script = get_sql_script_from_file(HelloSqlRoutesEnum.SELECT_ALL.value)
        self.cursor.execute(sql_script)
        data = self.cursor.fetchall()
        return data