from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
'''Local imports'''
from ..utils.sales_validations import Validator_sales
from ..models.product_models import Product_Model
from ..models.sale_models import Sales_Model
from .token import Token
from .main import Initialize


class Sale(Resource, Initialize):

    @Token.token_required
    def post(current_user, self):
        '''Create an endpoint for attendants to make sales'''
        data = self.restrict1.getJsonData()
        if not current_user:
            return self.must_login
        if current_user["admin"]:
            return self.only_attendant
        valid = Validator_sales(data)
        valid.validate_missing_data()
        valid.validate_data_types()
        title = data["title"].strip().lower()
        products = self.item.get()
        for product in products:
            if product["title"] == title:
                price = int(product["price"]) * data["quantity"]
                email = current_user["email"]
                sale_obj = Sales_Model(
                    email, product, data["quantity"], price)

                self.restrict1.restrictSales(data, product, price)
                sale_obj.save()
                self.item.updateQuanitity(product["quantity"], title)
                if product["quantity"] < int(product["minimum_stock"]):
                    return make_response(jsonify({
                        "Message": "Minimum stock reached",
                        "Sales made": product,
                        "Total": price
                    }), 201)
                return make_response(jsonify({
                    "message": "successfully sold",
                    "Sales made": product,
                    "Total": price
                }), 201)
        return self.no_products

    @Token.token_required
    def get(current_user, self):
        '''Method for getting all sales'''
        if not current_user:
            return self.must_login
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
        if not current_user:
            return self.must_login
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
