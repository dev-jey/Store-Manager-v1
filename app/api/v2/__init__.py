from flask import Blueprint
from flask_restful import Api, Resource

from .views import SignUp

'''Creation of blue prints and routes for endpoints'''
blprint2 = Blueprint('api', __name__, url_prefix="/api/v2")
api = Api(blprint2)
api.add_resource(SignUp, "/auth/signup")
