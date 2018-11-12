from flask import make_response, jsonify, abort


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
            Message = """Too many fields provided, only the title and quantity is required"""
            abort(400, Message)
        try:
            self.data["quantity"] = int(self.data["quantity"])
        except:
            Message = "Enter the quantity"
            abort(400, Message)
        if int(self.data["quantity"]) <= 0:
            Message = "Quantity must be more than 0"
            abort(400, Message)
