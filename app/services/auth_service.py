from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import AuthSqlRoutesEnum
from app.utils.decorators import with_db_connection

class AuthService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def login(self, username: str, password: str):
        sql_script = get_sql_script_from_file(AuthSqlRoutesEnum.SELECT_ONE.value)
        self.cursor.execute(sql_script, (username, password))
        
        return self.cursor.rowcount
