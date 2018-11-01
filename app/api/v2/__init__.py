from flask import Blueprint
from flask_restful import Api, Resource

from .views import SignUp, Login, Product, OneProduct, Sale, OneSale, UpdateUser, Signout

'''Creation of blue prints and routes for endpoints'''
blprint2 = Blueprint('api2', __name__, url_prefix="/api/v2")
api = Api(blprint2)
api.add_resource(SignUp, "/auth/signup")
api.add_resource(Login, "/auth/login")
api.add_resource(Product, "/products")
api.add_resource(OneProduct, "/products/<int:productId>")
api.add_resource(Sale, "/sales")
api.add_resource(OneSale, "/sales/<int:saleId>")
api.add_resource(UpdateUser, "/users/<int:userId>")
api.add_resource(Signout, "/auth/logout")