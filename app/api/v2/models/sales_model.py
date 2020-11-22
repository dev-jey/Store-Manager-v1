from .main_model import InitializeConnection
from itertools import groupby


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
            """INSERT INTO sales(user_id, cart_id, product_id, quantity, subtotals,
             date) VALUES(%s,%s,%s,%s,%s,%s)""",
            (self.user_id,self.cart_id, self.product_id, self.quantity,
             self.subtotals, self.date,))
    
    def get(self, admin, current_user):
        total = 0
        if admin:
            self.cursor.execute("SELECT * FROM sales")
        if not admin:
            self.cursor.execute("""SELECT * FROM sales WHERE user_id=%s""",
            (current_user,))
        sales = self.cursor.fetchall()
        cart_items = []
        for item in sales:
            list_of_items= list(item)
            oneitem = {}
            oneitem["id"] = list_of_items[0]
            self.cursor.execute("""SELECT email FROM users WHERE id=%s""",
            (current_user,))
            user_details = self.cursor.fetchone()
            oneitem["attendant_email"] = user_details[0]
            oneitem["cart_id"] = list_of_items[2]
            self.cursor.execute("""SELECT title, price, description FROM products WHERE id=%s""",
            (list_of_items[3],))
            product_details = self.cursor.fetchone()
            oneitem["product_title"] = product_details[0]
            oneitem["product_price"] = product_details[1]
            oneitem["product_description"] = product_details[2]
            oneitem["quantity"] = list_of_items[4]
            oneitem["subtotals"] = list_of_items[5]
            oneitem["date"] = list_of_items[6]
            total = total + list_of_items[5]
            cart_items.append(oneitem)
            res = [list(v) for l,v in groupby(sorted(cart_items, key=lambda x:x['cart_id']), lambda x: x['cart_id'])]
        return res, total
    
    def delete(self):
        self.cursor.execute(
            "DELETE * from sales"
        )
    
    def delete_one(self, itemId):
        self.cursor.execute(
            "DELETE from sales where id = %s",
            (itemId,)
        )


    @staticmethod
    def checkSales(admin, user):
        sale1 = Sale_Model()
        sales = sale1.get(admin, user)
        return len(sales)
