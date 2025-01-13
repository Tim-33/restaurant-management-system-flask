from flask import Flask
from flask_bootstrap import Bootstrap
from app.config.app_config import AppConfig
from app.router.app_router import AppRouter
import mysql.connector

def register_routes(app):
    from app.routes.app_routes import AppRoutes
    from app.routes.zaposlenik_routes import ZaposlenikRoutes
    from app.routes.zaposlenik_placa_routes import ZaposlenikPlacaRoutes
    from app.routes.restoran_routes import RestoranRoutes
    from app.routes.skladiste_routes import SkladisteRoutes
    
    AppRoutes(app).register_routes()
    ZaposlenikRoutes(app).register_routes()
    ZaposlenikPlacaRoutes(app).register_routes()
    RestoranRoutes(app).register_routes()
    SkladisteRoutes(app).register_routes()

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
    host=app.config['MYSQL_DATABASE_HOST'],
    port=app.config['MYSQL_DATABASE_PORT'],
    user=app.config['MYSQL_DATABASE_USER'],
    password=app.config['MYSQL_DATABASE_PASSWORD'],
    database=app.config['MYSQL_DATABASE_DB']
)

app.router.create_routes()

with app.app_context():
    register_routes(app)