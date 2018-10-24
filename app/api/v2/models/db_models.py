import psycopg2
import os
from flask import jsonify

from instance.config import Config


class Db(object):
    def __init__(self):
        self.db_name = Config.DB_NAME
        self.db_host = Config.DB_HOST
        self.db_user = Config.DB_USER
        self.db_password = Config.DB_PASSWORD
        self.conn = None

    def createConnection(self):
        try:
            if Config.APP_SETTINGS == "testing":
                self.conn = psycopg2.connect(database="test_db")
            else:
                self.conn = psycopg2.connect(
                    database=self.db_name, host=self.db_host, password=self.db_password)
            return self.conn
        except:
            return jsonify({"error": "failed to connect"})

    def createTables(self):
        cursor = self.createConnection().cursor()
        tables = [
            """CREATE TABLE IF NOT EXISTS users(
                id int NOT NULL PRIMARY KEY serial,
                email varchar(255) NOT NULL,
                password varchar(255) NOT NULL,
                role varchar(10) NOT NULL
                )
            """,

            """CREATE TABLE IF NOT EXISTS products(
                id int NOT NULL PRIMARY KEY serial,
                 title varchar(10) NOT NULL,
                  price float(50) NOT NULL,
                  quantity int NOT NULL,
                  minimum_stock varchar(10) NOT NULL,
                  description varchar(20) NOT NULL)
                  """,

            """
            CREATE TABLE IF NOT EXISTS sales(
                id int NOT NULL PRIMARY KEY serial,
                userId int REFERENCES users(id) NOT NULL,
                productId int REFERENCES products(id))
            """
        ]
        try:
            for table in tables:
                cursor.execute(table)
        except Exception as e:
            print(e)
            return "error"
        self.conn.commit()
        self.conn.close()

    def destroy_tables(self):
        cursor = self.createConnection().cursor()
        sql = [" DROP TABLE IF EXISTS users CASCADE",
               " DROP TABLE IF EXISTS products CASCADE",
               " DROP TABLE IF EXISTS sales CASCADE"
               ]
        for string in sql:
            cursor.execute(string)
        self.conn.commit()
        self.conn.close()
