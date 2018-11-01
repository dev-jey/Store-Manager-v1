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
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["Message"], "User registered")
        self.assertEqual(res.status_code, 201)

    def test_extra_field_signup(self):
        '''Tests for a signup with an extra field'''
        data = json.dumps({
            "email": "marys@gmail.com",
            "password": "mardsd2@Qss",
                        "admin": "false",
                        "Address": "Kenya"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "Too many fields entered. Only 3 required")
        self.assertEqual(res.status_code, 400)

    def test_email_not_string(self):
        '''Tests for a signup with an integer email'''
        data = json.dumps({
            "email": 12121,
            "password": "mardsd2@Qss",
                        "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "Email must contain string characters only")
        self.assertEqual(res.status_code, 400)

    def test_password_not_string(self):
        '''Tests for a signup with an int password'''
        data = json.dumps({
            "email": "e@e",
            "password": 1233234,
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(
            response["message"], "Password must contain string characters only")
        self.assertEqual(res.status_code, 400)

    def test_role_not_string(self):
        '''Tests for a signup with an int role'''
        data = json.dumps({
            "email": "e@e",
            "password": "James@12",
                        "admin": 65454
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "Admin role must contain string characters only")
        self.assertEqual(res.status_code, 400)

    def test_missing_email_key(self):
        '''Tests for a signup with a missing email key'''
        data = json.dumps({
            "": "e@e",
            "password": "James@12",
                        "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "Must enter email attribute precisely")
        self.assertEqual(res.status_code, 400)

    def test_missing_password_key(self):
        '''Tests for a signup with a missing password key'''
        data = json.dumps({
            "email": "e@e",
            "": "James@12",
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "Must enter password attribute precisely")
        self.assertEqual(res.status_code, 400)

    def test_missing_role_key(self):
        '''Tests for a signup with a missing role key'''
        data = json.dumps({
            "email": "e@e",
            "password": "James@12",
                        "": "true"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "Must enter admin attribute precisely")
        self.assertEqual(res.status_code, 400)

    def test_space_in_email(self):
        '''Tests for a signup with a space in email'''
        data = json.dumps({
            "email": "e@e  ",
            "password": "James@12",
                        "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"], "Email cannot have a space")
        self.assertEqual(res.status_code, 400)

    def test_space_in_password(self):
        '''Tests for a signup with a space in password'''
        data = json.dumps({
            "email": "e@e",
            "password": "   James@12",
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"], "Password cannot have a space")
        self.assertEqual(res.status_code, 400)

    def test_empty_email(self):
        '''Tests for a signup with an empty email'''
        data = json.dumps({
            "email": "",
            "password": "James@12",
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"], "Kindly enter your email")
        self.assertEqual(res.status_code, 400)

    def test_empty_password(self):
        '''Tests for a signup with an empty password'''
        data = json.dumps({
            "email": "s@s",
            "password": "",
            "admin": "false"
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"], "Kindly enter your password")
        self.assertEqual(res.status_code, 400)

    def test_empty_role(self):
        '''Tests for a signup with an empty role'''
        data = json.dumps({
            "email": "s@s",
            "password": "James@12",
            "admin": ""
        })
        res = self.test_client.post("/api/v2/auth/signup",
                                    data=data,
                                    headers={
                                        'x-access-token': self.admin_token,
                                        'content-type': 'application/json'
                                    })
        response = json.loads(res.data)
        self.assertEqual(response["message"],
                         "Kindly enter your admin status true/false")
        self.assertEqual(res.status_code, 400)

    def test_wrong_email_signup(self):
        '''Test for a signup with wrong email format given'''
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "emailcom",
                                         "password": "ssdsdD2@ja",
                                         "admin": "true"}),
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
                                         "admin": "true"
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        resp = self.test_client.post("/api/v2/auth/signup",
                                     data=json.dumps({
                                         "email": "maria@gmail.com",
                                         "password": "ssdsdD2@ja",
                                         "admin": "true"
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
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
                                         "admin": "true"}),
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
                                         "admin": "true"}),
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
                                         "admin": "true"}),
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
                                         "admin": "true"}),
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
                                         "admin": "true"}),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Password must have a special charater")
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

    def test_for_missing_email_login_key_data(self):
        '''Test for login without any data passed in email key'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "": "j@gmail",
                                         "password": "sdinsund@D2"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Email field must be filled precisely")
        self.assertEqual(resp.status_code, 400)

    def test_for_missing_password_login_key_data(self):
        '''Test for login without any data passed in password key'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "": "j@gmail",
                                         "password": "sdinsund@D2"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Email field must be filled precisely")
        self.assertEqual(resp.status_code, 400)

    def test_for_login_details_data_types_email(self):
        '''Test for login details where wrong data types are given'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": 2014,
                                         "password": "James@12"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Email must contain string characters only")
        self.assertEqual(resp.status_code, 400)

    def test_for_login_details_data_types(self):
        '''Test for login details where wrong data types are given'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": "e@e",
                                         "password": 123454
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Password must contain string characters only")
        self.assertEqual(resp.status_code, 400)

    def test_for_login_details_extra_field(self):
        '''Test for login details where an extra field is given'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": "e@e",
                                         "password": "James@12",
                                         "admin": "true"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Too many fields entered. Only email,password required")
        self.assertEqual(resp.status_code, 400)

    def test_for_login_details_email_with_space(self):
        '''Test for login details where email has a space'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": "e@e  ",
                                         "password": "James@12"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Invalid email check for space characters")
        self.assertEqual(resp.status_code, 400)

    def test_for_login_details_password_with_space(self):
        '''Test for login details where password has a space'''
        resp = self.test_client.post("/api/v2/auth/login",
                                     data=json.dumps({
                                         "email": "e@e",
                                         "password": "   James@12"
                                     }),
                                     headers={
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Password cant have space characters")
        self.assertEqual(resp.status_code, 400)
