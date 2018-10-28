from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from instance.config import app_config
import jwt
import datetime
'''Local imports'''
from .utils import User_validator, Validator_products, Validator_sales
from .models.user_model import User_Model
from .models.product_models import Product_Model
from .models.sale_models import Sales_Model


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
            data = jwt.decode(
                token, app_config["development"].SECRET_KEY, algorithms=['HS256'])
            model = User_Model()
            users = model.get()
            for user in users:
                if user["email"] == data["email"]:
                    current_user = user
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "token invalid"}),
                                 403)
        return fnc(current_user, *args, **kwargs)
    return decorated


class SignUp(Resource):
    '''Signup endpont'''
    @token_required
    def post(current_user, self):
        '''Method to create a new user'''
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide your credentials"
            }), 403)
        valid = User_validator(data)
        valid.validate_missing_keys_signup()
        valid.validate_data_types_signup()
        valid.validate_missing_data_signup()
        valid.validate_signup_password()
        valid.validate_user_exists()
        email = data["email"]
        password = generate_password_hash(data["password"], method='sha256')
        role = data["role"]
        user = User_Model(email, password, role)
        if current_user["role"] == "Admin" or current_user["role"] == "admin":
            user.save()
            return make_response(jsonify({
                "Message": "User registered",
                "Email": email,
                "Role": role
            }), 201)

        return make_response(jsonify({
            "Message": "Permission denied, must be admin"
        }), 201)


class AdminSignUp(Resource):
    '''Signup endpont'''

    def post(self):
        '''Method to create a new user'''
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide your credentials"
            }), 403)
        if data["role"] != "Admin":
            return make_response(jsonify({
                "Message": "Role must be 'Admin'"
            }), 403)
        valid = User_validator(data)
        valid.validate_missing_keys_signup()
        valid.validate_data_types_signup()
        valid.validate_missing_data_signup()
        valid.validate_signup_password()
        valid.validate_user_exists()
        email = data["email"]
        password = generate_password_hash(data["password"], method='sha256')
        role = data["role"]
        user = User_Model(email, password, role)
        user.save()
        return make_response(jsonify({
            "Message": "User registered",
            "Email": email,
            "Role": role
        }), 201)


class UpdateUser(Resource):
    @token_required
    def put(current_user, self, userId):
        '''Update user endpoint'''
        if current_user["role"] == "Admin":
            item = User_Model()
            users = item.get()
            for user in users:
                if user["id"] == userId:
                    if user["role"] != "Admin":
                        item.update(userId)
                        response = make_response(jsonify({
                            "Message": "User updated to:",
                            "Role": "Admin"
                        }), 201)
                    else:
                        response = make_response(jsonify({
                            "message":  "User already an admin"
                        }), 403)
                    return response
            return make_response(jsonify({"message":  "User non-existent"}), 404)
        return make_response(jsonify({
            "Message": "Permission denied, must be admin"
        }), 401)


class Login(Resource):
    '''Login endpoint'''

    def post(self):
        '''Method to login a user and create a unique JWT token'''
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide your credentials"
            }), 403)
        valid = User_validator(data)
        valid.validate_missing_data_login()
        valid.validate_data_types_login()
        valid.validate_empty_items_login()
        email = data["email"].strip()
        password = data["password"].strip()
        users = User_Model.get(self)
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
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide the product's details"
            }), 403)
        valid = Validator_products(data)
        valid.validate_missing_data()
        valid.validate_data_types()
        valid.validate_negations()
        valid.validate_duplication()
        product = Product_Model(data)
        product.save()
        return make_response(jsonify({
            "Message": "Successfully added",
            "Products": product.get()
        }), 201)

    @token_required
    def get(current_user, self):
        '''Get all products endpoint that fetches all products
        and outputs them to the user'''
        if current_user:
            product = Product_Model()
            products = product.get()
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


