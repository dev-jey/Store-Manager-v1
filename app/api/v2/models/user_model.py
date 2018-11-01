import psycopg2
from flask import jsonify, make_response, abort
from werkzeug.security import generate_password_hash
from .db_models import Db


class User_Model(Db):

    '''Initializes a new user object'''

    def __init__(self, email=None, password=None, admin=False):
        self.email = email
        self.password = password
        self.admin = admin
        self.db = Db()
        self.conn = self.db.createConnection()
        self.db.createTables()
        self.cursor = self.conn.cursor()

    def save(self):
        self.cursor.execute(
            "INSERT INTO users(email,password,admin) VALUES(%s,%s,%s)", (
                self.email, self.password, self.admin,)
        )
        self.cursor.execute("SELECT id FROM users WHERE email = %s", (self.email,))
        row = self.cursor.fetchone()
        self.id = row[0]

    def get(self):
        sql = "SELECT * FROM users"
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        allusers = []
        for user in users:
            list_of_users = list(user)
            oneuser = {}
            oneuser["id"] = list_of_users[0]
            oneuser["email"] = list_of_users[1]
            oneuser["password"] = list_of_users[2]
            oneuser["admin"] = list_of_users[3]
            allusers.append(oneuser)
        return allusers

    def update(self, userId):
        self.cursor.execute(
            "UPDATE users SET admin = %s WHERE id = %s", (True, userId,)
        )
    
    def logout(self, token, date):
        '''method to logout a user from the system'''
        self.cursor.execute(
                "INSERT INTO blacklist (token, date) VALUES (%s,%s)",
                (token, date,)
        )
    
    def __repr__(self):
        return self.conn.close()
