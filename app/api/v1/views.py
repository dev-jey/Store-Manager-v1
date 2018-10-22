from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from functools import wraps
from instance.config import app_config
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from .utils import Validator
from .models import User_Model, users, Product_Model, products, sales


def token_required(fnc):
        @wraps(fnc)
        def decorated(*args, **kwargs):
            token = None
            current_user = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return make_response(jsonify({
                            "message": "Token Missing, Login to get one"
                                            }), 401)
            try:
                data = jwt.decode(token, app_config["development"].SECRET_KEY)
                for user in users:
                    if user["email"] == data["email"]:
                        current_user = user
            except:
                return make_response(jsonify({"message": "token invalid"}),
                                     403)
            return fnc(current_user, *args, **kwargs)
        return decorated


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                                    "Message": "Kindly enter credentials"
                                    }), 400)
        email = data["email"]
        password = generate_password_hash(data["password"], method='sha256')
        role = data["role"]
        user = User_Model(email, password, role)
        Validator.validate_credentials(self, data)
        user.save()
        return make_response(jsonify({
                                    "Message": "Success",
                                    "users": users
                                    }), 201)


class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                            "message": "Kindly enter your credentials",
                            }), 400)
        email = data["email"]
        password = data["password"]
        for user in users:
            if email == user["email"] and check_password_hash(user["password"],
                                                              password):
                token = jwt.encode({"email": email, "password": password,
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(minutes=30)},
                                   app_config["development"].SECRET_KEY)
                return make_response(jsonify({
                                "message": "Login success",
                                "token": token.decode("UTF-8"
                                                      )}), 200)
        return make_response(jsonify({
                        "Message": "Login failed, check credentials"
                        }), 403)


class Product(Resource):
    @token_required
    def post(current_user, self):
        if current_user and current_user["role"] != "Admin":
            return make_response(jsonify({
                                    "Message": "You must be an admin"
                                    }), 403)
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                            "message": "Kindly enter product details",
                            }), 400)
        id = len(products) + 1
        title = data["title"]
        category = data["category"]
        price = data["price"]
        quantity = data["quantity"]
        minimum_stock = data["minimum_stock"]
        description = data["description"]
        product = Product_Model(title, category, price, quantity,
                                minimum_stock, description)
        Validator.validate_product_description(self, data)
        product.save()
        return make_response(jsonify({
                                    "Message": "Successfully added",
                                    "Products": products
                                    }), 201)

    @token_required
    def get(current_user, self):
        if current_user:
            if len(products) > 0:
                response = make_response(jsonify({
                                        "products": products
                                        }), 200)
            else:
                response = make_response(jsonify({
                    "Message": "No products found"
                                                 }), 404)
        return response


class Sale(Resource):

    @token_required
    def post(current_user, self):
        if current_user and current_user["role"] == "Attendant":
            data = request.get_json()
            if not data:
                return jsonify({
                                "message": "Kindly enter product to sell",
                                }, 400)
            id = len(sales) + 1
            productId = data["productId"]
            for product in products:
                total_price = 0
                if product["productId"] == productId:
                        userId = current_user["id"]
                        new_sale = {
                            "saleId": id,
                            "userId": userId,
                            "product": product
                        }
                        product["quantity"] = product["quantity"]-1
                        sales.append(new_sale)
                        for sale in sales:
                            if product["productId"] in sale.values():
                                price = int(product["price"])
                            total_price = total_price+price

                        if product["quantity"] <= 0:
                            response = make_response(jsonify({
                                            "Message": "Products sold up"
                                            }), 404)
                        elif product["quantity"] < product["minimum_stock"]:
                            response = make_response(jsonify({
                                            "Message": "Minimum stock reached",
                                            "Sales made": sales,
                                            "total price": total_price
                                            }), 201)
                        else:
                            response = make_response(jsonify({
                                                "message": "successfully sold",
                                                "Sales made": sales,
                                                "total price": total_price
                                                }), 201)
                        return response
            return make_response(jsonify({
                                        "Message": "Product non-existent"
                                        }), 404)
        else:
            return make_response(jsonify({
                                        "Message": "Must be an attendant!"
                                        }), 401)
