from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
'''Local imports'''
from ..utils.sales_validations import Validator_sales
from ..models.product_models import Product_Model
from ..models.sale_models import Sales_Model
from .token import Token


class Sale(Resource):

    @Token.token_required
    def post(current_user, self):
        '''Create an endpoint for attendants to make sales'''
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide the product's details"
            }), 403)
        if current_user and not current_user["admin"]:
            valid = Validator_sales(data)
            valid.validate_missing_data()
            valid.validate_data_types()
            title = data["title"].strip().lower()
            item = Product_Model()
            products = item.get()
            for product in products:
                if product["title"] == title:
                    price = int(product["price"]) * data["quantity"]
                    email = current_user["email"]
                    sale_obj = Sales_Model(
                        email, product, data["quantity"], price)
                    if data["quantity"] > product["quantity"] and product["quantity"] != 0:
                        return make_response(jsonify({
                            "Message": "Attempting to sell more than there is in stock"
                        }), 404)
                    elif product["quantity"] > 0:
                        product["quantity"] = product["quantity"] - \
                            data["quantity"]
                    else:
                        return make_response(jsonify({
                            "Message": "Products sold up"
                        }), 404)

                    sale_obj.save()
                    item.updateQuanitity(product["quantity"], title)
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
            return make_response(jsonify({
                "Message": "Product non-existent"
            }), 404)
        else:
            return make_response(jsonify({
                "Message": "Must be an attendant!"
            }), 401)

    @Token.token_required
    def get(current_user, self):
        '''Method for getting all sales'''
        if current_user:
            sale_obj = Sales_Model()
            sales = sale_obj.get()
            total = 0
            for sale in sales:
                total = total + sale["subtotals"]
            len_Sales = sale_obj.checkSales()
            if len_Sales:
                response = make_response(jsonify({
                    "Message": "Success",
                    "Sales": sales,
                    "Total": total
                }), 200)
            else:
                response = make_response(jsonify({
                    "Message": "Failure, no sales made yet"
                }), 404)
            return response
        else:
            return make_response(jsonify({
                "Message": "Must be logged in"
            }), 401)


class OneSale(Resource):
    @Token.token_required
    def get(current_user, self, saleId):
        '''Gets one sale using its sale Id'''
        if current_user:
            sale = Sales_Model()
            sales = sale.get()
            len_Sales = sale.checkSales()
            if not len_Sales:
                response = make_response(jsonify({
                    "Message": "No sales at all"
                }), 404)
            else:
                for item in sales:
                    if int(saleId) == item["id"]:
                        if current_user["admin"] or current_user["email"] == item["email"]:
                            resp = make_response(jsonify({
                                "Message": "Success",
                                "Sale": item
                            }), 200)
                        else:
                            resp = make_response(jsonify({
                                "Message": "Access denied"
                            }), 401)
                        return resp
                    else:
                        response = make_response(jsonify({
                            "Message": "Sale non-existent"
                        }), 404)
            return response
        return make_response(jsonify({
            "message": "Must be logged in"
        }), 403)
