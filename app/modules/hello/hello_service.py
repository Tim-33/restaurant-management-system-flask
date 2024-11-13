from app.modules.hello.enums.hello_sql_routes import HelloSqlRoutesEnum
from app.utils.sql_utils import get_sql_script_from_file
from app.database import Database

class HelloService:
    def __init__(self, db: Database):
        self.connection = db.connection
        
    def get_hello_message(self):
        sql = get_sql_script_from_file(HelloSqlRoutesEnum.SELECT_ALL.value)
        cur = self.connection.cursor()
        cur.execute(sql)
        rv = cur.fetchall()    
        return rv