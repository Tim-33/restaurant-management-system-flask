import os
from dotenv import load_dotenv
from logging.config import dictConfig

loggingConfig = dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

class AppConfig:
    def __init__(self):
        load_dotenv()
        self.MYSQL_HOST: str = os.getenv('MYSQL_HOST')
        self.MYSQL_PORT: int = int(os.getenv('MYSQL_PORT'))
        self.MYSQL_USER: str = os.getenv('MYSQL_USER')
        self.MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD')
        self.MYSQL_DB: str = os.getenv('MYSQL_DB')
        self.MYSQL_CUSTOM_OPTIONS: str = {"ssl": {"ca": os.getenv('MYSQL_SSL_CA')}}
        self.API_PORT: int = int(os.getenv('API_PORT'))
        self.API_BASE_URL: str = os.getenv('API_BASE_URL')
        self.LOGGING_CONFIG = loggingConfig