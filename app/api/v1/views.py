from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from functools import wraps
from instance.config import app_config
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

'''Local imports'''
from .utils import User_validator, Validator_products, Validator_sales
from .models import User_Model, users, Product_Model, products, Sales_Model, sales


def token_required(fnc):
    '''Creates decorator to decode tokens and assign them to current users'''
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
            data = jwt.decode(token, app_config["development"].SECRET_KEY, algorithms=['HS256'])
            for user in users:
                if user["email"] == data["email"]:
                    current_user = user
        except:
            return make_response(jsonify({"message": "token invalid"}),
                                 403)
        return fnc(current_user, *args, **kwargs)
    return decorated


class SignUp(Resource):
    '''Signup endpont'''
    def post(self):
        '''Method to create a new user'''
        data = request.get_json()
        User_validator.validate_missing_data(self, data)
        User_validator.validate_data_types(self, data)
        email = data["email"]
        password = generate_password_hash(data["password"], method='sha256')
        role = data["role"]
        user = User_Model(email, password, role)
        User_validator.validate_credentials(self, data)
        user.save()
        return make_response(jsonify({
                                    "Message": "User registered",
                                    "Email": email,
                                    "Role": role
                                    }), 201)


class Login(Resource):
    '''Login endpoint'''
    def post(self):
        '''Method to login a user and create a unique JWT token'''
        data = request.get_json()
        User_validator.validate_missing_data(self, data)
        User_validator.validate_data_types_login(self, data)
        email = data["email"]
        password = data["password"]
        for user in users:
            if email == user["email"] and check_password_hash(user["password"],
                                                              password):
                token = jwt.encode({"email": email, "password": password,
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(minutes=30)},
                                   app_config["development"].SECRET_KEY, algorithm='HS256')
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
        '''Post product endpoint that creates a new product'''
        if current_user and current_user["role"] != "Admin":
            return make_response(jsonify({
                                    "Message": "You must be an admin"
                                    }), 403)
        data = request.get_json()
        Validator_products.validate_missing_data(self, data)
        Validator_products.validate_data_types(self, data)
        Validator_products.validate_duplication(self, data)
        Validator_products.validate_negations(self, data)
        id = len(products) + 1
        title = data["title"]
        category = data["category"]
        price = data["price"]
        quantity = data["quantity"]
        minimum_stock = data["minimum_stock"]
        description = data["description"]
        product = Product_Model(data)
        Validator_products.validate_product_description(self, data)
        product.save()
        return make_response(jsonify({
                                    "Message": "Successfully added",
                                    "Products": products
                                    }), 201)

    @token_required
    def get(current_user, self):
        '''Get all products endpoint that fetches all products
        and outputs them to the user'''
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
        else:
            return make_response(jsonify({
                                        "message": "Must be logged in"
                                        }), 401)


class Sale(Resource):
    @token_required
    def post(current_user, self):
        '''Create an endpoint for attendants to make sales'''
        data = request.get_json()
        if current_user and current_user["role"] == "Attendant":
            Validator_sales.validate_missing_data(self, data)
            Validator_sales.validate_data_types(self, data)
            id = len(sales) + 1
            productId = data["productId"]
            for product in products:
                total_price = 0
                if product["productId"] == productId:
                        userId = current_user["id"]
                        sale_obj = Sales_Model(id, userId, product)
                        product["quantity"] = product["quantity"]-1
                        sale_obj.save()
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

    @token_required
    def get(current_user, self):
        '''Method for getting all sales'''
        if current_user and current_user["role"] == "Admin":
            if len(sales) > 0:
                response = make_response(jsonify({
                                            "Message": "Success",
                                            "Sales": sales
                                                }), 200)
            else:
                response = make_response(jsonify({
                                        "Message": "Failure, no sales made yet"
                                                 }), 404)
            return response
        else:
            return make_response(jsonify({
                                        "Message": "Must be an admin"
                                        }), 401)


class OneProduct(Resource):
    @token_required
    def get(current_user, self, productId):
        '''Gets one product using its product id'''
        if len(products) == 0:
            response = make_response(jsonify({
                            "Message": "No products yet"
                            }), 404)
        if current_user:
            for product in products:
                if int(productId) == product["productId"]:
                    return make_response(jsonify({
                                                "Message": "Success",
                                                "Product": product
                                                }), 200)
        return make_response(jsonify({
                                "Message": "Product non-existent"
                                }), 404)


class OneSale(Resource):
    @token_required
    def get(current_user, self, saleId):
        '''Gets one sale using its sale Id'''
        if len(sales) == 0:
            response = make_response(jsonify({
                            "Message": "No sales at all"
                            }), 404)
        else:
            for sale in sales:
                if int(saleId) == sale["saleId"]:
                    if current_user["role"] == "Admin" or current_user["id"] == sale["userId"]:
                        resp = make_response(jsonify({
                                    "Message": "Success",
                                    "Sale": sale
                                    }), 200)
                    else:
                        resp = make_response(jsonify({
                                    "Message": "Access denied"
                                    }), 401)
                    return resp
                else:
                    response = make_response(jsonify({
                                    "Message": "Sale non-existent"
                                    }), 404)
        return response

