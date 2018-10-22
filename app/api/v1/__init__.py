from flask import Blueprint
from flask_restful import Api, Resource


blprint = Blueprint('api', __name__, url_prefix="/api/v1")
api = Api(blprint)
api.add_resource(SignUp, "/auth/signup")
api.add_resource(Login, "/auth/login")
api.add_resource(Sale, "/sales")
api.add_resource(Product, "/products")
api.add_resource(OneSale, "/sales/<saleId>")
api.add_resource(OneProduct, "/products/<productId>")