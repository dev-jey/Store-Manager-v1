
from .base_test import *


class TestUsers(TestsForApi):

    def test_successful_signup(self):
        '''Tests for a successful signup'''
        data = json.dumps({
            "email": "marys@gmail.com",
            "password": "mardsd2@Qss",
                        "role": "Attendant"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["Message"], "User registered")
        self.assertEqual(res.status_code, 201)

    def test_wrong_email_signup(self):
        '''Test for a signup with wrong email format given'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "emailcom",
                                         "password": "ssdsdD2@ja",
                                         "role": "Admin"}),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Invalid email")
        self.assertEqual(resp.status_code, 400)

    def test_email_already_exists(self):
        '''Test for signing up with an already existing email'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "maria@gmail.com",
                                         "password": "ssdsdD2@ja",
                                         "role": "Admin"
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "maria@gmail.com",
                                         "password": "ssdsdD2@ja",
                                         "role": "Admin"
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "User already exists")
        self.assertEqual(resp.status_code, 406)

    def test_signup_with_details_missing(self):
        '''Tests for signup with no details'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "",
                                         "password": "dsdE@sdD3",
                                         "role": "Admin"
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Kindly enter your full credentials")
        self.assertEqual(resp.status_code, 400)

    def test_short_password(self):
        '''Test for a signup with a short password'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "jame@gmail.com",
                                         "password": "dS#e3",
                                         "role": "Admin"
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "Password must be long than 6 characters or less than 12")
        self.assertEqual(resp.status_code, 400)

    def test_long_password(self):
        '''Test for a signup with a long password'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "jame@gmail.com",
                                         "password": "dhsdsdsdssdhjh3#dDd",
                                         "role": "Admin"}),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "Password must be long than 6 characters or less than 12")
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_digit(self):
        '''Test for signup witha password that lacks a numerical digit'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "jame@gmail.com",
                                         "password": "ssrrdjD@",
                                         "role": "Admin"}),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Password must have a digit")
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_upperCase(self):
        '''Test for signup with a password with no uppercase character'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "jame@gmail.com",
                                         "password": "dddsdsd2@",
                                         "role": "Admin"}),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Password must have an upper case character")
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_lowerCase(self):
        '''Test for signup with no lower case character'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "jame@gmail.com",
                                         "password": "DHDHDDHD2@",
                                         "role": "Admin"}),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Password must have a lower case character")
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_specialChar(self):
        '''Test for signup with a password that lacks a special character'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "jame@gmail.com",
                                         "password": "ddddssd2D",
                                         "role": "Admin"}),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Password must have a special charater")
        self.assertEqual(resp.status_code, 400)

    def test_for_signup_details_data_types(self):
        '''Test for signup details where wrong data types are given'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": 2014,
                                         "password": 3.29,
                                         "role": 3232
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Details must be strings characters")
        self.assertEqual(resp.status_code, 400)

    def test_success_login(self):
        '''Test for successful login'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=self.admin_login_details,
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Login success")
        self.assertEqual(resp.status_code, 200)

    def test_fail_login(self):
        '''Test for a failing login'''
        response = self.test_client.post("/api/v2/auth/login",
                                         data=json.dumps({
                                             "email": "m@ew",
                                             "password": "dxfdfd#eE"
                                         }),
                                         headers={
                                             'content-type': 'application/json'
                                         })
        resp = json.loads(response.data)
        self.assertEqual(resp["Message"], "Login failed, check credentials")
        self.assertEqual(response.status_code, 403)

    def test_for_missing_login_data(self):
        '''Test for login without any data passed'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({}),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        self.assertEqual(resp.status_code, 400)

    def test_for_missing_login_data(self):
        '''Test for login without any data keys passed'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": "",
                                         "password": ""
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        self.assertEqual(resp.status_code, 403)

    def test_for_missing_login_keys_data(self):
        '''Test for login without any data passed in keys'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "": "j@gmail",
                                         "": "sdinsund@D2"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Must enter all credentials")
        self.assertEqual(resp.status_code, 400)

    def test_for_login_details_data_types(self):
        '''Test for login details where wrong data types are given'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": 2014,
                                         "password": 3.29
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Details must be strings characters")
        self.assertEqual(resp.status_code, 401)
