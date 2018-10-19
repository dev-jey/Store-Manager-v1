'''Creation of all data structures and CRUD manipulation functions'''
users = []
products = []
sales = []


class User_Model():
    '''Initializes a new user object'''
    def __init__(self, email, password, role):
        self.id = len(users) + 1
        self.email = email
        self.password = password
        self.role = role

    def save(self):
        '''Saves a user by appending to the users list'''
        new_user = {
                "id": self.id,
                "email": self.email,
                "password": self.password,
                "role": self.role
            }
        users.append(new_user)
    
    def getEmail(self):
        return self.email


class Product_Model():
    '''Inittializes a new product'''
    def __init__(self, data):
        self.id = len(products) + 1
        self.product = data

    def save(self):
        '''Method to save a product by appending it to existing
        products list'''
        new_product = {
            "productId": self.id,
            "title": self.product["title"],
            "category": self.product["category"],
            "price": self.product["price"],
            "quantity": self.product["quantity"],
            "minimum_stock": self.product["minimum_stock"],
            "description": self.product["description"]
        }
        products.append(new_product)


def destroy():
    '''Destroys all the data in the data structures duting teardown
    in testing'''
    users.clear()
    products.clear()
    sales.clear()
