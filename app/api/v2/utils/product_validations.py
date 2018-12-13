from ..models.product_models import Product_Model
from ..models.category_model import Category_Model
from flask import abort


class Validator_products(object):
    def __init__(self, data):
        self.data = data
        self.model = Product_Model()
        self.products = self.model.get()

    def validate_negations(self):
        '''Checks to avoid any negative interger/float values 
           from being registered'''
        if int(self.data["price"]) < 1 or int(self.data["quantity"]) < 1 or int(self.data["minimum_stock"]) < 0:
            Message = "Price, quantity or minmum stock cant be negative"
            abort(400, Message)

        if self.data["quantity"] < self.data["minimum_stock"]:
            Message = "Minmum stock cant be more than quantity"
            abort(400, Message)

    def check_category_valid(self):
        '''checks if entered category is valid'''
        category_obj = Category_Model()
        categories = category_obj.get()
        there = [cat for cat in categories if cat["title"].strip(
        ).lower() == self.data["category"].strip().lower()]
        if not there:
            abort(400, "Category non existent")

    def validate_length_of_data(self):
        '''Verifies data types of product details'''
        if len(self.data["description"]) < 20:
            Message = "Product description cant be less than 20 characters"
            abort(400, Message)
        if not self.data:
            Message = "No product details given yet"
            abort(400, Message)

    def check_data_type_not_string(self):
        if type(self.data["price"]) is not float:
            Message = "Price field only accepts a float or an integer"
            abort(400, Message)

        if type(self.data["quantity"]) is not int:
            Message = "Quantity field only accepts an integer"
            abort(400, Message)

        if type(self.data["minimum_stock"]) is not int:
            Message = "Minimum stock field only accepts an integer"
            abort(400, Message)

    def validate_data_types(self):
        '''Verifies data types of product details'''
        try:
            self.data["price"] = float(self.data["price"])
            self.data["quantity"] = int(self.data["quantity"])
            self.data["minimum_stock"] = int(self.data["minimum_stock"])
        except Exception:
            self.check_data_type_not_string()

    def strip_spaces(self):
        title = self.data["title"].lower()
        category = self.data["category"].lower()
        quantity = self.data["quantity"]
        price = self.data["price"]
        minimum_stock = self.data["minimum_stock"]
        description = self.data["description"].lower()
        new_prod = {
            "title": title,
            "category": category,
            "quantity": quantity,
            "price": price,
            "minimum_stock": minimum_stock,
            "description": description
        }
        return new_prod

    def validate_duplication(self, data2):
        '''Checks if the product title to be
         registered already exists in database'''
        for product in self.products:
            if data2["title"] == product["title"].lower():
                Message = "Product already exists"
                abort(400, Message)

    def check_empty(self):
        if self.data["title"] == "":
            Message = "Product title is missing"
            abort(400, Message)

        if self.data["category"] == "":
            Message = "Product category is missing"
            abort(400, Message)

    def check_int_empty(self):
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

    def validate_availability(self):
        if len(self.products) < 0:
            Message = "No product/products found"
            abort(404, Message)
