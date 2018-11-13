from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from flask_expects_json import expects_json
'''Local imports'''
from ..utils.sales_validations import Validator_sales
from ..models.product_models import Product_Model
from ..models.sale_models import Sales_Model
from .token import Token
from .main import Initialize
from .json_schema import SALE_JSON


class Sale(Resource, Initialize):

    @expects_json(SALE_JSON)
    @Token.token_required
    def post(current_user, self):
        '''Create an endpoint for attendants to make sales'''
        data = self.restrict1.getJsonData()
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAttendantStatus(current_user)
        valid = Validator_sales(data)
        valid.validate_data_types()
        title = data["title"].strip().lower()
        products = self.product.get()
        for product in products:
            if product["title"] == title:
                price = int(product["price"]) * data["quantity"]
                email = current_user["email"]
                sale_obj = Sales_Model(
                    email, product, data["quantity"], price)
                self.restrict1.restrictSales(data, product, price)
                sale_obj.save()
                self.product.updateQuanitity(product["quantity"], title)
                if product["quantity"] < int(product["minimum_stock"]):
                    response = make_response(jsonify({
                        "Message": "Minimum stock reached",
                        "Sales made": product,
                        "Total": price
                    }), 201)
                else:
                    response = make_response(jsonify({
                        "message": "successfully sold",
                        "Sales made": product,
                        "Total": price
                    }), 201)
                return response
        return self.no_products

    @Token.token_required
    def get(current_user, self):
        '''Method for getting all sales'''
        self.restrict1.checkUserStatus(current_user)
        sales = self.sales_obj.get()
        total = 0
        for sale in sales:
            total = total + sale["subtotals"]
        len_Sales = self.sales_obj.checkSales()
        if len_Sales:
            response = make_response(jsonify({
                "Message": "Success",
                "Sales": sales,
                "Total": total
            }), 200)
        else:
            response = self.no_sales
        return response


class OneSale(Resource, Initialize):
    @Token.token_required
    def get(current_user, self, saleId):
        '''Gets one sale using its sale Id'''
        self.restrict1.checkUserStatus(current_user)
        sales = self.sales_obj.get()
        len_Sales = self.sales_obj.checkSales()
        if not len_Sales:
            return self.no_sales
        for item in sales:
            if int(saleId) == item["id"]:
                self.restrict1.checkUser(current_user, item)
                return make_response(jsonify({
                    "Message": "Success",
                    "Sale": item
                }), 200)
        return self.no_sales
