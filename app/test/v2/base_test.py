import unittest
import json
from app import create_app

from instance.config import Config
from app.api.v2.models.db_models import Db
from app.api.v2.models.user_model import User_Model


class TestsForApi(unittest.TestCase):
    '''Set up method to create an attendant, admin, product,
    and a sales table for use in other tests and authentication'''

    def setUp(self):
        self.db = Db()
        self.db.createConnection()
        self.db.createTables()
        self.app = create_app(config_name="testing")
        self.test_client = self.app.test_client()
        self.admin_login_details = json.dumps({
            "email": "admin@gmail.com",
            "password": "admin"
        })
        admin_login = self.test_client.post("/api/v2/auth/login",
                                            data=self.admin_login_details,
                                            headers={
                                                'content-type': 'application/json'
                                            })
        self.admin_token = json.loads(admin_login.data.decode())["token"]
        self.attendant = json.dumps({
            "email": "james2@gmail.com",
            "password": "as@dsDdz2a",
            "admin": "false"
        })
        self.attendant_login_details = json.dumps({
            "email": "james2@gmail.com",
            "password": "as@dsDdz2a"
        })

        signup_attendant = self.test_client.post("/api/v2/auth/signup",
                                                 data=self.attendant,
                                                 headers={
                                                     'x-access-token': self.admin_token,
                                                     'content-type': 'application/json'
                                                 })
        login_attendant = self.test_client.post("/api/v2/auth/login",
                                                data=self.attendant_login_details,
                                                headers={
                                                    'content-type': 'application/json'
                                                })
        self.data = json.loads(login_attendant.data.decode())
        self.attendant_token = self.data["token"]
        self.product = json.dumps(
            {
                "title": "tecno",
                "category": "phones",
                "price": 3000,
                "quantity": 100,
                "minimum_stock": 5,
                "description": "great smartphone to have"
            })
        self.sale = json.dumps({
            "title": "tecno",
            "quantity": 10
        })
        self.test_client.post("/api/v2/products", data=self.product,
                              headers={
                                  'content-type': 'application/json',
                                  'x-access-token': self.admin_token
                              })
        self.test_client.post("/api/v2/sales", data=self.sale,
                                  headers={
                                      'content-type': 'application/json',
                                      'x-access-token': self.attendant_token
                                  })
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        '''Method to clear all tables
        before another test is undertaken'''
        self.db.destroy_tables()
        self.db.closeConnection()
        self.context.pop()
