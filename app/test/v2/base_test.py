import unittest
import json

from app import create_app
from instance.config import Config
from app.api.v2.models.db_models import Db


class TestsForApi(unittest.TestCase):
    '''Set up method to create an attendant, admin, product,
    and a sales table for use in other tests and authentication'''
    def setUp(self):
        self.db = Db()
        self.db.createTables()
        self.app = create_app(config_name=Config.APP_SETTINGS)
        self.test_client = self.app.test_client()
        self.admin_info = json.dumps({
            "email": "maria@gmail.com",
            "password": "as@dsDdz2a",
            "role": "Admin"
        })
        self.admin_login_details = json.dumps({
            "email": "maria@gmail.com",
            "password": "as@dsDdz2a"
        })
        signup_admin = self.test_client.post("/api/v2/auth/signup",
                                             data=self.admin_info,
                                             headers={
                                                 'content-type': 'application/json'
                                             })
        admin_login = self.test_client.post("/api/v2/auth/login",
                                            data=self.admin_login_details,
                                            headers={
                                                'content-type': 'application/json'
                                            })
        self.admin_token = json.loads(admin_login.data.decode())["token"]
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        '''Method to clear all tables
        before another test is undertaken'''
        self.db.destroy_tables()
        self.context.pop()