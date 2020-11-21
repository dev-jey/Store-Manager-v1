import random
from flask import jsonify, make_response
from flask_restful import Resource
from flask_expects_json import expects_json

from ..models.sales_model import Sale_Model
from ..models.product_models import Product_Model
from .token import Token
from .main import Initialize
from .json_schema import CART_JSON

class Sale(Resource, Initialize):

    @Token.token_required
    def post(current_user, self):
        '''Create an endpoint for attendants to make sales'''
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAttendantStatus(current_user)
        random_id = ' '.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        cart_items = self.cart_obj.get()
        if not cart_items:
            return make_response(jsonify({
                "Message": "No items to sell"
            }), 404)
        for item in cart_items:
            sales_obj = Sale_Model(int(current_user["id"]), int(item["product"]["id"]), int(random_id.replace(" ", "")),
            int(item["quantity"]), int(item["subtotals"]))
            sales_obj.save()
        self.cart_obj.delete()
        return make_response(jsonify({
                "Message": "Success",
                "Sale Made": cart_items
            }), 200)

    @Token.token_required
    def get(current_user, self):
        '''Method for getting all items in cart'''
        self.restrict1.checkUserStatus(current_user)
        sales = self.sales_obj.get(current_user['id'])
        total = 0
        for item in sales:
            total = total + item["subtotals"]
        len_sales = self.sales_obj.checkSales(current_user['id'])
        if len_sales:
            response = make_response(jsonify({
                "Message": "Success",
                "Sales": sales,
                "Total": total
            }), 200)
        else:
            response = self.no_sales
        return response

    @Token.token_required
    def delete(current_user, self):
        '''Method for deleting all items in cart'''
        self.restrict1.checkUserStatus(current_user)
        sales = self.sales_obj.get()
        if not sales:
            return self.no_sales
        self.sales_obj.delete()
        return make_response(jsonify({"message":"Sales deleted"}))

class OneSale(Resource, Initialize):
    @Token.token_required
    def get(current_user, self, itemId):
        '''Gets one item in cart using its item Id'''
        self.restrict1.checkUserStatus(current_user)
        sales = self.sales_obj.get()
        len_sales = self.sales_obj.checkSales()
        if not len_sales:
            return self.no_sales
        for item in sales:
            if int(itemId) == item["id"]:
                self.restrict1.checkUser(current_user, item)
                return make_response(jsonify({
                    "Message": "Success",
                    "Sale": item
                }), 200)
        return self.no_sales
    
    @Token.token_required
    def delete(current_user, self, itemId):
        '''Method for deleting a single item in cart'''
        self.restrict1.checkUserStatus(current_user)
        len_sales = self.sales_obj.checkSales()
        sales = self.sales_obj.get()
        if not len_sales:
            return self.no_sales
        for item in sales:
            if int(itemId) == item["id"]:
                self.restrict1.checkUser(current_user, item)
                self.sales_obj.delete_one(itemId)
                return make_response(jsonify({
                    "Message": "Deleted successfully"
                }), 200)
        return self.no_sales
