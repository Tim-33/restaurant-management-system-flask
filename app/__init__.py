from flask import Flask
from flask_bootstrap import Bootstrap
from app.config.app_config import AppConfig
from app.database import Database
from app.router.app_router import AppRouter

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    
    config = AppConfig()
    
    app.config['API_PORT'] = config.API_PORT
    app.config['API_BASE_URL'] = config.API_BASE_URL
    
    app.config['MYSQL_DATABASE_HOST'] = config.MYSQL_HOST
    app.config['MYSQL_DATABASE_PORT'] = config.MYSQL_PORT
    app.config['MYSQL_DATABASE_USER'] = config.MYSQL_USER
    app.config['MYSQL_DATABASE_PASSWORD'] = config.MYSQL_PASSWORD
    app.config["MYSQL_CUSTOM_OPTIONS"] = config.MYSQL_CUSTOM_OPTIONS
    app.config['MYSQL_DATABASE_DB'] = config.MYSQL_DB
    app.config['LOGGING_CONFIG'] = config.LOGGING_CONFIG
    
    app.router = AppRouter()
    app.db = Database(app)
    
    app.router.create_routes()
    
    with app.app_context():
        register_blueprints(app)
        register_routes(app)
    
    return app

def register_blueprints(app):
    from app.modules.hello.hello_module import HelloModule
    
    HelloModule(app).register_blueprints()

def register_routes(app):
    from app.routes.app_routes import AppRoutes
    from app.routes.hello_routes import HelloRoutes
    
    AppRoutes(app).register_routes()
    HelloRoutes(app).register_routes()