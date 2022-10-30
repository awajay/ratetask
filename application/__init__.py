from flask import Flask

import application
from application.controllers import rates_bp
from config import load_config


def create_app(testing=None, envfile='.env'):
    load_config(testing, envfile)
    app = Flask(__name__)
    app.json.sort_keys = False
    register_bp(app)
    return app


def register_bp(app):
    app.register_blueprint(rates_bp)
