from flask import Blueprint
from flask_restful import Api, Resource

from .views import SignUp, Login, Product, OneProduct, Sale

'''Creation of blue prints and routes for endpoints'''
blprint2 = Blueprint('api', __name__, url_prefix="/api/v2")
api = Api(blprint2)
api.add_resource(SignUp, "/auth/signup")
api.add_resource(Login, "/auth/login")
api.add_resource(Product, "/products")
api.add_resource(OneProduct, "/products/<int:productId>")
api.add_resource(Sale, "/sales")