from .base_test import *


class TestUsers(TestsForApi):

    def test_successful_signup(self):
        '''Tests for a successful signup'''
        data = json.dumps({
            "email": "marys@gmail.com",
            "password": "mardsd2@Qss",
                        "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(response["Message"], "User registered")
        self.assertEqual(res.status_code, 201)

    def test_email_not_string(self):
        '''Tests for a signup with an integer email'''
        data = json.dumps({
            "email": 12121,
            "password": "mardsd2@Qss.com",
                        "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "12121 is not of type 'string'")
        self.assertEqual(res.status_code, 400)

    def test_password_not_string(self):
        '''Tests for a signup with an int password'''
        data = json.dumps({
            "email": "e@e.com",
            "password": 1233234,
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(
            response["message"], "1233234 is not of type 'string'")
        self.assertEqual(res.status_code, 400)

    def test_role_not_string(self):
        '''Tests for a signup with an int role'''
        data = json.dumps({
            "email": "e@e.com",
            "password": "James@12",
                        "admin": 65454
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "65454 is not of type 'string'")
        self.assertEqual(res.status_code, 400)

    def test_missing_email_key(self):
        '''Tests for a signup with a missing email key'''
        data = json.dumps({
            "": "e@e.com",
            "password": "James@12",
                        "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "'email' is a required property")
        self.assertEqual(res.status_code, 400)

    def test_missing_password_key(self):
        '''Tests for a signup with a missing password key'''
        data = json.dumps({
            "email": "e@e.com",
            "": "James@12",
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "'password' is a required property")
        self.assertEqual(res.status_code, 400)

    def test_missing_role_key(self):
        '''Tests for a signup with a missing role key'''
        data = json.dumps({
            "email": "e@e.com",
            "password": "James@12",
                        "": "true"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "'admin' is a required property")
        self.assertEqual(res.status_code, 400)

    def test_empty_email(self):
        '''Tests for a signup with an empty email'''
        data = json.dumps({
            "email": "",
            "password": "James@gmial.com",
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(response["message"], "Invalid email")
        self.assertEqual(res.status_code, 400)

    def test_empty_password(self):
        '''Tests for a signup with an empty password'''
        data = json.dumps({
            "email": "s@s.com",
            "password": "",
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers=self.admin_header)
        response = json.loads(res.data)
        self.assertEqual(response["message"], "Password must be long than 6 characters or less than 12")
        self.assertEqual(res.status_code, 400)

    def test_wrong_email_signup(self):
        '''Test for a signup with wrong email format given'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "emailcom",
                                         "password": "ssdsdD2@ja",
                                         "admin": "true"}),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Invalid email")
        self.assertEqual(resp.status_code, 400)

    def test_email_already_exists(self):
        '''Test for signing up with an already existing email'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "maria@gmail.com",
                                         "password": "ssdsdD2@ja",
                                         "admin": "true"
                                     }),
                                     headers=self.admin_header)
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "maria@gmail.com",
                                         "password": "ssdsdD2@ja",
                                         "admin": "true"
                                     }),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "User already exists")
        self.assertEqual(resp.status_code, 406)

    def test_short_password(self):
        '''Test for a signup with a short password'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "jame@gmail.com",
                                         "password": "dS#e3",
                                         "admin": "true"
                                     }),
                                     headers=self.admin_header)
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
                                         "admin": "true"}),
                                     headers=self.admin_header)
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
                                         "admin": "true"}),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Password must have a digit")
        self.assertEqual(resp.status_code, 400)

    def test_password_lacks_upperCase(self):
        '''Test for signup with a password with no uppercase character'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "jame@gmail.com",
                                         "password": "dddsdsd2@",
                                         "admin": "true"}),
                                     headers=self.admin_header)
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
                                         "admin": "true"}),
                                     headers=self.admin_header)
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
                                         "admin": "true"}),
                                     headers=self.admin_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Password must have a special charater")
        self.assertEqual(resp.status_code, 400)

    def test_success_login(self):
        '''Test for successful login'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=self.admin_login_details,
                                     headers=self.main_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Login success")
        self.assertEqual(resp.status_code, 200)

    def test_fail_login(self):
        '''Test for a failing login'''
        response = self.test_client.post("/api/v2/auth/login",
                                         data=json.dumps({
                                             "email": "m@ew.com",
                                             "password": "dxfdfd#eE"
                                         }),
                                         headers=self.main_header)
        resp = json.loads(response.data)
        self.assertEqual(resp["Message"], "Login failed, check credentials")
        self.assertEqual(response.status_code, 403)

    def test_for_missing_email_login_key_data(self):
        '''Test for login without any data passed in email key'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "": "j@gmail.com",
                                         "password": "sdinsund@D2"
                                     }),
                                     headers=self.main_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "'email' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_for_missing_password_login_key_data(self):
        '''Test for login without any data passed in password key'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": "j@gmail.com",
                                         "": "sdinsund@D2"
                                     }),
                                     headers=self.main_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "'password' is a required property")
        self.assertEqual(resp.status_code, 400)

    def test_for_login_details_data_types_email(self):
        '''Test for login details where wrong data types are given'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": 2014,
                                         "password": "James@12"
                                     }),
                                     headers=self.main_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "2014 is not of type 'string'")
        self.assertEqual(resp.status_code, 400)

    def test_for_login_details_data_types(self):
        '''Test for login details where wrong data types are given'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": "e@e.com",
                                         "password": 123454
                                     }),
                                     headers=self.main_header)
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "123454 is not of type 'string'")
        self.assertEqual(resp.status_code, 400)
