from flask import jsonify, request, make_response
from functools import wraps
from instance.config import app_config
import jwt

from ..models.user_model import User_Model
from ..models.db_models import Db


class Token:
    @staticmethod
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
                    token, app_config["development"].SECRET_KEY,
                    algorithms=['HS256'])
                model = User_Model()
                users = model.get()
                for user in users:
                    if user["email"] == data["email"]:
                        current_user = user
            except Exception:
                return make_response(jsonify({"message": "token invalid"}),
                                     403)
            return fnc(current_user, *args, **kwargs)
        return decorated
