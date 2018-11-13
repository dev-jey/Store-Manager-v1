from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
'''Local imports'''
from ..utils.product_validations import Validator_products
from ..models.product_models import Product_Model
from .token import Token
from .restrict import Restrictions


class Product(Resource):
    def __init__(self):
        self.restrict1 = Restrictions()
        self.only_admin = self.restrict1.only_admin
        self.must_login = self.restrict1.must_login
        self.no_products = self.restrict1.no_products
        self.product = Product_Model()

    @Token.token_required
    def post(current_user, self):
        '''Post product endpoint that creates a new product'''
        if current_user and not current_user["admin"]:
            return self.only_admin
        data = self.restrict1.getJsonData()
        valid = Validator_products(data)
        valid.validate_missing_data()
        valid.validate_data_types()
        valid.validate_negations()
        data2 = valid.strip_spaces()
        valid.validate_duplication(data2)
        product1 = Product_Model(data2)
        product1.save()
        return make_response(jsonify({
            "Message": "Successfully added",
            "Products": product1.get()
        }), 201)

    @Token.token_required
    def get(current_user, self):
        '''Get all products endpoint that fetches all products
        and outputs them to the user'''
        if not current_user:
            return self.must_login
        products = self.product.get()
        if len(products) > 0:
            response = make_response(jsonify({
                "products": products
            }), 200)
        else:
            response = self.no_products

        return response


class OneProduct(Resource):
    def __init__(self):
        self.restrict1 = Restrictions()
        self.only_admin = self.restrict1.only_admin
        self.must_login = self.restrict1.must_login
        self.no_products = self.restrict1.no_products
        self.product = Product_Model()

    @Token.token_required
    def get(current_user, self, productId):
        '''Gets one product using its product id'''
        if not current_user:
            return self.must_login
        products = self.product.get()
        if len(products) == 0:
            return self.no_products
        for product in products:
            if int(productId) == product["id"]:
                return make_response(jsonify({
                    "Message": "Success",
                    "Product": product
                }), 200)
        return self.no_products

    @Token.token_required
    def put(current_user, self, productId):
        '''Updates a product details'''
        if current_user and not current_user["admin"]:
            return self.only_admin
        data = self.restrict1.getJsonData()
        product = Product_Model(data)
        products = product.get()
        found = [prod for prod in products if prod["id"] == int(productId)]
        if not found:
            return self.no_products
        elif len(products) == 0:
            return self.no_products
        valid = Validator_products(data)
        valid.validate_missing_data()
        valid.validate_data_types()
        valid.validate_negations()
        data2 = valid.strip_spaces()
        product = Product_Model(data2)
        product.update(productId)
        prods = Product_Model()
        producs = prods.get()
        for prod in producs:
            if prod['id'] == productId:
                return make_response(jsonify({
                    "Message": "Successfully updated",
                    "Products": prod
                }), 200)

    @Token.token_required
    def delete(current_user, self, productId):
        '''deletes product'''
        products = self.product.get()
        if not current_user["admin"]:
            return self.only_admin
        for item in products:
            if productId == item["id"]:
                self.product.delete(productId)
                return make_response(jsonify({
                    "message": "Deleted successfully"}), 200)
        return self.no_products
