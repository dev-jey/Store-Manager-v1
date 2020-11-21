from flask import Blueprint
from flask_restful import Api, Resource

from .views.user_views import SignUp, Login, UpdateUser, Signout, GetUsers
from .views.product_views import Product, OneProduct, CategoryProduct
from .views.cart_views import Cart, OneItem, Change
from .views.sales_view import Sale, OneSale
from .views.categories_views import Category, OneCategory

blprint2 = Blueprint('api2', __name__, url_prefix="/api/v2")
api = Api(blprint2)
api.add_resource(SignUp, "/auth/signup")
api.add_resource(Login, "/auth/login")
api.add_resource(Product, "/products")
api.add_resource(OneProduct, "/products/<int:productId>")
api.add_resource(CategoryProduct, "/products/categories/<int:itemId>")
api.add_resource(Cart, "/cart")
api.add_resource(Change, "/change")
api.add_resource(OneItem, "/cart/<int:itemId>")
api.add_resource(Sale, "/sales")
api.add_resource(Category, "/categories")
api.add_resource(OneCategory, "/categories/<int:itemId>")
api.add_resource(OneSale, "/sales/<int:itemId>")
api.add_resource(UpdateUser, "/users/<int:userId>")
api.add_resource(GetUsers, "/users")
api.add_resource(Signout, "/auth/logout")
