from .models.user_model import User_Model
from .models.product_models import Product_Model
from flask import make_response, jsonify, abort
from validate_email import validate_email
import re


class User_validator(object):
    def __init__(self, data):
        self.data = data
    '''User validations undertaken here'''
    def validate_credentials(self):
        item = User_Model()
        users = item.get()
        for user in users:
            if self.data["email"] == user["email"]:
                Message = "User already exists"
                abort(406, Message)
                
    def validate_password(self):
        valid_email = validate_email(self.data["email"])
        if self.data["email"] == "" or self.data["password"] == "" or self.data["role"] == "":
            Message = "Kindly enter your full credentials"
            abort(400, Message)
        if not valid_email:
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
        elif "email" not in self.data or "password" not in self.data or "role" not in self.data:
            Message = "Must enter all credentials"
            abort(400, Message)

    def validate_missing_data(self):
        '''Validates if the data keys are not entered'''
        if "email" not in self.data or "password" not in self.data:
            Message = "Must enter all credentials"
            abort(400, Message)

    def validate_data_types(self):
        '''Verifies the data types of different data items passed'''
        if type(self.data["email"]) is not str or type(self.data["role"]) is not str or type(self.data["password"]) is not str:
            Message = "Details must be strings characters"
            abort(400, Message)

    def validate_data_types_login(self):
        '''Validates data types of data passed during login'''
        if type(self.data["email"]) is not str or type(self.data["password"]) is not str:
            Message = "Details must be strings characters"
            abort(401, Message)


class Validator_products(object):
    def __init__(self, data):
        self.data = data
    def validate_product_description(self):
        '''Product descriptions validated here'''
        if len(self.data["description"]) < 20:
            Message = "Product description cant be less than 20 characters"
            abort(400, Message)
        if self.data["title"] == "" or self.data["category"] == "" or self.data["price"] == "" or self.data["quantity"] == "" or self.data["minimum_stock"] == "":
            Message = "All Product details ought to be filled up"
            abort(400, Message)

    def validate_missing_data(self):
        '''Checks for missing data keys in data passed during product registration'''
        if "title" not in self.data or "category" not in self.data or "price" not in self.data or "quantity" not in self.data or "minimum_stock" not in self.data or "description" not in self.data:
            Message = "Must enter all product details"
            abort(400, Message)

    def validate_data_types(self):
        '''Verifies data types of product details'''
        try:
            self.data["price"] = float(self.data["price"])
        except:
            pass
        if type(self.data["title"]) is not str or type(self.data["category"]) is not str or type(self.data["price"]) is not float or type(self.data["quantity"]) is not int or type(self.data["minimum_stock"]) is not int or type(self.data["description"]) is not str:
            Message = "Wrong data types given"
            abort(400, Message)

    def validate_duplication(self):
        model = Product_Model()
        products = model.get()
        for product in products:
            if self.data["title"] == product["title"]:
                Message = "Product already exists"
                abort(400, Message)

    def validate_negations(self):
        if self.data["price"] < 1 or self.data["quantity"] < 1 or self.data["minimum_stock"] < 0:
            Message = "Price, quantity or minmum stock cant be negative"
            abort(400, Message)

        if self.data["quantity"] < self.data["minimum_stock"]:
            Message = "Minmum stock cant be more than quantity"
            abort(400, Message)


class Validator_sales(object):
    def __init__(self, data):
        self.data = data

    def validate_missing_data(self):
        '''checks for missing data when making a sale'''
        if "productId" not in self.data:
            Message = "Must enter the product Id"
            abort(400, Message) 

    def validate_data_types(self):
        '''validates datatype of the product id passed'''
        if type(self.data["productId"]) is not int:
            Message = "Product Id must be an integer"
            abort(400, Message)