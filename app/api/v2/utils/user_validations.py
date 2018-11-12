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

    def validate_data_types_signup(self):
        '''Verifies the data types of different data items passed'''

        if len(self.data) > 3:
            Message = "Too many fields entered. Only 3 required"
            abort(400, Message)

        if type(self.data["email"]) is not str:
            Message = "Email must contain string characters only"
            abort(400, Message)

        if type(self.data["password"]) is not str:
            Message = "Password must contain string characters only"
            abort(400, Message)

        if type(self.data["admin"]) is not str:
            Message = "Admin role must contain string characters only"
            abort(400, Message)

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

    def validate_missing_keys_signup(self):
        '''Validates for any missing data keys when someone is signing up'''
        if not self.data:
            Message = "Kindly enter your details"
            abort(400, Message)

        if "email" not in self.data:
            Message = "Must enter email attribute precisely"
            abort(400, Message)

        if "password" not in self.data:
            Message = "Must enter password attribute precisely"
            abort(400, Message)

        if "admin" not in self.data:
            Message = "Must enter admin attribute precisely"
            abort(400, Message)

    def validate_missing_data_signup(self):
        '''Validates for any missing data and invalid
         spaces when someone is signing up'''
        if " " in self.data["email"]:
            Message = "Email cannot have a space"
            abort(400, Message)

        if " " in self.data["password"]:
            Message = "Password cannot have a space"
            abort(400, Message)

        if self.data["email"] == "":
            Message = "Kindly enter your email"
            abort(400, Message)

        if self.data["password"] == "":
            Message = "Kindly enter your password"
            abort(400, Message)

        if self.data["admin"] == "":
            Message = "Kindly enter your admin status true/false"
            abort(400, Message)

    def validate_user_exists(self, data2):
        '''Checks if the registration email already exists on the database'''
        item = User_Model()
        users = item.get()
        for user in users:
            if data2["email"] == user["email"]:
                Message = "User already exists"
                abort(406, Message)

    def validate_missing_data_login(self):
        '''Validates if the data keys are not entered'''

        if not self.data:
            Message = "Kindly enter your details"
            abort(400, Message)

        if "email" not in self.data:
            Message = "Email field must be filled precisely"
            abort(400, Message)

        if "password" not in self.data:
            Message = "Password field must be filled precisely"
            abort(400, Message)

    def validate_empty_items_login(self):
        '''Checks if empty values are entered'''
        if self.data["email"] == "":
            Message = "Kindly enter your email"
            abort(400, Message)

        if self.data["password"] == "":
            Message = "Kindly enter your password"
            abort(400, Message)

        if " " in self.data["email"]:
            Message = "Invalid email check for space characters"
            abort(400, Message)

        if " " in self.data["password"]:
            Message = "Password cant have space characters"
            abort(400, Message)

    def validate_data_types_login(self):
        '''Verifies the data types of different data items passed'''

        if len(self.data) > 2:
            Message = "Too many fields entered. Only email,password required"
            abort(400, Message)

        if type(self.data["email"]) is not str:
            Message = "Email must contain string characters only"
            abort(400, Message)

        if type(self.data["password"]) is not str:
            Message = "Password must contain string characters only"
            abort(400, Message)
