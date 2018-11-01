import psycopg2
from flask import jsonify, abort
import datetime

from .db_models import Db


class Product_Model(Db):
    '''Inittializes a new product'''

    def __init__(self, data=None):
        self.data = data
        self.date = datetime.datetime.now()
        self.db = Db()
        self.conn = self.db.createConnection()
        self.db.createTables()
        self.cursor = self.conn.cursor()

    def save(self):
        '''Method to save a product by appending it to existing
        products table'''
        self.cursor.execute(
            "INSERT INTO products(title,category,price,quantity,minimum_stock,description, date) VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (self.data["title"], self.data["category"], self.data["price"], self.data["quantity"],
             self.data["minimum_stock"], self.data["description"], self.date),
        )
        self.cursor.execute("SELECT id FROM products WHERE title = %s",
                            (self.data["title"],))
        row = self.cursor.fetchone()
        self.id = row[0]
        self.conn.commit()

    def update(self, productId):
        '''Method is meant to update a product by editing its details in the
        products table'''
        self.productId = productId
        self.cursor.execute("SELECT id FROM products WHERE title = %s",
                            (self.data["title"],))
        row = self.cursor.fetchone()
        if not row or row[0] == productId:
            self.cursor.execute(
                """UPDATE products SET title = %s, category = %s, 
                        price = %s, quantity = %s, minimum_stock = %s,
                         description = %s, date = %s WHERE id = %s""",
                (self.data["title"], self.data["category"], self.data["price"],
                 self.data["quantity"], self.data["minimum_stock"],
                 self.data["description"], self.date, self.productId),
            )
        else:
            abort(403, "Product title already exists, try another one")

        self.conn.commit()

    def get(self):
        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        products = self.cursor.fetchall()
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
        return allproducts

    def delete(self, productId):
        self.productId = productId
        self.cursor.execute(
            "DELETE from products where id = %s",
            (self.productId,)
        )
        self.conn.commit()

    def updateQuanitity(self, quantity, title):
        '''Method is meant to update a product by editing its details in the
        products table'''
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """UPDATE products SET quantity = %s Where title = %s""", (
                quantity, title,)
        )
        self.conn.commit()