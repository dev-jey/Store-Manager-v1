import unittest
import json

from app import create_app
from instance.config import app_config
from app.api.v1.models import destroy


class TestsForApi(unittest.TestCase):
    '''Set up method to create an attendant, admin, product,
    and a sale for use in other tests and authentication'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.test_client = self.app.test_client()
        self.admin_info = json.dumps({
                        "id": 1,
                        "email": "maria@gmail.com",
                        "password": "as@dsDdz2a",
                        "role": "Admin"
                        })
        self.admin_login_details = json.dumps({
            "email": "maria@gmail.com",
            "password": "as@dsDdz2a"
            })
        signup_admin = self.test_client.post("/api/v1/auth/signup",
                                             data=self.admin_info,
                                             headers={
                                              'content-type': 'application/json'
                                             })
        admin_login = self.test_client.post("/api/v1/auth/login",
                                            data=self.admin_login_details,
                                            headers={
                                             'content-type': 'application/json'
                                            })
        self.admin_token = json.loads(admin_login.data.decode())["token"]
        self.attendant = json.dumps({
                        "id": 2,
                        "email": "james@gmail.com",
                        "password": "as@dsDdz2a",
                        "role": "Attendant"
                        })
        self.attendant_login_details = json.dumps({
                                                 "email": "james@gmail.com",
                                                 "password": "as@dsDdz2a"
                                                 })
        signup_attendant = self.test_client.post("/api/v1/auth/signup",
                                                 data=self.attendant,
                                                 headers={
                                                  'content-type': 'application/json'
                                                 })

        login_attendant = self.test_client.post("/api/v1/auth/login",
                                                data=self.attendant_login_details,
                                                headers={
                                                 'content-type': 'application/json'
                                                })
        self.data = json.loads(login_attendant.data.decode())
        self.attendant_token = self.data["token"]
        self.product = json.dumps(
            {
                "title": "infinix",
                "category": "phones",
                "price": 3000,
                "quantity": 10,
                "minimum_stock": 5,
                "description": "great smartphone to have"
            })
        self.sale = json.dumps({
            "productId": 1
        })
        self.test_client.post("/api/v1/products", data=self.product,
                              headers={
                                    'content-type': 'application/json',
                                    'x-access-token': self.admin_token
                                      })
        self.test_client.post("/api/v1/sales", data=self.sale,
                              headers={
                                        'content-type': 'application/json',
                                        'x-access-token': self.attendant_token
                                        })
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        '''Method to clear all dictionaries and
        lists before another test is undertaken'''
        destroy()
        self.context.pop()

    def test_for_empty_product_registration(self):
        '''Tests for an empty product registration'''
        resp = self.test_client.post("/api/v1/products",
                                     data=json.dumps({
                                        "title": "",
                                        "category": "",
                                        "price": 3000,
                                        "quantity": 10,
                                        "minimum_stock": 5,
                                        "description": "great products to have"
                                            }),
                                     headers={
                                        'content-type': 'application/json',
                                        'x-access-token': self.admin_token
                                        })
        self.assertEqual(resp.status_code, 400)

    def test_product_description_less_than_20_chars(self):
        '''Test for short product descriptions'''
        resp = self.test_client.post("/api/v1/products",
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
        self.assertEqual(resp.status_code, 400)

    def test_for_successful_product_registration(self):
        '''Tests for a successful product registration'''
        resp = self.test_client.post("/api/v1/products",
                                     data=self.product,
                                     headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 201)

    def test_for_token_authentication(self):
        '''Test for the functionality of token based authentication'''
        resp = self.test_client.post("/api/v1/products",
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
        self.assertEqual(resp.status_code, 401)

    def test_getting_all_products(self):
        '''Test for getting all products'''
        resp = self.test_client.get("/api/v1/products",
                                    headers={
                                            'x-access-token': self.admin_token
                                            })
        self.assertEqual(resp.status_code, 200)

    def test_post_sale_attendant(self):
        '''Test for posting a sale'''
        resp = self.test_client.post("/api/v1/sales",
                                     data=json.dumps({"productId": 1}),
                                     headers={
                                        'x-access-token': self.attendant_token,
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 201)

    def test_post_sale_admin(self):
        '''Test for administrator posting a sale'''
        resp = self.test_client.post("/api/v1/sales",
                                     data=json.dumps({"productId": 1}),
                                     headers={
                                            'x-access-token': self.admin_token,
                                            'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 401)

    def test_get_all_sales_admin(self):
        '''Test for admin getting all sales'''
        resp = self.test_client.get("/api/v1/sales",
                                    headers={
                                            'x-access-token': self.admin_token
                                            })
        self.assertEqual(resp.status_code, 200)

    def test_get_all_sales_attendant(self):
        '''Test for attendant getting all sales'''
        resp = self.test_client.get("/api/v1/sales",
                                    headers={
                                        'x-access-token': self.attendant_token
                                            })
        self.assertEqual(resp.status_code, 401)

    def test_getting_one_product(self):
        '''Test for getting one product'''
        resp = self.test_client.get("/api/v1/products/1",
                                    headers={
                                        'x-access-token': self.attendant_token
                                            })
        self.assertEqual(resp.status_code, 200)

    def test_getting_one_product_using_wrong_productId(self):
        '''Test for getting one product using wrong id'''
        resp = self.test_client.get("/api/v1/products/5",
                                    headers={
                                        'x-access-token': self.attendant_token
                                            })
        self.assertEqual(resp.status_code, 404)

    def test_getting_one_sale_admin(self):
        '''Test for getting one sale for an admin'''
        resp = self.test_client.get("/api/v1/sales/1",
                                    headers={
                                        'x-access-token': self.admin_token
                                            })
        self.assertEqual(resp.status_code, 200)

    def test_getting_one_sale_attendant(self):
        '''Test for getting one sale for an attendant'''
        resp = self.test_client.get("/api/v1/sales/1",
                                    headers={
                                        'x-access-token': self.attendant_token
                                            })
        self.assertEqual(resp.status_code, 200)

    def test_getting_one_sale_with_wrong_saleId(self):
        '''Test for getting one sale when a person enters wrong saleID'''
        resp = self.test_client.get("/api/v1/sales/4",
                                    headers={
                                        'x-access-token': self.attendant_token
                                            })
        self.assertEqual(resp.status_code, 404)

    def test_successful_signup(self):
        '''Tests for a successful signup'''
        data = json.dumps({
                           "email": "mary@gmail.com",
                           "password": "mardsd2@Qss",
                           "role": "Admin"
                           })
        res = self.test_client.post("/api/v1/auth/signup",
                                    data=data,
                                    headers={
                                            'content-type': 'application/json'
                                            })
        self.assertEqual(res.status_code, 201)

    def test_success_login(self):
        '''Test for successful login'''
        resp = self.test_client.post("/api/v1/auth/login",
                                     data=self.admin_login_details,
                                     headers={
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 200)

    def test_fail_login(self):
        '''Test for a failing login'''
        response = self.test_client.post("/api/v1/auth/login",
                                         data=json.dumps({
                                                        "email": "m@ew",
                                                        "password": "dxfdfd#eE"
                                                        }),
                                         headers={
                                            'content-type': 'application/json'
                                                })
        self.assertEqual(response.status_code, 403)

    def test_login_with_no_credentials_given(self):
        '''Test for a login with no credentials given'''
        resp = self.test_client.post("/api/v1/auth/login",
                                     headers={
                                             'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)

    def test_wrong_email_signup(self):
        '''Test for a signup with wrong email format given'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                                    "id": 5,
                                                    "email": "emailcom",
                                                    "password": "ssdsdD2@ja",
                                                    "role": "Admin"}),
                                     headers={
                                             'content-type': 'application/json'
                                             })
        self.assertEqual(resp.status_code, 400)

    def test_email_already_exists(self):
        '''Test for signing up with an already existing email'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                                    "id": 5,
                                                    "email": "maria@gmail.com",
                                                    "password": "ssdsdD2@ja",
                                                    "role": "Admin"
                                                    }),
                                     headers={
                                             'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 406)

    def test_signup_with_details_missing(self):
        '''Tests for signup with no details'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                                    "id": 5,
                                                    "email": "",
                                                    "password": "dsdE@sdD3",
                                                    "role": "Admin"
                                                    }),
                                     headers={
                                             'content-type': 'application/json'
                                             })
        self.assertEqual(resp.status_code, 400)

    def test_short_password(self):
        '''Test for a signup with a short password'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                                    "id": 5,
                                                    "email": "jame@gmail.com",
                                                    "password": "dS#e3",
                                                    "role": "Admin"
                                                    }),
                                     headers={
                                            'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)

    def test_long_password(self):
        '''Test for a signup with a long password'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                            "id": 5,
                                            "email": "jame@gmail.com",
                                            "password": "dhsdsdsdssdhjh3#dDd",
                                            "role": "Admin"}),
                                     headers={
                                             'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_digit(self):
        '''Test for signup witha password that lacks a numerical digit'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                        "id": 5,
                                        "email": "jame@gmail.com",
                                        "password": "ssrrdjD@",
                                        "role": "Admin"}),
                                     headers={
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_upperCase(self):
        '''Test for signup with a password with no uppercase character'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                        "id": 5,
                                        "email": "jame@gmail.com",
                                        "password": "dddsdsd2@",
                                        "role": "Admin"}),
                                     headers={
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_lowerCase(self):
        '''Test for signup with no lower case character'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                        "id": 5,
                                        "email": "jame@gmail.com",
                                        "password": "DHDHDDHD2@",
                                        "role": "Admin"}),
                                     headers={
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_specialChar(self):
        '''Test for signup with a password that lacks a special character'''
        resp = self.test_client.post("/api/v1/auth/signup",
                                     data=json.dumps({
                                        "id": 5,
                                        "email": "jame@gmail.com",
                                        "password": "ddddssd2D",
                                        "role": "Admin"}),
                                     headers={
                                        'content-type': 'application/json'
                                            })
        self.assertEqual(resp.status_code, 400)
