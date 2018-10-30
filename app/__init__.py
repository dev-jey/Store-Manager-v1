from flask import Flask, Blueprint
from instance.config import app_config
from .api.v2 import blprint2 as version2


def create_app(config_name):
    '''Main function to create the flask app and
    set configurations'''
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../instance/config.py')
    app.register_blueprint(version2)
    return app
