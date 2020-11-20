from .main_model import InitializeConnection


class Cart_Model(InitializeConnection):
    '''Initializes a cart'''

    def __init__(self, user_id=None, product=None,
                 quantity=None, subtotals=None):
        InitializeConnection.__init__(self)
        if user_id or product or quantity or subtotals:
            self.user_id = user_id
            self.product_id = product["id"]
            self.quantity = quantity
            self.subtotals = subtotals

    def save(self):
        '''Saves a cart item to the table'''
        self.cursor.execute(
            """INSERT INTO cart(user_id, product_id, quantity, subtotals,
             date) VALUES(%s,%s,%s,%s,%s)""",
            (self.user_id, self.product_id, self.quantity,
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
    
    def add_or_reduce_quantity(self, quantity, price, product_id):
        '''Method is meant to update an item in cart quantity by editing its details in the
        cart table'''
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """UPDATE cart SET quantity = %s, subtotals=%s Where product_id = %s""", (
                quantity,price, product_id,)
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
            oneitem["user_id"] = list_of_items[1]
            
            self.cursor.execute(
                "SELECT * FROM products WHERE id =%s",
                (list_of_items[2],)
            )
            product_details = self.cursor.fetchone()

            oneitem["product"] = {
                "id": product_details[0],
                "title": product_details[1],
                "price":product_details[3],
                "quantity":product_details[4]
            }
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
    
    def get_one_item(self, product_id):
        '''Get one cart item from the table'''
        self.cursor.execute(
            """SELECT * FROM cart Where product_id = %s""", (
               product_id,)
        )
        cart_items = self.cursor.fetchone()
        cart_item = []

        oneitem = {}
        list_of_items= list(cart_items)
        oneitem["user_id"] = list_of_items[1]
            
        self.cursor.execute(
            "SELECT * FROM products WHERE id =%s",
            (cart_items[2],)
        )
        product_details = self.cursor.fetchone()

        oneitem["product"] = {
            "id": product_details[0],
            "title": product_details[1],
            "price":product_details[3],
            "quantity":product_details[4]
        }
        oneitem["id"] = list_of_items[0]
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
