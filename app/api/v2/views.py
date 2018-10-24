from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from instance.config import app_config
import jwt
import datetime
'''Local imports'''
from .utils import User_validator, Validator_products
from .models.user_model import User_Model
from .models.product_models import Product_Model


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
    def post(self):
        '''Method to create a new user'''
        data = request.get_json()
        User_validator.validate_missing_data(self, data)
        User_validator.validate_data_types(self, data)
        User_validator.validate_credentials(self, data)
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


class Login(Resource):
    '''Login endpoint'''
    def post(self):
        '''Method to login a user and create a unique JWT token'''
        data = request.get_json()
        User_validator.validate_missing_data(self, data)
        User_validator.validate_data_types_login(self, data)
        email = data["email"]
        password = data["password"]
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
        data = request.get_json()
        Validator_products.validate_missing_data(self, data)
        Validator_products.validate_data_types(self, data)
        Validator_products.validate_duplication(self, data)
        Validator_products.validate_negations(self, data)
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
                                    "Products": product.get()
                                    }), 201)
