
from .base_test import *


class TestProducts(TestsForApi):
    def test_for_empty_product_registration(self):
        '''Tests for an empty product registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "",
                                         "category": "",
                                         "price": "",
                                         "quantity": "",
                                         "minimum_stock": "",
                                         "description": "great products to have"
                                     }),
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Wrong data types given")
        self.assertEqual(resp.status_code, 400)

    def test_for_empty_keys_product_registration(self):
        '''Tests for an empty product registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "": "infinix",
                                         "": "phones",
                                         "": 536,
                                         "": 5,
                                         "": 2,
                                         "": "great products to have"
                                     }),
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Must enter all product details")
        self.assertEqual(resp.status_code, 400)

    def test_validate_duplication(self):
        '''Test for duplicate product registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=self.product,
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Product already exists")
        self.assertEqual(resp.status_code, 400)

    def test_product_minimum_stock_more_than_quantity(self):
        '''Test for minimum stock more than quantity'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 1,
                                         "minimum_stock": 5,
                                         "description": "great"
                                     }),
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Minmum stock cant be more than quantity")
        self.assertEqual(resp.status_code, 400)

    def test_product_details_negative(self):
        '''Test for product price, quantity, and minimum stock negation'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix",
                                         "category": "phones",
                                         "price": -3000,
                                         "quantity": -1,
                                         "minimum_stock": -5,
                                         "description": "great"
                                     }),
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "Price, quantity or minmum stock cant be negative")
        self.assertEqual(resp.status_code, 400)

    def test_product_description_less_than_20_chars(self):
        '''Test for short product descriptions'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 10,
                                         "minimum_stock": 5,
                                         "description": "great"
                                     }),
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "Product description cant be less than 20 characters")
        self.assertEqual(resp.status_code, 400)

    def test_for_empty_product_entries(self):
        '''Test for empty/no product entries'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({}),
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Must enter all product details")
        self.assertEqual(resp.status_code, 400)

    def test_for_product_creation_data_types(self):
        '''Test for product creation using wrong data types'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": 1212,
                                         "category": 1212,
                                         "price": "ds",
                                         "quantity": "qw",
                                         "minimum_stock": 12,
                                         "description": 2232
                                     }),
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Wrong data types given")
        self.assertEqual(resp.status_code, 400)

    def test_if_price_is_converted_to_a_float(self):
        '''Test for product creation using wrong data types'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "Mandazi",
                                         "category": "food",
                                         "price": 12050,
                                         "quantity": 23,
                                         "minimum_stock": 2,
                                         "description": "Great product to possess at school"
                                     }),
                                     headers={
                                         'content-type': 'application/json',
                                         'x-access-token': self.admin_token
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Successfully added")
        self.assertEqual(resp.status_code, 201)

    def test_for_successful_product_registration(self):
        '''Tests for a successful product registration'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 10,
                                         "minimum_stock": 5,
                                         "description": "great products to have at hoome"
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Successfully added")
        self.assertEqual(resp.status_code, 201)

    def test_for_product_registration_attendant(self):
        '''Tests for a product registration by a sales attendant'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 10,
                                         "minimum_stock": 5,
                                         "description": "great products to have at hoome"
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "You must be an admin")
        self.assertEqual(resp.status_code, 403)

    def test_for_token_authentication(self):
        '''Test for the functionality of token based authentication'''
        resp = self.test_client.post("/api/v2/products",
                                     data=json.dumps({
                                         "title": "infinix",
                                         "category": "phones",
                                         "price": 3000,
                                         "quantity": 10,
                                         "minimum_stock": 5,
                                         "description": "great products to have at hoome"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Token Missing, Login to get one")
        self.assertEqual(resp.status_code, 401)
    
    def test_getting_all_products(self):
        '''Test for getting all products'''
        resp = self.test_client.get("/api/v2/products",
                                    headers={
                                        'x-access-token': self.admin_token
                                    })
        self.assertEqual(resp.status_code, 200)

