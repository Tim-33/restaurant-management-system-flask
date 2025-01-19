from flask import Flask
from app.utils.sql_utils import get_sql_script_from_file
from app.router.sql_routes import UserSqlRoutesEnum
from app.utils.decorators import with_db_connection

class UserService:
    def __init__(self, app: Flask):
        self.app = app
        
    @with_db_connection
    def get_users(self):
        try:
            sql_script = get_sql_script_from_file(UserSqlRoutesEnum.SELECT_ALL.value)
            self.cursor.execute(sql_script)
            data = self.cursor.fetchall()
            users = [
                {
                    'user': row[0],
                    'table': row[1],
                    'privilege': row[2],
                } 
            for row in data]
            return users
        except Exception as e:
            self.app.logger.error(f"Error in get_users: {e}")
            raise e