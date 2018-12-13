from flask import abort
from ..models.category_model import Category_Model


class Validator_Category(object):
    def __init__(self, data=None):
        self.data = data

    def check_data_types(self):
        if all(char.isdigit() for char in self.data["title"]):
            abort(400, "Enter a valid category")

    def check_duplicate(self):
        category_obj = Category_Model()
        categories = category_obj.get()
        for category in categories:
            if self.data["title"].strip().lower() == category["title"].strip().lower():
                abort(406, "Category already exists")
