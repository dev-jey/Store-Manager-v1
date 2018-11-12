from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
'''Local imports'''
from ..utils.product_validations import Validator_products
from ..models.product_models import Product_Model
from .token import Token


class Product(Resource):
    @Token.token_required
    def post(current_user, self):
        '''Post product endpoint that creates a new product'''
        if current_user and not current_user["admin"]:
            return make_response(jsonify({
                "Message": "You must be an admin"
            }), 403)
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide the product's details"
            }), 403)
        valid = Validator_products(data)
        valid.validate_missing_data()
        valid.validate_data_types()
        valid.validate_negations()
        data2 = valid.strip_spaces()
        valid.validate_duplication(data2)
        product = Product_Model(data2)
        product.save()
        return make_response(jsonify({
            "Message": "Successfully added",
            "Products": product.get()
        }), 201)

    @Token.token_required
    def get(current_user, self):
        '''Get all products endpoint that fetches all products
        and outputs them to the user'''
        if current_user:
            product = Product_Model()
            products = product.get()
            if len(products) > 0:
                response = make_response(jsonify({
                    "products": products
                }), 200)
            else:
                response = make_response(jsonify({
                    "Message": "No products found"
                }), 404)
            return response
        else:
            return make_response(jsonify({
                "message": "Must be logged in"
            }), 401)


class OneProduct(Resource):
    @Token.token_required
    def get(current_user, self, productId):
        '''Gets one product using its product id'''
        product = Product_Model()
        products = product.get()
        if len(products) == 0:
            response = make_response(jsonify({
                "Message": "No products yet"
            }), 404)
        if current_user:
            for product in products:
                if int(productId) == product["id"]:
                    return make_response(jsonify({
                        "Message": "Success",
                        "Product": product
                    }), 200)
        return make_response(jsonify({
            "Message": "Product non-existent"
        }), 404)

    @Token.token_required
    def put(current_user, self, productId):
        '''Updates a product details'''
        if current_user and not current_user["admin"]:
            return make_response(jsonify({
                "Message": "You must be an admin"
            }), 403)
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide the product's details"
            }), 403)
        product = Product_Model(data)
        products = product.get()
        found = [prod for prod in products if prod["id"] == int(productId)]
        if not found:
            return make_response(jsonify({
                "Message": "Product non-existent"
            }), 404)

        if len(products) == 0:
            return make_response(jsonify({
                "Message": "No products yet"
            }), 404)
        valid = Validator_products(data)
        valid.validate_missing_data()
        valid.validate_data_types()
        valid.validate_negations()
        data2 = valid.strip_spaces()
        product = Product_Model(data2)
        product.update(productId)
        prods = Product_Model().get()
        for prod in prods:
            if prod['id'] == productId:
                return make_response(jsonify({
                    "Message": "Successfully updated",
                    "Products": prod
                }), 200)

    @Token.token_required
    def delete(current_user, self, productId):
        '''deletes product'''
        product = Product_Model()
        products = product.get()
        if current_user["admin"]:
            for item in products:
                if productId == item["id"]:
                    product.delete(productId)
                    response = make_response(jsonify({
                        "message": "Deleted successfully"}), 200)
                    return response
        response = make_response(jsonify(
            {"Message": "Attempting to delete a product that doesn't exist"}), 404)
        return response
