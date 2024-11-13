import os
from dotenv import load_dotenv

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