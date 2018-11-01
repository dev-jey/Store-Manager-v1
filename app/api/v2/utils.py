from .models.user_model import User_Model
from .models.product_models import Product_Model
from flask import make_response, jsonify, abort
from validate_email import validate_email
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
        if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", self.data["email"]):
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
        '''Validates for any missing data and invalid spaces when someone is signing up'''
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


class Validator_products(object):
    def __init__(self, data):
        self.data = data

    def validate_data_types(self):
        '''Verifies data types of product details'''
        if len(self.data) > 6:
            Message = "Error, Excess fields given"
            abort(400, Message)
        try:
            self.data["price"] = float(self.data["price"])
            self.data["quantity"] = int(self.data["quantity"])
            self.data["minimum_stock"] = int(self.data["minimum_stock"])
        except:
            pass
        if type(self.data["title"]) is not str:
            Message = "Title field only accepts a string"
            abort(400, Message)

        if type(self.data["category"]) is not str:
            Message = "Category field only accepts a string"
            abort(400, Message)

        if type(self.data["price"]) is not float:
            Message = "Price field only accepts a float or an integer"
            abort(400, Message)

        if type(self.data["quantity"]) is not int:
            Message = "Quantity field only accepts an integer"
            abort(400, Message)

        if type(self.data["minimum_stock"]) is not int:
            Message = "Minimum stock field only accepts an integer"
            abort(400, Message)

        if len(self.data["description"]) < 20:
            Message = "Product description cant be less than 20 characters"
            abort(400, Message)

    def validate_missing_data(self):
        '''Checks for missing data keys in data passed during product registration'''

        if not self.data:
            Message = "No product details given yet"
            abort(400, Message)

        if "title" not in self.data:
            Message = "Product title key/field missing or mistyped"
            abort(400, Message)

        if "category" not in self.data:
            Message = "Product category key/field missing or mistyped"
            abort(400, Message)

        if "price" not in self.data:
            Message = "Product price key/field missing or mistyped"
            abort(400, Message)

        if "quantity" not in self.data:
            Message = "Product quantity key/field missing or mistyped"
            abort(400, Message)

        if "minimum_stock" not in self.data:
            Message = "Product minimum stock key/field missing or mistyped"
            abort(400, Message)

        if "description" not in self.data:
            Message = "Product description key/field missing or mistyped"
            abort(400, Message)

        if self.data["title"] == "":
            Message = "Product title is missing"
            abort(400, Message)

        if self.data["category"] == "":
            Message = "Product category is missing"
            abort(400, Message)

        if self.data["price"] == "":
            Message = "Product price is missing"
            abort(400, Message)

        if self.data["quantity"] == "":
            Message = "Product quantity is missing"
            abort(400, Message)

        if self.data["minimum_stock"] == "":
            Message = "Product minimum_stock is missing"
            abort(400, Message)

        if self.data["description"] == "":
            Message = "Product description is missing"
            abort(400, Message)

    def validate_duplication(self, data2):
        '''Checks if the product title to be registered already exists in database'''
        model = Product_Model()
        products = model.get()
        for product in products:
            if data2["title"] == product["title"]:
                Message = "Product already exists"
                abort(400, Message)

    def validate_negations(self):
        '''Checks to avoid any negative interger/float values from being registered'''
        if self.data["price"] < 1 or self.data["quantity"] < 1 or self.data["minimum_stock"] < 0:
            Message = "Price, quantity or minmum stock cant be negative"
            abort(400, Message)

        if self.data["quantity"] < self.data["minimum_stock"]:
            Message = "Minmum stock cant be more than quantity"
            abort(400, Message)

    def strip_spaces(self):
        title = self.data["title"].strip().lower()
        category = self.data["category"].strip().lower()
        quantity = self.data["quantity"]
        price = self.data["price"]
        minimum_stock = self.data["minimum_stock"]
        description = self.data["description"].strip().lower()
        new_prod = {
            "title": title,
            "category": category,
            "quantity": quantity,
            "price": price,
            "minimum_stock": minimum_stock,
            "description": description
        }
        return new_prod


class Validator_sales(object):
    def __init__(self, data=None):
        self.data = data

    def strip_spacing(self):
        title = self.data["title"].strip().lower()
        quantity = self.data["quantity"]
        new_sale = {
            "title": title,
            "quantity": quantity
        }
        return new_sale

    def validate_missing_data(self):
        '''checks for missing data when making a sale'''
        if not self.data:
            Message = "Must enter the product details in the body"
            abort(400, Message)

        if "title" not in self.data:
            Message = "Must enter the title key well"
            abort(400, Message)

        if "quantity" not in self.data:
            Message = "Must enter the quantity key well"
            abort(400, Message)

    def validate_data_types(self):
        '''validates datatype of the title passed'''
        if len(self.data) > 2:
            Message = "Too many fields provided, only the title and quantity is required"
            abort(400, Message)

        if type(self.data["title"]) is not str:
            Message = "title must be a string"
            abort(400, Message)

        if type(self.data["quantity"]) is not int:
            Message = "Quantity must be an integer"
            abort(400, Message)

        if self.data["quantity"] <= 0:
            Message = "Quantity must be more than 0"
            abort(400, Message)
