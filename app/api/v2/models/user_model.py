import psycopg2
from flask import jsonify, make_response, abort
from werkzeug.security import generate_password_hash
from .db_models import Db


class User_Model(Db):

    '''Initializes a new user object'''

    def __init__(self, email=None, password=None, role=None):
        self.email = email
        self.password = password
        self.role = role
        db = Db()
        db.createTables()
        self.conn = db.createConnection()

    def save(self):
        cursor = self.conn.cursor()
        if self.role == "Admin":
            user = User_Model()
            users = user.get()
            for user in users:
                if user["role"] == "Admin" or user["role"] == "admin":
                    abort(401, "Admin already exists")
        cursor.execute(
            "INSERT INTO users(email,password,role) VALUES(%s,%s,%s)", (
                self.email, self.password, self.role,)
        )
        cursor.execute("SELECT id FROM users WHERE email = %s", (self.email,))
        row = cursor.fetchone()
        self.id = row[0]
        self.conn.commit()
        self.conn.close()

    def saveAdmin(self):
        cursor = self.conn.cursor()
        password = generate_password_hash('as@dsDdz2a', method='sha256')
        cursor.execute(
            "INSERT INTO users(email, password, role) VALUES('maria@gmail.com', %s, 'Admin')",
            (password,)
        )
        cursor.execute("SELECT role FROM users WHERE email = 'maria@gmail.com'")
        row = cursor.fetchone()
        self.id = row[0]
        self.conn.commit()
        self.conn.close()

    def get(self):
        db = Db()
        self.conn = db.createConnection()
        db.createTables()
        cursor = self.conn.cursor()
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        users = cursor.fetchall()
        allusers = []
        for user in users:
            list_of_items = list(user)
            oneuser = {}
            oneuser["id"] = list_of_items[0]
            oneuser["email"] = list_of_items[1]
            oneuser["password"] = list_of_items[2]
            oneuser["role"] = list_of_items[3]
            allusers.append(oneuser)
        cursor.close()
        self.conn.close()
        return allusers
