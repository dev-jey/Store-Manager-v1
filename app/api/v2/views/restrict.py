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

        self.no_items = make_response(jsonify({
            "Message": "No item in cart"
        }), 404)

        self.no_sales = make_response(jsonify({
            "Message": "No sale/sales found"
        }), 404)

        self.no_user = make_response(jsonify({
            "Message": "No user/users found"
        }), 404)

        self.no_categories = make_response(jsonify({
            "Message": "No category/categories found"
        }), 404)

        self.access_denied = make_response(jsonify({
            "Message": "Access denied"
        }), 401)

        self.login_failed = make_response(jsonify({
            "Message": "Login failed, check credentials"
        }), 401)

    def checkUserStatus(self, current_user):
        if not current_user:
            abort(self.must_login)

    def checkAdminStatus(self, current_user):
        if not current_user["admin"]:
            abort(self.only_admin)

    def checkAttendantStatus(self, current_user):
        if current_user["admin"]:
            abort(self.only_attendant)

    @staticmethod
    def getJsonData():
        return request.get_json()

    @staticmethod
    def restrictCart(data, quantity, price, status):
        if data['quantity'] > quantity and status == 1:
            abort(make_response(jsonify({
                "Message": "You cannot add more than is in stock"
            }), 401))

    def checkUser(self, current_user, item):
        if not current_user["admin"] and not current_user["id"] == item["user_id"]:
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
