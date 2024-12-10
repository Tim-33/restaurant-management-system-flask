from app.router.sql_routes import HelloSqlRoutesEnum
from app.modules.hello.dto.create_hello_dto import CreateHelloDto
from app.modules.hello.hello_model import HelloModel
from app.utils.sql_utils import get_sql_script_from_file
from typing import List
from flask import Flask

class HelloService:
    def __init__(self, app: Flask):
        self.app = app
        self.cursor = self.app.db.cursor
    
    def get_hello_messages(self) -> List[HelloModel]:
        sql_script = get_sql_script_from_file(HelloSqlRoutesEnum.SELECT_ALL.value)
        self.cursor.execute(sql_script)
        data = self.cursor.fetchall()
        hellos = [{"id": row[0], "message": row[1]} for row in data]
        return hellos
    
    def get_hello_message(self, id: int) -> HelloModel:
        sql_script = get_sql_script_from_file(HelloSqlRoutesEnum.SELECT_ONE.value)
        self.cursor.execute(sql_script, id)
        data = self.cursor.fetchone()
        hello = {"id": data[0], "message": data[1]}
        return hello
    
    def insert_hello_message(self, message: CreateHelloDto):
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