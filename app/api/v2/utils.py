from .models.user_model import User_Model

from flask import make_response, jsonify, abort
from validate_email import validate_email
import re


class User_validator(object):
    '''User validations undertaken here'''
    def validate_credentials(self, data):
        valid_email = validate_email(data["email"])
        users = User_Model.get(self)
        for user in users:
            if data["email"] == user["email"]:
                Message = "User already exists"
                abort(406, Message)
        if data["email"] == "" or data["password"] == "" or data["role"] == "":
            Message = "Kindly enter your full credentials"
            abort(400, Message)
        if not valid_email:
            Message = "Invalid email"
            abort(400, Message)
        elif len(data["password"]) < 6 or len(data["password"]) > 12:
            Message = "Password must be long than 6 characters or less than 12"
            abort(400, Message)
        elif not any(char.isdigit() for char in data["password"]):
            Message = "Password must have a digit"
            abort(400, Message)
        elif not any(char.isupper() for char in data["password"]):
            Message = "Password must have an upper case character"
            abort(400, Message)
        elif not any(char.islower() for char in data["password"]):
            Message = "Password must have a lower case character"
            abort(400, Message)
        elif not re.search("^.*(?=.*[@#$%^&+=]).*$", data["password"]):
            Message = "Password must have a special charater"
            abort(400, Message)
        elif "email" not in data or "password" not in data or "role" not in data:
            Message = "Must enter all credentials"
            abort(400, Message)

    def validate_missing_data(self, data):
        '''Validates if the data keys are not entered'''
        if "email" not in data or "password" not in data:
            Message = "Must enter all credentials"
            abort(400, Message)

    def validate_data_types(self, data):
        '''Verifies the data types of different data items passed'''
        if type(data["email"]) is not str or type(data["role"]) is not str or type(data["password"]) is not str:
            Message = "Details must be strings characters"
            abort(400, Message)

    def validate_data_types_login(self, data):
        '''Validates data types of data passed during login'''
        if type(data["email"]) is not str or type(data["password"]) is not str:
            Message = "Details must be strings characters"
            abort(401, Message)
