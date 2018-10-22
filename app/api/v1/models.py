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
    def __init__(self, title, category, price, quantity, minimum_stock,
                 description):
        self.id = len(products) + 1
        self.title = title
        self.category = category
        self.price = price
        self.quantity = quantity
        self.minimum_stock = minimum_stock
        self.description = description

    def save(self):
        new_product = {
            "productId": self.id,
            "title": self.title,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "minimum_stock": self.minimum_stock,
            "description": self.description
        }
        products.append(new_product)


def destroy():
    users.clear()
    products.clear()
    sales.clear()
