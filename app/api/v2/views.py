from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from instance.config import app_config
import jwt
import datetime
'''Local imports'''
from .utils import User_validator
from .models.user_model import User_Model


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
