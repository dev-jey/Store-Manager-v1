from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from instance.config import app_config
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import Validator
from .models import User_Model, users

class SignUp(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                                    "Message": "Kindly enter credentials"
                                    }), 400)
        email = data["email"]
        password = generate_password_hash(data["password"], method='sha256')
        role = data["role"]
        user = User_Model(email, password, role)
        Validator.validate_credentials(self, data)
        user.save()
        return make_response(jsonify({
                                    "Message": "Success",
                                    "users": users
                                    }), 201)

