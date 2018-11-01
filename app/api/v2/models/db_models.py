import psycopg2
import os
from flask import jsonify
from werkzeug.security import generate_password_hash

from instance.config import Config


class Db(object):
    def __init__(self):
        self.db_name = Config.DB_NAME
        self.db_host = Config.DB_HOST
        self.db_user = Config.DB_USER
        self.db_password = Config.DB_PASSWORD
        self.conn = None

    def get_db_url(self):
        DB_URL = None
        if Config.APP_SETTINGS == "testing" or APP_SETTINGS == "testing":
            DB_URL = "host= {} user={} dbname={} password={}".format(
                self.db_host, self.db_user, "test_db", self.db_password)

        elif Config.APP_SETTINGS == "development":
            DB_URL = "host= {} user={} dbname={} password={}".format(
                self.db_host, self.db_user, self.db_name, self.db_password)
        else:
            DB_URL = os.environ['DATABASE_URL'], sslmode = 'require'

        return DB_URL

    def createConnection(self):
        '''Create connection to db'''
        db1 = Db()
        DB_URL = db1.get_db_url()
        try:
            self.conn = psycopg2.connect(DB_URL)
            self.conn.autocommit = True
            return self.conn
        except:
            return jsonify({"error": "failed to connect"})

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
                cursor.execute(
                    """INSERT INTO users (email, password, admin) 
                    VALUES('admin@gmail.com',%s ,%s) ON CONFLICT(email) DO NOTHING;""",
                    (password, True)
                )
        except Exception as e:
            print(e)
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
