
from .base_test import *


class TestSales(TestsForApi):

    def test_post_and_get_sales(self):
        '''Test for posting a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "productId": 1,
                                         "quantity": 1
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "successfully sold")
        self.assertEqual(resp.status_code, 201)

        '''Test for posting a sale in which the product doesnt exist'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "productId": 91,
                                         "quantity": 1
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Product non-existent")
        self.assertEqual(resp.status_code, 404)

        '''Test for posting a sale with no product id'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "quantity": 1
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Must enter the product Id key well")
        self.assertEqual(resp.status_code, 400)

        '''Test for posting a sale with no quantity'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "productId": 1
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Must enter the quantity key well")
        self.assertEqual(resp.status_code, 400)

        '''Test for posting a sale with no data given'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Must enter the product details in the body")
        self.assertEqual(resp.status_code, 400)

        '''Test to assert the correct datatype for product id when
        making a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "productId": "one",
                                         "quantity": 1
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Product Id must be an integer")
        self.assertEqual(resp.status_code, 400)

        '''Test to assert the correct datatype for quantity when
        making a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "productId": 1,
                                         "quantity": "one"
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Quantity must be an integer")
        self.assertEqual(resp.status_code, 400)

        '''Test to assert the result if many fields are given'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "productId": 1,
                                         "quantity": 1,
                                         "role": "Admin"
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "Too many fields provided, only the productId and quantity is required")
        self.assertEqual(resp.status_code, 400)

        '''Test to assert the quantity less than zero'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "productId": 1,
                                         "quantity": -1000
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Quantity must be more than 0")
        self.assertEqual(resp.status_code, 400)

        '''Test for administrator posting a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "productId": 1,
                                         "quantity": 1
                                     }),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Must be an attendant!")
        self.assertEqual(resp.status_code, 401)

        '''Test for admin getting all sales'''
        resp = self.test_client.get("/api/v2/sales",
                                    headers={
                                        'x-access-token': self.admin_token
                                    })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Success")
        self.assertEqual(resp.status_code, 200)

        '''Test for attendant getting all sales'''
        resp = self.test_client.get("/api/v2/sales",
                                    headers={
                                        'x-access-token': self.attendant_token
                                    })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Must be an admin")
        self.assertEqual(resp.status_code, 401)

        '''Test for getting one sale for an admin'''
        resp = self.test_client.get("/api/v2/sales/1",
                                    headers={
                                        'x-access-token': self.admin_token
                                    })
        self.assertEqual(resp.status_code, 200)

        '''Test for getting one sale for an attendant'''
        resp = self.test_client.get("/api/v2/sales/1",
                                    headers={
                                        'x-access-token': self.attendant_token
                                    })
        self.assertEqual(resp.status_code, 200)

        '''Test for getting one sale when a person enters wrong saleID'''
        resp = self.test_client.get("/api/v2/sales/400",
                                    headers={
                                        'x-access-token': self.attendant_token
                                    })
        self.assertEqual(resp.status_code, 404)
