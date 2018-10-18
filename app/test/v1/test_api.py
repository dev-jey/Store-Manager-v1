import unittest
import json

from app import create_app
from instance.config import app_config


class TestsForApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.test_client = self.app.test_client()
        self.admin_info = json.dumps({
                        "id": 1,
                        "email": "maria@gmail.com",
                        "password": "as@dsDdz2a",
                        "role": "Admin"
                        })

        signup_admin = self.test_client.post("/api/v1/auth/signup",
                                             data=self.admin_info,
                                             headers={
                                              'content-type': 'application/json'
                                             })
        self.attendant = json.dumps({
                        "id": 2,
                        "email": "james@gmail.com",
                        "password": "as@dsDdz2a",
                        "role": "Attendant"
                        })
        
        signup_attendant = self.test_client.post("/api/v1/auth/signup",
                                                 data=self.attendant,
                                                 headers={
                                                  'content-type': 'application/json'
                                                 })

        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        self.context.pop()

    def test_successful_signup(self):
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

    def test_wrong_email_signup(self):
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
