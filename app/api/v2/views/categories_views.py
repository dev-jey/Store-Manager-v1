from flask import jsonify, make_response
from flask_restful import Resource
from flask_expects_json import expects_json

from ..utils.category_validations import Validator_Category
from ..models.category_model import Category_Model
from .token import Token
from .main import Initialize
from .json_schema import CATEGORY_JSON


class Category(Resource, Initialize):

    @expects_json(CATEGORY_JSON)
    @Token.token_required
    def post(current_user, self):
        '''Create an endpoint for attendants to add categories'''
        data = self.restrict1.getJsonData()
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAdminStatus(current_user)
        title = data["title"].strip()
        valid = Validator_Category(data)
        valid.check_data_types()
        valid.check_duplicate()
        category_obj = Category_Model(data)
        category_obj.save()
        return make_response(jsonify({
            "message": "successfully added",
            "category": title
        }), 201)

    @Token.token_required
    def get(current_user, self):
        '''Method for getting all categories in the system'''
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAdminStatus(current_user)
        categories = self.category_obj.get()
        if not len(categories):
            return self.restrict1.no_categories
        return make_response(jsonify({
            "message": "Success",
            "categories": categories
        }))

    @Token.token_required
    def delete(current_user, self):
        '''Method for deleting all categories'''
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAdminStatus(current_user)
        self.category_obj.delete()
        return make_response(
            jsonify({"message": "Categories deleted"}), 200)


class OneCategory(Resource, Initialize):
    @Token.token_required
    def get(current_user, self, itemId):
        '''Gets one category in cart using its name'''
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAdminStatus(current_user)
        for category in self.category_obj.get():
            if category["id"] == itemId:
                category = self.category_obj.get_one(itemId)
                return make_response(jsonify({
                    "message": "success",
                    "category": category
                }), 200)
        return self.restrict1.no_categories

    @Token.token_required
    def put(current_user, self, itemId):
        '''Method for updating a single category'''
        data = self.restrict1.getJsonData()
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAdminStatus(current_user)
        title = data["title"].strip()
        valid = Validator_Category(data)
        valid.check_data_types()
        for category in self.category_obj.get():
            if category["id"] == itemId:
                category_obj = Category_Model(data)
                category = category_obj.update_one(itemId)
                new_category = category_obj.get_one(itemId)
                return make_response(jsonify({
                    "message": "successfully updated",
                    "New category": new_category
                }), 200)
        return self.restrict1.no_categories

    @Token.token_required
    def delete(current_user, self, itemId):
        '''Method for deleting a single category'''
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAdminStatus(current_user)
        for category in self.category_obj.get():
            if category["id"] == itemId:
                category = self.category_obj.delete_one(itemId)
                return make_response(jsonify({
                    "message": "successfully deleted"
                }), 200)
        return self.restrict1.no_categories
