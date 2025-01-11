from flask import Flask
from flask_bootstrap import Bootstrap
from app.config.app_config import AppConfig
from app.router.app_router import AppRouter
import mysql.connector

def register_routes(app):
    from app.routes.app_routes import AppRoutes
    from app.routes.hello_routes import HelloRoutes
    from app.routes.zaposlenik_routes import ZaposlenikRoutes
    
    AppRoutes(app).register_routes()
    HelloRoutes(app).register_routes()
    ZaposlenikRoutes(app).register_routes()

app = Flask(__name__)
Bootstrap(app)

config = AppConfig()

app.config['API_PORT'] = config.API_PORT
app.config['API_BASE_URL'] = config.API_BASE_URL

app.config['MYSQL_DATABASE_HOST'] = config.MYSQL_HOST
app.config['MYSQL_DATABASE_PORT'] = config.MYSQL_PORT
app.config['MYSQL_DATABASE_DB'] = config.MYSQL_DB
app.config['LOGGING_CONFIG'] = config.LOGGING_CONFIG

app.config['MYSQL_DATABASE_USER'] = config.MYSQL_USER
app.config['MYSQL_DATABASE_PASSWORD'] = config.MYSQL_PASSWORD

app.router = AppRouter()
app.mysql = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="sustav_za_upravljanje_restoranom"
)

app.router.create_routes()

with app.app_context():
    register_routes(app)