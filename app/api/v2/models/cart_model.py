from .main_model import InitializeConnection


class Cart_Model(InitializeConnection):
    '''Initializes a cart'''

    def __init__(self, email=None, product=None,
                 quantity=None, subtotals=None):
        InitializeConnection.__init__(self)
        if email or product or quantity or subtotals:
            self.email = email
            self.title = product["title"]
            self.quantity = quantity
            self.subtotals = subtotals

    def save(self):
        '''Saves a cart item to the table'''
        self.cursor.execute(
            """INSERT INTO cart(email, title, quantity, subtotals,
             date) VALUES(%s,%s,%s,%s,%s)""",
            (self.email, self.title, self.quantity,
             self.subtotals, self.date),)

    def updateQuanitity(self, quantity, price, _id):
        '''Method is meant to update an item in cart quantity by editing its details in the
        cart table'''
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT quantity,subtotals from cart WHERE id=%s", (_id,))
        existing_item = self.cursor.fetchone()
        existing_quantity = int(existing_item[0])
        subtotal = int(existing_item[1])
        new_quantity = existing_quantity + quantity
        new_subtotal = subtotal + price
        self.cursor.execute(
            """UPDATE cart SET quantity = %s, subtotals=%s Where id = %s""", (
                new_quantity,new_subtotal, _id,)
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
        '''Get all cart elements'''
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

    def get_one_item_quantity(self, _id):
        '''Get the quantity of one item in the cart'''
        self.cursor.execute(
            """SELECT quantity FROM cart Where id = %s""", (
               _id,)
        )
        cart_items = self.cursor.fetchone()
        new_quantity = int(cart_items[0])
        return new_quantity
    
    def get_one_item(self, title):
        '''Get one cart item from the table'''
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
        '''Empty cart'''
        self.cursor.execute(
            "DELETE from cart"
        )
    
    def delete_one(self, itemId):
        '''Delete a single element from the cart'''
        self.cursor.execute(
            "DELETE from cart where id = %s",
            (itemId,)
        )


    @staticmethod
    def checkCart():
        '''Check if the cart is empty'''
        cart1 = Cart_Model()
        cart = cart1.get()
        return len(cart)
