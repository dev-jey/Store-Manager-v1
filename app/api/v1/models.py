users = []
products = []
sales = []


class User_Model():
    def __init__(self, email, password, role):
        self.id = len(users) + 1
        self.email = email
        self.password = password
        self.role = role

    def save(self):
        new_user = {
                "id": self.id,
                "email": self.email,
                "password": self.password,
                "role": self.role
            }
        users.append(new_user)


class Product_Model():
    def __init__(self, data):
        self.id = len(products) + 1
        self.product = data

    def save(self):
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
    users.clear()
    products.clear()
    sales.clear()