class OneProduct(Resource):
    @token_required
    def get(current_user, self, productId):
        '''Gets one product using its product id'''
        product = Product_Model()
        products = product.get()
        if len(products) == 0:
            response = make_response(jsonify({
                "Message": "No products yet"
            }), 404)
        if current_user:
            for product in products:
                if int(productId) == product["id"]:
                    return make_response(jsonify({
                        "Message": "Success",
                        "Product": product
                    }), 200)
        return make_response(jsonify({
            "Message": "Product non-existent"
        }), 404)

    @token_required
    def put(current_user, self, productId):
        '''Updates a product details'''
        if current_user and current_user["role"] != "Admin":
            return make_response(jsonify({
                "Message": "You must be an admin"
            }), 403)
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide the product's details"
            }), 403)
        valid = Validator_products(data)
        valid.validate_missing_data()
        valid.validate_data_types()
        valid.validate_negations()
        product = Product_Model(data)
        products = product.get()
        if len(products) == 0:
            return make_response(jsonify({
                "Message": "No products yet"
            }), 404)
        for item in products:
            if int(productId) == item["id"]:
                product.update(productId)
                return make_response(jsonify({
                    "Message": "Successfully updated",
                    "Products": product.get()
                }), 200)
        return make_response(jsonify({
            "Message": "Product non-existent"
        }), 404)

    @token_required
    def delete(current_user, self, productId):
        '''deletes product'''
        product = Product_Model()
        products = product.get()
        if current_user["role"] == "Admin":
            for item in products:
                if productId == item["id"]:
                    product.delete(productId)
                    response = make_response(jsonify({
                        "message": "Deleted successfully"}), 200)
                    return response
        response = make_response(jsonify(
            {"Message": "Attempting to delete a product that doesn't exist"}), 404)
        return response


class Sale(Resource):
    @token_required
    def post(current_user, self):
        '''Create an endpoint for attendants to make sales'''
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide the product's details"
            }), 403)
        if current_user and current_user["role"] == "Attendant":
            valid = Validator_sales(data)
            valid.validate_missing_data()
            valid.validate_data_types()
            productId = data["productId"]
            item = Product_Model(data)
            products = item.get()
            for product in products:
                total_price = 0
                if product["id"] == productId:
                    userId = current_user["id"]
                    sale_obj = Sales_Model(userId, product)
                    if product["quantity"] > 0:
                        product["quantity"] = product["quantity"]-1
                    else:
                        return make_response(jsonify({
                            "Message": "Products sold up"
                        }), 404)

                    sale_obj.save()
                    prod = Product_Model(data)
                    prod.updateQuanitity(product["quantity"], productId)
                    sales = sale_obj.get()
                    for sale in sales:
                        if product["id"] in sale.values():
                            price = int(product["price"])
                            total_price = total_price+price

                    if product["quantity"] < int(product["minimum_stock"]):
                        response = make_response(jsonify({
                            "Message": "Minimum stock reached",
                            "Sales made": products,
                            "total price": total_price
                        }), 201)
                    else:
                        response = make_response(jsonify({
                            "message": "successfully sold",
                            "Sales made": products,
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
            sale_obj = Sales_Model()
            sales = sale_obj.get()
            len_Sales = sale_obj.checkSales()
            if len_Sales:
                response = make_response(jsonify({
                    "Message": "Success",
                    "Sales": sale_obj.get()
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


class OneSale(Resource):
    @token_required
    def get(current_user, self, saleId):
        '''Gets one sale using its sale Id'''
        sale = Sales_Model()
        sales = sale.get()
        len_Sales = sale.checkSales()
        if not len_Sales:
            response = make_response(jsonify({
                "Message": "No sales at all"
            }), 404)
        else:
            for item in sales:
                if int(saleId) == item["id"]:
                    if current_user["role"] == "Admin" or current_user["id"] == item["userId"]:
                        resp = make_response(jsonify({
                            "Message": "Success",
                            "Sale": item
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
