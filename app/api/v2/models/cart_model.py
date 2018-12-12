from .main_model import InitializeConnection


class Cart_Model(InitializeConnection):
    '''Initializes a sale'''

    def __init__(self, email=None, product=None,
                 quantity=None, subtotals=None):
        InitializeConnection.__init__(self)
        if email or product or quantity or subtotals:
            self.email = email
            self.title = product["title"]
            self.quantity = quantity
            self.subtotals = subtotals

    def save(self):
        '''Saves a sale to sale records'''
        self.cursor.execute(
            """INSERT INTO cart(email, title, quantity, subtotals,
             date) VALUES(%s,%s,%s,%s,%s)""",
            (self.email, self.title, self.quantity,
             self.subtotals, self.date),)

    def updateQuanitity(self, quantity, price, title):
        '''Method is meant to update an item in cart quantity by editing its details in the
        cart table'''
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT quantity,subtotals from cart WHERE title=%s", (title,))
        existing_item = self.cursor.fetchone()
        existing_quantity = int(existing_item[0])
        subtotal = int(existing_item[1])
        new_quantity = existing_quantity + quantity
        new_subtotal = subtotal + price
        self.cursor.execute(
            """UPDATE cart SET quantity = %s, subtotals=%s Where title = %s""", (
                new_quantity,new_subtotal, title,)
        )
    
    def add_or_reduce_quantity(self, quantity, price, title):
        '''Method is meant to update an item in cart quantity by editing its details in the
        cart table'''
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """UPDATE cart SET quantity = %s, subtotals=%s Where title = %s""", (
                quantity,price, title,)
        )


    def get(self):
        sql = "SELECT * FROM cart"
        self.cursor.execute(sql)
        cart = self.cursor.fetchall()
        allitems = []
        for item in cart:
            list_of_items= list(item)
            oneitem = {}
            oneitem["id"] = list_of_items[0]
            oneitem["email"] = list_of_items[1]
            oneitem["title"] = list_of_items[2]
            oneitem["quantity"] = list_of_items[3]
            oneitem["subtotals"] = list_of_items[4]
            oneitem["date"] = list_of_items[5]
            allitems.append(oneitem)

        return allitems

    def get_one_item_quantity(self, title):
        self.cursor.execute(
            """SELECT quantity FROM cart Where title = %s""", (
               title,)
        )
        cart_items = self.cursor.fetchone()
        new_quantity = int(cart_items[0])
        return new_quantity
    
    def get_one_item(self, title):
        self.cursor.execute(
            """SELECT * FROM cart Where title = %s""", (
               title,)
        )
        cart_items = self.cursor.fetchone()
        cart_item = []
        list_of_items= list(cart_items)
        oneitem = {}
        oneitem["id"] = list_of_items[0]
        oneitem["email"] = list_of_items[1]
        oneitem["title"] = list_of_items[2]
        oneitem["quantity"] = list_of_items[3]
        oneitem["subtotals"] = list_of_items[4]
        oneitem["date"] = list_of_items[5]
        cart_item.append(oneitem)
        return cart_item

    def delete(self):
        self.cursor.execute(
            "DELETE from cart"
        )
    
    def delete_one(self, itemId):
        self.cursor.execute(
            "DELETE from cart where id = %s",
            (itemId,)
        )


    @staticmethod
    def checkCart():
        cart1 = Cart_Model()
        cart = cart1.get()
        return len(cart)
