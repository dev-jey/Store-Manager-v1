from .main_model import InitializeConnection


class Sale_Model(InitializeConnection):
    '''Initializes a sale'''

    def __init__(self, user_id=None, product_id=None, cart_id=None, 
                 quantity=None, subtotals=None):
        InitializeConnection.__init__(self)
        if user_id or product_id or quantity or subtotals or cart_id:
            self.user_id = user_id
            self.product_id = product_id
            self.cart_id = cart_id
            self.quantity = quantity
            self.subtotals = subtotals

    def save(self):
        '''Saves a sale to sale records'''
        self.cursor.execute(
            """INSERT INTO sales(user_id, product_id, quantity, subtotals,
             date) VALUES(%s,%s,%s,%s,%s)""",
            (self.email, self.title, self.quantity,
             self.subtotals, self.date),)
    
    def get(self):
        sql = "SELECT * FROM sales"
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
    
    def delete(self):
        self.cursor.execute(
            "DELETE from sales"
        )
    
    def delete_one(self, itemId):
        self.cursor.execute(
            "DELETE from sales where id = %s",
            (itemId,)
        )


    @staticmethod
    def checkSales():
        sale1 = Sale_Model()
        sales = sale1.get()
        return len(sales)
