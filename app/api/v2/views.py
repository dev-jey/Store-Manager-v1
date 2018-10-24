from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash

'''Local imports'''
from .utils import User_validator
from .models.user_model import User_Model


class SignUp(Resource):
    '''Signup endpont'''
    def post(self):
        '''Method to create a new user'''
        data = request.get_json()
        User_validator.validate_missing_data(self, data)
        User_validator.validate_data_types(self, data)
        email = data["email"]
        password = generate_password_hash(data["password"], method='sha256')
        role = data["role"]
        user = User_Model(email, password, role)
        User_validator.validate_credentials(self, data)
        user.save()
        return make_response(jsonify({
                                    "Message": "User registered",
                                    "Email": email,
                                    "Role": role
                                    }), 201)