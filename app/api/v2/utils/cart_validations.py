from flask import abort


class Validator_cart(object):
    def __init__(self, data=None):
        self.data = data

    def strip_spacing(self):
        title = self.data["title"].strip().lower()
        quantity = self.data["quantity"]
        new_cart = {
            "title": title,
            "quantity": quantity
        }
        return new_cart

    def validate_data_types(self):
        '''validates datatype of the title passed'''

        if self.data["quantity"] == "":
            Message = "Enter the quantity"
            abort(400, Message)
        try:
            self.data["quantity"] = int(self.data["quantity"])
        except Exception:
            Message = "Quantity must be an integer"
            abort(400, Message)
        if int(self.data["quantity"]) <= 0:
            Message = "Quantity must be more than 0"
            abort(400, Message)
