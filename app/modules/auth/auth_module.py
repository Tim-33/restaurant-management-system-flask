from app.interfaces.imodule import IModule
from flask import Flask
from app.modules.auth.auth_controller import AuthController

class AuthModule(IModule):
    def __init__(self, app: Flask):
        self.app = app
        self.controller = AuthController(self.app)
        
    def register_blueprints(self):
        self.controller.register_routes()