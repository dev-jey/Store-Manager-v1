import psycopg2
import os
from flask import jsonify
from werkzeug.security import generate_password_hash

from instance.config import Config
from sys import modules


class Db(object):
    def __init__(self):
        self.conn = None

    def createConnection(self):
        try:
            if 'pytest' in modules:
                URL = os.getenv("TEST_DB_URL")
            elif os.getenv("APP_SETTINGS") == "development":
                URL = os.getenv("DB_URL")
            else:
                URL = os.environ['DATABASE_URL'], sslmode = 'require'
            self.conn = psycopg2.connect(database=URL)
        except Exception:
            pass
        self.conn.autocommit = True
        return self.conn

    def closeConnection(self):
        '''method to close connections'''
        return self.conn.close()

    def createTables(self):
        cursor = self.createConnection().cursor()
        tables = [
            """CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                email varchar(255) UNIQUE NOT NULL,
                password varchar(255) NOT NULL,
                admin BOOLEAN NOT NULL
                )
            """,

            """CREATE TABLE IF NOT EXISTS products(
                id serial PRIMARY KEY,
                 title varchar(255) NOT NULL UNIQUE,
                 category varchar NOT NULL,
                  price float(45) NOT NULL,
                  quantity int NOT NULL,
                  minimum_stock int NOT NULL,
                  description varchar(255) NOT NULL,
                  date varchar(255) NOT NULL)
                  """,

            """
            CREATE TABLE IF NOT EXISTS sales(
                id serial PRIMARY KEY,
                email varchar(255) REFERENCES users(email) NOT NULL,
                title varchar(255) REFERENCES products(title) ON UPDATE RESTRICT ON DELETE RESTRICT,
                quantity int NOT NULL,
                subtotals int NOT NULL,
                date varchar(255) NOT NULL)
            """,
            """
            CREATE TABLE IF NOT EXISTS blacklist(
                id serial PRIMARY KEY,
                token varchar(255) NOT NULL,
                date varchar(255) NOT NULL
                )
            """
        ]
        try:
            password = str(generate_password_hash("admin", method='sha256'))
            for table in tables:
                cursor.execute(table)
        except Exception:
            pass
        try:
            cursor.execute(
                    """INSERT INTO users (email, password, admin) 
                    VALUES('admin@gmail.com',%s ,%s);""",
                    (password, True)
                )
        except:
            pass
        self.conn.commit()
        self.conn.close()

    def destroy_tables(self):
        cursor = self.createConnection().cursor()
        cursor.execute(
            "SELECT table_schema,table_name FROM information_schema.tables "
            " WHERE table_schema = 'public' ORDER BY table_schema,table_name"
        )
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("drop table "+row[1] + " cascade")
        self.conn.commit()
        self.conn.close()
