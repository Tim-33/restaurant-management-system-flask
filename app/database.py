from app.config.db_config import DBConfig

class Database:
    _instance = None

    def __new__(cls, app):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.__init__(app)
        return cls._instance

    def __init__(self, app):
        if not hasattr(self, 'initialized'):
            self.app = app
            self.db_config = DBConfig(app)
            self.initialized = True

    @property
    def connection(self):
        return self.db_config.connection
    
    @property
    def cursor(self):
        return self.connection.cursor()