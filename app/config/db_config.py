from flask_mysqldb import MySQL

class DBConfig:
    def __init__(self, app):
        self.mysql = MySQL(app)