from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from instance.config import app_config
import jwt
import datetime
'''Local imports'''
from .utils import User_validator, Validator_products, Validator_sales
from .models.user_model import User_Model
from .models.product_models import Product_Model
from .models.sale_models import Sales_Model
from .models.db_models import Db


def token_required(fnc):
    '''Creates decorator to decode tokens and assign them to current users'''
    @wraps(fnc)
    def decorated(*args, **kwargs):
        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            db = Db()
            conn = db.createConnection()
            db.createTables()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM blacklist WHERE token = %s", (token,))
            if cursor.fetchone():
                return jsonify({"Message": "Token blacklisted, please login"})
        if not token:
            return make_response(jsonify({
                "message": "Token Missing, Login to get one"
            }), 401)
        try:
            data = jwt.decode(
                token, app_config["development"].SECRET_KEY, algorithms=['HS256'])
            model = User_Model()
            users = model.get()
            for user in users:
                if user["email"] == data["email"]:
                    current_user = user
        except Exception as e:
            return make_response(jsonify({"message": "token invalid"}),
                                 403)
        return fnc(current_user, *args, **kwargs)
    return decorated


class SignUp(Resource):
    '''Signup endpont'''
    @token_required
    def post(current_user, self):
        '''Method to create a new user'''
        if current_user and current_user["admin"]:
            try:
                data = request.get_json()
            except:
                return make_response(jsonify({
                    "Message": "Please, provide your credentials"
                }), 403)
            valid = User_validator(data)
            valid.validate_missing_keys_signup()
            valid.validate_data_types_signup()
            valid.validate_missing_data_signup()
            valid.validate_signup_password()
            user2 = valid.space_strip()
            valid.validate_user_exists(user2)
            email = data["email"].strip().lower()
            password = generate_password_hash(
                data["password"], method='sha256').strip()
            admin = data["admin"]
            if admin not in ["true", "t", "false", "f"]:
                return make_response(jsonify({
                    "message": "Admin can either be true/t or false/f"
                }))
            elif admin not in ["true", "t"]:
                admin = False
            user = User_Model(email, password, admin)
            user.save()
            return make_response(jsonify({
                "Message": "User registered",
                "Email": email,
                "Admin": admin
            }), 201)

        return make_response(jsonify({
            "Message": "Must be an admin to undertake this action"
        }), 201)


class Signout(Resource):
    @token_required
    def post(current_user, self):
        try:
            if current_user:
                if 'x-access-token' in request.headers:
                    token = request.headers["x-access-token"]
                    user_obj = User_Model()
                    date = datetime.datetime.now()
                    user_obj.logout(token, date)
                    return make_response(jsonify({
                        "Message": "Successfully logged out"
                    }), 200)
        except Exception as e:
            return make_response(jsonify({
                "Message": "Error while blacklisting token"
            }), 403)


class UpdateUser(Resource):
    @token_required
    def put(current_user, self, userId):
        '''Update user endpoint'''
        if current_user["admin"]:
            item = User_Model()
            users = item.get()
            for user in users:
                if user["id"] == userId:
                    if not user["admin"]:
                        item.update(userId)
                        response = make_response(jsonify({
                            "Message": "User updated to:",
                            "Role": "Admin"
                        }), 201)
                    else:
                        response = make_response(jsonify({
                            "message":  "User already an admin"
                        }), 403)
                    return response
            return make_response(jsonify({"message":  "User non-existent"}), 404)
        return make_response(jsonify({
            "Message": "Must be admin"
        }), 401)


class Login(Resource):
    '''Login endpoint'''

    def post(self):
        '''Method to login a user and create a unique JWT token'''
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide your credentials"
            }), 403)
        valid = User_validator(data)
        valid.validate_missing_data_login()
        valid.validate_data_types_login()
        valid.validate_empty_items_login()
        email = data["email"].strip()
        password = data["password"].strip()
        user2 = User_Model()
        users = user2.get()
        for user in users:
            if email == user["email"] and check_password_hash(user["password"],
                                                              password):
                token = jwt.encode({"email": email, "password": password,
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(minutes=30)},
                                   app_config["development"].SECRET_KEY, algorithm='HS256')
                return make_response(jsonify({
                    "message": "Login success",
                    "token": token.decode("UTF-8"
                                          )}), 200)
        return make_response(jsonify({
            "Message": "Login failed, check credentials"
        }), 403)


class Product(Resource):
    @token_required
    def post(current_user, self):
        '''Post product endpoint that creates a new product'''
        if current_user and not current_user["admin"]:
            return make_response(jsonify({
                "Message": "Must be an admin to undertake this action"
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
        products = product.get()
        for product in products:
            if product["title"] == data2["title"]:
                return make_response(jsonify({
                    "Message": "Successfully added",
                    "Products": product
                }), 201)

    @token_required
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
    @token_required
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

    @token_required
    def put(current_user, self, productId):
        '''Updates a product details'''
        if current_user and not current_user["admin"]:
            return make_response(jsonify({
                "Message": "Must be an admin to undertake this action"
            }), 403)
        try:
            data = request.get_json()
        except:
            return make_response(jsonify({
                "Message": "Please, provide the product's details"
            }), 403)
        product = Product_Model()
        products = product.get()

        if len(products) == 0:
            return make_response(jsonify({
                "Message": "No products yet"
            }), 404)
        for product in products:
            if product["id"] == int(productId):
                if "title" not in data:
                    data["title"] = product["title"]
                if "category" not in data:
                    data["category"] = product["category"]
                if "price" not in data:
                    data["price"] = product["price"]
                if "quantity" not in data:
                    data["quantity"] = product["quantity"]
                if "minimum_stock" not in data:
                    data["minimum_stock"] = product["minimum_stock"]
                if "description" not in data:
                    data["description"] = product["description"]
                valid = Validator_products(data)
                valid.validate_data_types()
                valid.validate_negations()
                data2 = valid.strip_spaces()
                product_obj = Product_Model()
                product_obj.update(productId, data2["title"], data2["category"], data2["price"],
                                                   data2["quantity"], data2["minimum_stock"], data2["description"])
                product1 = Product_Model()
                all_products = product1.get()
                for item in all_products:
                    if item["title"] == data2["title"]:
                        return make_response(jsonify({
                            "Message": "Successfully updated",
                            "Product": item
                        }), 200)
        return make_response(jsonify({
            "Message": "Product non-existent"
        }), 404)

    @token_required
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


class Sale(Resource):

    @token_required
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
                "Message": "Must be an admin to undertake this action"
            }), 401)

    @token_required
    def get(current_user, self):
        '''Method for getting all sales'''
        if current_user and current_user["admin"]:
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
                "Message": "Must be an admin to undertake this action"
            }), 401)


class OneSale(Resource):
    @token_required
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
