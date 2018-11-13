from ..models.user_model import User_Model
from flask import make_response, jsonify, abort
import re


class User_validator(object):
    def __init__(self, data=None):
        self.data = data

    def space_strip(self):
        email = self.data["email"].strip().lower()
        password = self.data["password"].strip()
        new_person = {
            "email": email,
            "password": password
        }
        return new_person

    def validate_signup_password(self):
        '''Validates legitimacy of a person's signup email and password'''
        if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)",
                        self.data["email"]):
            Message = "Invalid email"
            abort(400, Message)
        elif len(self.data["password"]) < 6 or len(self.data["password"]) > 12:
            Message = "Password must be long than 6 characters or less than 12"
            abort(400, Message)
        elif not any(char.isdigit() for char in self.data["password"]):
            Message = "Password must have a digit"
            abort(400, Message)
        elif not any(char.isupper() for char in self.data["password"]):
            Message = "Password must have an upper case character"
            abort(400, Message)
        elif not any(char.islower() for char in self.data["password"]):
            Message = "Password must have a lower case character"
            abort(400, Message)
        elif not re.search("^.*(?=.*[@#$%^&+=]).*$", self.data["password"]):
            Message = "Password must have a special charater"
            abort(400, Message)

    def validate_user_exists(self, data2):
        '''Checks if the registration email already exists on the database'''
        item = User_Model()
        users = item.get()
        for user in users:
            if data2["email"] == user["email"]:
                Message = "User already exists"
                abort(406, Message)
