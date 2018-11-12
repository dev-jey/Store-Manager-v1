from flask import Flask, Blueprint, make_response, jsonify
from instance.config import app_config
from flask_cors import CORS
from .api.v2 import blprint2 as version2


def create_app(config_name):
    '''Main function to create the flask app and
    set configurations'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../instance/config.py')
    app.register_blueprint(version2)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.errorhandler(404)
    def not_found(e):
        '''Defining a custom message for not found'''
        return make_response(jsonify({
            "Message": "What you are looking for was Not found (The route is wrong)"
        }), 404)

    @app.errorhandler(500)
    def server_error(e):
        logging.exception('An error occurred during a request. %s', e)
        logging.getLogger('flask_cors').level = logging.DEBUG
        return "An internal error occured", 500
    
    return app
