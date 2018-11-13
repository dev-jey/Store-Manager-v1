from flask import abort, make_response, jsonify, request


class Restrictions:
    def __init__(self):
        self.only_admin = make_response(jsonify({
            "Message": "You must be an admin"
        }), 403)

        self.only_attendant = make_response(jsonify({
            "Message": "Must be an attendant!"
        }), 401)

        self.must_login = make_response(jsonify({
            "message": "Must be logged in"
        }), 401)

        self.no_products = make_response(jsonify({
            "Message": "No product/products found"
        }), 404)

        self.no_sales = make_response(jsonify({
            "Message": "Failure, no sales made yet"
        }), 404)

        self.no_user = make_response(jsonify({
            "Message": "No user/users found"
        }), 404)

        self.access_denied = make_response(jsonify({
            "Message": "Access denied"
        }), 401)

        self.login_failed = make_response(jsonify({
            "Message": "Login failed, check credentials"
        }), 403)

    @staticmethod
    def getJsonData():
        return request.get_json()

    @staticmethod
    def restrictSales(data, product, price):
        response = None
        if data["quantity"] > product["quantity"] and product["quantity"] != 0:
            response = make_response(jsonify({
                "Message": "Attempting to sell more than there is in stock"
            }), 404)
        elif product["quantity"] > 0:
            product["quantity"] = product["quantity"] - \
                data["quantity"]
        else:
            response = make_response(jsonify({
                "Message": "Products sold up"
            }), 404)
        if response:
            abort(response)

    def checkUser(self, current_user, item):
        if not current_user["admin"] and not current_user["email"] == item["email"]:
            abort(self.access_denied)

    @staticmethod
    def checkAdmin(admin):
        response = None
        if admin not in ["true", "t", "false", "f"]:
            response = make_response(jsonify({
                "message": "Admin can either be true/t or false/f"
            }))
        elif admin not in ["true", "True", "T", "t"]:
            admin = False
        if response:
            abort(400, response)
