from flaskext.mysql import MySQL
import logging

class DBConfig:
    def __init__(self, app):
        self.my_database = MySQL()
        self.my_database.init_app(app)
        self.app = app
    
    @property
    def connection(self):
        return self.my_database.connect()