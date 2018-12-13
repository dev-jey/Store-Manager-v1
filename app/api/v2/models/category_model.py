from .main_model import InitializeConnection


class Category_Model(InitializeConnection):
    '''Initializes a cart'''

    def __init__(self, data=None):
        InitializeConnection.__init__(self)
        if data:
            self.data = data

    def save(self):
        '''Saves a category to the table'''
        self.cursor.execute(
            """INSERT INTO categories(title,
                date) VALUES(%s,%s)""",
            (self.data["title"], self.date),)

    def get(self):
        '''Get all category elements'''
        sql = "SELECT * FROM categories"
        self.cursor.execute(sql)
        cart = self.cursor.fetchall()
        allitems = []
        for item in cart:
            list_of_items = list(item)
            oneitem = {}
            oneitem["id"] = list_of_items[0]
            oneitem["title"] = list_of_items[1]
            oneitem["date"] = list_of_items[2]
            allitems.append(oneitem)
        return allitems

    def get_one(self, itemId):
        self.cursor.execute(
            "SELECT * FROM categories WHERE id = %s",
            (itemId,))
        item = self.cursor.fetchone()
        allitems = []
        list_of_items = list(item)
        oneitem = {}
        oneitem["id"] = list_of_items[0]
        oneitem["title"] = list_of_items[1]
        oneitem["date"] = list_of_items[2]
        allitems.append(oneitem)
        return allitems

    def delete(self):
        '''Delete all categories'''
        self.cursor.execute(
            "DELETE from categories"
        )

    def update_one(self, itemId):
        '''update a category'''
        self.cursor.execute(
            "UPDATE categories SET title = %s WHERE id=%s",
            (self.data["title"].strip(), itemId)
        )

    def delete_one(self, itemId):
        '''Delete a single element from the categories'''
        self.cursor.execute(
            "DELETE from categories where id = %s",
            (itemId,)
        )
