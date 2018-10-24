import psycopg2
from flask import jsonify
import datetime

from .db_models import Db


class Product_Model(Db):
    '''Inittializes a new product'''
    def __init__(self, data=None):
        self.data = data
        self.date = datetime.datetime.now()
        db = Db()
        db.createTables()
        self.conn = db.createConnection()

    def save(self):
        '''Method to save a product by appending it to existing
        products table'''
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO products(title,category,price,quantity,minimum_stock,description, date) VALUES(%s,%s,%s,%s,%s,%s,%s)" 
            , (self.data["title"], self.data["category"], self.data["price"], self.data["quantity"], 
            self.data["minimum_stock"], self.data["description"], self.date),
            )
        cursor.execute("SELECT id FROM products WHERE title = %s", (self.data["title"],))
        row = cursor.fetchone()
        self.id = row[0]
        self.conn.commit()
        self.conn.close()
    
    def update(self, productId):
        '''Method is meant to update a product by editing its details in the
        products table'''
        db = Db()
        self.conn = db.createConnection()
        db.createTables()
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE products SET title = %s, category = %s, 
            price = %s, quantity = %s, minimum_stock = %s, description = %s,
             date = %s""", (self.data["title"], self.data["category"], self.data["price"],
              self.data["quantity"], self.data["minimum_stock"], self.data["description"], self.date,))
        self.conn.commit()
        self.conn.close()

    def get(self):
        db = Db()
        self.conn = db.createConnection()
        db.createTables()
        cursor = self.conn.cursor()
        sql = "SELECT * FROM products"
        cursor.execute(sql)
        products = cursor.fetchall()
        allproducts = []
        for product in products:
            list_of_items = list(product)
            oneproduct = {}
            oneproduct["id"] = list_of_items[0]
            oneproduct["title"] = list_of_items[1]
            oneproduct["category"] = list_of_items[2]
            oneproduct["price"] = list_of_items[3]
            oneproduct["quantity"] = list_of_items[4]
            oneproduct["minimum_stock"] = list_of_items[5]
            oneproduct["description"] = list_of_items[6]
            allproducts.append(oneproduct)
        cursor.close()
        self.conn.close()
        return allproducts
