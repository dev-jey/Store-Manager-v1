from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from functools import wraps
from instance.config import app_config
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from .utils import Validator
from .models import User_Model, users

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


