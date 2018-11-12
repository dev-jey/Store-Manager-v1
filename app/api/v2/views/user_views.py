from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from instance.config import app_config
import datetime
import jwt
'''Local imports'''
from ..utils.user_validations import User_validator
from ..models.user_model import User_Model
from .token import Token


class SignUp(Resource):
    '''Signup endpont'''
    @Token.token_required
    def post(current_user, self):
        '''Method to create a new user'''
        if current_user and current_user["admin"]:
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
            user2 = valid.space_strip()
            valid.validate_user_exists(user2)
            email = data["email"].strip().lower()
            password = generate_password_hash(
                data["password"], method='sha256').strip()
            admin = data["admin"]
            if admin not in ["true", "t", "false", "f"]:
                return make_response(jsonify({
                    "message": "Admin can either be true/t or false/f"
                }))
            elif admin not in ["true", "True", "T", "t"]:
                admin = False
            user = User_Model(email, password, admin)
            user.save()
            return make_response(jsonify({
                "Message": "User registered",
                "Email": email,
                "Admin": admin
            }), 201)

        return make_response(jsonify({
            "Message": "Must be admin"
        }), 201)


class Signout(Resource):
    @Token.token_required
    def post(current_user, self):
        try:
            if current_user:
                if 'x-access-token' in request.headers:
                    token = request.headers["x-access-token"]
                    user_obj = User_Model()
                    date = datetime.datetime.now()
                    user_obj.logout(token, date)
                    return make_response(jsonify({
                        "Message": "Successfully logged out"
                    }), 200)
        except Exception:
            return make_response(jsonify({
                "Message": "Error while blacklisting token"
            }), 403)


class UpdateUser(Resource):
    @Token.token_required
    def put(current_user, self, userId):
        '''Update user endpoint'''
        if current_user["admin"]:
            item = User_Model()
            users = item.get()
            for user in users:
                if user["id"] == userId:
                    if not user["admin"]:
                        item.update(userId)
                        response = make_response(jsonify({
                            "Message": "User updated to Administrator"
                        }), 201)
                    else:
                        response = make_response(jsonify({
                            "message":  "User already an admin"
                        }), 403)
                    return response
            return make_response(
                jsonify({
                    "message":  "User non-existent"
                }), 404)
        return make_response(jsonify({
            "Message": "Must be admin"
        }), 401)


class GetUsers(Resource):
    @Token.token_required
    def get(current_user, self):
        if not current_user:
            return make_response(jsonify({
                "Message": "Must be a user to view users"
            }), 401)
        item = User_Model()
        users = item.get()
        return make_response(jsonify({
            "Message": "Success",
            "Users": users
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
        user2 = User_Model()
        users = user2.get()
        for user in users:
            if email == user["email"] and check_password_hash(user["password"],
                                                              password):
                token = jwt.encode({"email": email, "password": password,
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(minutes=180000)},
                                   app_config["development"].SECRET_KEY,
                                   algorithm='HS256')
                return make_response(jsonify({
                    "message": "Login success",
                    "token": token.decode("UTF-8"
                                          )}), 200)
        return make_response(jsonify({
            "Message": "Login failed, check credentials"
        }), 403)
