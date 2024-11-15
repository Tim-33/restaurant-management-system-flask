from app.config.db_config import DBConfig

class Database:
    def __init__(self, app):
        self.app = app
        self.db_config = DBConfig(app)
    
    @property
    def connection(self):
        return self.db_config.connection