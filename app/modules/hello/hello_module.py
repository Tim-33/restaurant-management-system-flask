from app.modules.hello.hello_controller import HelloController
from app.interfaces.imodule import IModule
from flask import Flask

class HelloModule(IModule):
    def __init__(self, app: Flask):
        self.app = app
        self.controller = HelloController(self.app)