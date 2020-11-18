from flask import jsonify, make_response
from flask_restful import Resource
from flask_expects_json import expects_json

from ..utils.cart_validations import Validator_cart
from ..models.cart_model import Cart_Model
from .token import Token
from .main import Initialize
from .json_schema import CART_JSON


class Cart(Resource, Initialize):

    @expects_json(CART_JSON)
    @Token.token_required
    def post(current_user, self):
        '''Create an endpoint for attendants to add items to cart'''
        data = self.restrict1.getJsonData()
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAttendantStatus(current_user)
        valid = Validator_cart(data)
        valid.validate_data_types()
        id_ = data["id"].strip().lower()
        products = self.product.get()
        for product in products:
            if str(product["id"]) == id_:
                price = int(product["price"]) * data["quantity"]
                email = current_user["email"]
                cart_obj = Cart_Model(
                    email, product, data["quantity"], price)
                cart = self.cart_obj.get()
                for itm in cart:
                    if str(itm["id"]) == id_:
                        remaining_quantity = product["quantity"] - \
                            itm["quantity"]
                        self.restrict1.restrictCart(
                            data, remaining_quantity, price)
                        self.cart_obj.updateQuanitity(
                            data["quantity"], price, id_)
                        new_quantity = self.cart_obj.get_one_item_quantity(
                            id_)
                        remaining_quantity_new = product["quantity"] - \
                            new_quantity
                        return make_response(jsonify({
                            "message": "Added",
                            "Title": product["title"],
                            "quantity": product["quantity"],
                            "Available stock": remaining_quantity_new,
                            "Price": product["price"]
                        }), 201)
                self.restrict1.restrictCart(data, product["quantity"], price)
                cart_obj.save()
                if product["quantity"] < int(product["minimum_stock"]):
                    response = make_response(jsonify({
                        "Message": "Minimum stock reached",
                        "Title": product["title"],
                        "quantity": product["quantity"],
                        "Available stock": product["quantity"]-data["quantity"],
                        "Price": product["price"]
                    }), 201)
                else:
                    response = make_response(jsonify({
                        "message": "Added",
                        "Title": product["title"],
                        "quantity": product["quantity"],
                        "Available stock": product["quantity"]-data["quantity"],
                        "Price": product["price"]
                    }), 201)
                return response
        return self.no_products

    @Token.token_required
    def get(current_user, self):
        '''Method for getting all items in cart'''
        self.restrict1.checkUserStatus(current_user)
        cart = self.cart_obj.get()
        total = 0
        for item in cart:
            total = total + item["subtotals"]
        len_cart = self.cart_obj.checkCart()
        if len_cart:
            response = make_response(jsonify({
                "Message": "Success",
                "Cart": cart,
                "Total": total
            }), 200)
        else:
            response = self.no_items
        return response

    @Token.token_required
    def delete(current_user, self):
        '''Method for deleting all items in cart'''
        self.restrict1.checkUserStatus(current_user)
        self.cart_obj.delete()
        return make_response(jsonify({"message": "cart empty"}))


class OneItem(Resource, Initialize):
    @Token.token_required
    def get(current_user, self, itemId):
        '''Gets one item in cart using its item Id'''
        self.restrict1.checkUserStatus(current_user)
        cart = self.cart_obj.get()
        len_cart = self.cart_obj.checkCart()
        if not len_cart:
            return self.no_items
        for item in cart:
            if int(itemId) == item["id"]:
                self.restrict1.checkUser(current_user, item)
                return make_response(jsonify({
                    "Message": "Success",
                    "Cart": item
                }), 200)
        return self.no_items

    @Token.token_required
    def put(current_user, self, itemId):
        '''Method for updating a single item in cart'''
        self.restrict1.checkUserStatus(current_user)
        self.restrict1.checkAttendantStatus(current_user)
        data = self.restrict1.getJsonData()
        valid = Validator_cart(data)
        valid.validate_data_types()
        quantity = data["quantity"]
        cart = self.cart_obj.get()
        products = self.product.get()
        len_cart = self.cart_obj.checkCart()
        cart = self.cart_obj.get()
        if not len_cart:
            return self.no_items
        for itm in cart:
            if itm["id"] == itemId:
                self.restrict1.checkUser(current_user, itm)
                for product in products:
                    if product["title"] == itm["title"]:
                        remaining_quantity = product["quantity"] - \
                            itm["quantity"]
                        self.restrict1.restrictCart(
                            data, remaining_quantity, product["price"])
                        price = int(product["price"]) * data["quantity"]
                        self.cart_obj.add_or_reduce_quantity(
                            data["quantity"], price, itm["title"])
                        updated_item = self.cart_obj.get_one_item(
                            product["title"])
                        return make_response(jsonify({
                            "Message": "Quantity updated successfully",
                            "Cart": updated_item
                        }), 200)
        return self.no_items

    @Token.token_required
    def delete(current_user, self, itemId):
        '''Method for deleting a single item in cart'''
        self.restrict1.checkUserStatus(current_user)
        len_cart = self.cart_obj.checkCart()
        cart = self.cart_obj.get()
        if not len_cart:
            return self.no_items
        for item in cart:
            if int(itemId) == item["id"]:
                self.restrict1.checkUser(current_user, item)
                self.cart_obj.delete_one(itemId)
                return make_response(jsonify({
                    "Message": "Deleted successfully"
                }), 200)
        return self.no_items
