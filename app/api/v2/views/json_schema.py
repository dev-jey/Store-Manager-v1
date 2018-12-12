'''All properties that I require for my application endpoints'''
PRODUCT_JSON = {
    'type': 'object',
    'maxProperties': 6,
    'properties': {
        'title': {'type': 'string'},
        'price': {'type': 'string'},
        'quantity': {'type': 'string'},
        'description': {'type': 'string'},
        'category': {'type': 'string'},
        'minimum_stock': {'type': 'string'},
    },
    'required': ['title', 'price', 'description',
                 'category', 'quantity', 'minimum_stock']
}
USER_JSON = {
    'type': 'object',
    'maxProperties': 3,
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'admin': {'type': 'string'}
    },
    'required': ['password', 'email', 'admin']
}
USER_LOGIN_JSON = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'email': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']
}
CART_JSON = {
    'type': 'object',
    'maxProperties': 2,
    'properties': {
        'title': {'type': 'string'},
        'quantity': {'type': 'string'}
    },
    'required': ['title', 'quantity']
}