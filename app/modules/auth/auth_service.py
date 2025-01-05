from flask import Flask
from app.modules.auth.dto.login_dto import LoginDto
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import AuthSqlRoutesEnum

class AuthService:
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.db.cursor
        
    def login(self, username: str, password: str):
        sql_script = get_sql_script_from_file(AuthSqlRoutesEnum.SELECT_ONE.value)
        self.cursor.execute(sql_script, (username, password))
        
        return self.cursor.rowcount
