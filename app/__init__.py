from flask import Flask
from app.controllers import controller

def create_app():
    app = Flask(__name__)
    
    controller.init_app(app)

    return app
