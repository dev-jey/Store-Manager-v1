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
from .restrict import Restrictions


class SignUp(Resource):
    '''Signup endpont'''

    def __init__(self):
        self.restrict1 = Restrictions()
        self.only_admin = self.restrict1.only_admin
        self.must_login = self.restrict1.must_login

    @Token.token_required
    def post(current_user, self):
        '''Method to create a new user'''
        if not current_user:
            return self.must_login
        if not current_user["admin"]:
            return self.only_admin
        data = self.restrict1.getJsonData()
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
        self.restrict1.checkAdmin(admin)
        user = User_Model(email, password, admin)
        user.save()
        return make_response(jsonify({
            "Message": "User registered",
            "Email": email,
            "Admin": admin
        }), 201)


class Signout(Resource):
    def __init__(self):
        self.restrict1 = Restrictions()
        self.must_login = self.restrict1.must_login
        self.item = User_Model()

    @Token.token_required
    def post(current_user, self):
        if not current_user:
            return self.must_login
        if 'x-access-token' in request.headers:
            token = request.headers["x-access-token"]
            date = datetime.datetime.now()
            self.item.logout(token, date)
            return make_response(jsonify({
                "Message": "Successfully logged out"
            }), 200)


class UpdateUser(Resource):
    def __init__(self):
        self.restrict1 = Restrictions()
        self.must_login = self.restrict1.must_login
        self.only_admin = self.restrict1.only_admin
        self.no_user = self.restrict1.no_user
        self.item = User_Model()

    @Token.token_required
    def put(current_user, self, userId):
        '''Update user endpoint'''
        if not current_user["admin"]:
            return self.only_admin
        users = self.item.get()
        for user in users:
            if user["id"] == userId:
                if not user["admin"]:
                    self.item.update(userId)
                    response = make_response(jsonify({
                        "Message": "User updated to Administrator"
                    }), 201)
                else:
                    response = make_response(jsonify({
                        "message":  "User already an admin"
                    }), 403)
                return response
        return self.no_user


class GetUsers(Resource):
    def __init__(self):
        self.restrict1 = Restrictions()
        self.must_login = self.restrict1.must_login
        self.no_user = self.restrict1.no_user
        self.item = User_Model()

    @Token.token_required
    def get(current_user, self):
        if not current_user:
            return self.must_login
        users = self.item.get()
        if len(users) < 1:
            return self.no_user
        return make_response(jsonify({
            "Message": "Success",
            "Users": users
        }), 401)


class Login(Resource):
    '''Login endpoint'''

    def __init__(self):
        self.restrict1 = Restrictions()
        self.must_login = self.restrict1.must_login
        self.no_user = self.restrict1.no_user
        self.fail_login = self.restrict1.login_failed
        self.item = User_Model()

    def post(self):
        '''Method to login a user and create a unique JWT token'''
        data = self.restrict1.getJsonData()
        valid = User_validator(data)
        valid.validate_missing_data_login()
        valid.validate_data_types_login()
        valid.validate_empty_items_login()
        email = data["email"].strip()
        password = data["password"].strip()
        users = self.item.get()
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
        return self.fail_login