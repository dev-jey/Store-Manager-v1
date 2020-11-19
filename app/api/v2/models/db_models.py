import psycopg2
import os
import datetime
from werkzeug.security import generate_password_hash
from sys import modules


class Db(object):
    def __init__(self):
        self.conn = None

    def createConnection(self):
        try:
            if 'pytest' in modules:
                URL = os.getenv("TEST_DB_URL")
            if os.getenv("APP_SETTINGS") == "development":
                URL = os.getenv("DB_URL")
            self.conn = psycopg2.connect(database=URL)
        except Exception:
            try:
                if os.getenv("APP_SETTINGS") == "production":
                    self.conn = psycopg2.connect(os.environ['DATABASE_URL'],
                                                 sslmode='require')
            except Exception:
                return "Connection Failed"
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
                admin BOOLEAN NOT NULL,
                date varchar(255) NOT NULL
                )
            """,

            """
            CREATE TABLE IF NOT EXISTS categories(
                id serial PRIMARY KEY,
                title varchar(255) NOT NULL UNIQUE,
                date varchar(255) NOT NULL
                )
            """,

            """CREATE TABLE IF NOT EXISTS products(
                id serial PRIMARY KEY,
                 title varchar(255) NOT NULL UNIQUE,
                  category_id int REFERENCES categories(id) ON 
                  UPDATE CASCADE ON DELETE CASCADE,
                  price float(45) NOT NULL,
                  quantity int NOT NULL,
                  minimum_stock int NOT NULL,
                  description varchar(255) NOT NULL,
                  date varchar(255) NOT NULL)
                  """,

            """
            CREATE TABLE IF NOT EXISTS cart(
                id serial PRIMARY KEY,
                user_id int REFERENCES users(id) NOT NULL,
                product_id int REFERENCES products(id) ON UPDATE
                 CASCADE ON DELETE CASCADE,
                quantity int NOT NULL,
                subtotals int NOT NULL,
                date varchar(255) NOT NULL)
            """,
            """
            CREATE TABLE IF NOT EXISTS sales(
                id serial PRIMARY KEY,
                user_id int REFERENCES users(id) NOT NULL,
                cart_id int REFERENCES cart(id) NOT NULL,
                product_id int REFERENCES products(id) ON DELETE CASCADE,
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
        password = str(generate_password_hash(os.environ.get('PASSWORD'), method='sha256'))
        email = os.environ.get('EMAIL')
        for table in tables:
            cursor.execute(table)
        try:
            cursor.execute(
                """INSERT INTO users (email, password, admin, date) 
                    VALUES(%s,%s ,%s, %s);""",
                (email, password, True, datetime.datetime.now())
            )
        except Exception:
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
