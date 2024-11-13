from app.config.db_config import DBConfig

class Database:
    _instance = None

    def __new__(cls, app):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.db_config = DBConfig(app)
        return cls._instance

    @property
    def connection(self):
        return self.db_config.mysql.connection