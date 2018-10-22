from flask import make_response, jsonify, abort
from validate_email import validate_email
import re

from .models import users, products


class User_validator(object):
    '''User validations undertaken here'''
    def validate_credentials(self, data):
        valid_email = validate_email(data["email"])
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


class Validator_products(object):
    def validate_product_description(self, data):
        '''Product descriptions validated here'''
        if len(data["description"]) < 20:
            Message = "Product description cant be less than 20 characters"
            abort(400, Message)
        if data["title"] == "" or data["category"] == "" or data["price"] == "" or data["quantity"] == "" or data["minimum_stock"] == "":
            Message = "All Product details ought to be filled up"
            abort(400, Message)

    def validate_missing_data(self, data):
        '''Checks for missing data keys in data passed during product registration'''
        if "title" not in data or "category" not in data or "price" not in data or "quantity" not in data or "minimum_stock" not in data or "description" not in data:
            Message = "Must enter all product details"
            abort(400, Message)

    def validate_data_types(self, data):
        '''Verifies data types of product details'''
        try:
            data["price"] = float(data["price"])
        except:
            pass
        if type(data["title"]) is not str or type(data["category"]) is not str or type(data["price"]) is not float or type(data["quantity"]) is not int or type(data["minimum_stock"]) is not int or type(data["description"]) is not str:
            Message = "Wrong data types given"
            abort(400, Message)

    def validate_duplication(self, data):
        for product in products:
            if data["title"] == product["title"]:
                Message = "Product already exists"
                abort(400, Message)

    def validate_negations(self, data):
        if data["price"] < 1 or data["quantity"] < 1 or data["minimum_stock"] < 0:
            Message = "Price, quantity or minmum stock cant be negative"
            abort(400, Message)

        if data["quantity"] < data["minimum_stock"]:
            Message = "Minmum stock cant be more than quantity"
            abort(400, Message)


class Validator_sales(object):
    def validate_missing_data(self, data):
        '''checks for missing data when making a sale'''
        if "productId" not in data:
            Message = "Must enter the product Id"
            abort(400, Message) 

    def validate_data_types(self, data):
        '''validates datatype of the product id passed'''
        if type(data["productId"]) is not int:
            Message = "Product Id must be an integer"
            abort(400, Message)
