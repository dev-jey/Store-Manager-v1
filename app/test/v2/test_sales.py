
from .base_test import *


class TestSales(TestsForApi):

    def test_post_sale_attendant(self):
        '''Test for posting a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({"productId": 1}),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "successfully sold")
        self.assertEqual(resp.status_code, 201)

    def test_post_sale_product_non_existent(self):
        '''Test for posting a sale in which the product doesnt exist'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({"productId": 91}),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Product non-existent")
        self.assertEqual(resp.status_code, 404)

    def test_validate_posting_empty_product_id(self):
        '''Test for posting a sale with no product id'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({}),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Must enter the product Id")
        self.assertEqual(resp.status_code, 400)

    def test_validate_posting_with_no_correct_key(self):
        '''Test for posting a sale with no correct key for productId'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({"prod": 1}),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Must enter the product Id")
        self.assertEqual(resp.status_code, 400)

    def test_validate_posting_with_blank_key(self):
        '''Test for posting a sale with blank key for productId'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({"": 1}),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Must enter the product Id")
        self.assertEqual(resp.status_code, 400)

    def test_validate_product_id_data_type(self):
        '''Test to assert the correct datatype for product id when
        making a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({"productId": "one"}),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Product Id must be an integer")
        self.assertEqual(resp.status_code, 400)

    def test_post_sale_admin(self):
        '''Test for administrator posting a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({"productId": 1}),
                                     headers={
                                         'x-access-token': self.admin_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Must be an attendant!")
        self.assertEqual(resp.status_code, 401)

    def test_get_all_sales_admin(self):
        '''Test for admin getting all sales'''
        resp = self.test_client.get("/api/v2/sales",
                                    headers={
                                        'x-access-token': self.admin_token
                                    })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Success")
        self.assertEqual(resp.status_code, 200)

    def test_get_all_sales_attendant(self):
        '''Test for attendant getting all sales'''
        resp = self.test_client.get("/api/v2/sales",
                                    headers={
                                        'x-access-token': self.attendant_token
                                    })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Must be an admin")
        self.assertEqual(resp.status_code, 401)
    
    def test_getting_one_sale_admin(self):
        '''Test for getting one sale for an admin'''
        resp = self.test_client.get("/api/v2/sales/1",
                                    headers={
                                        'x-access-token': self.admin_token
                                    })
        self.assertEqual(resp.status_code, 200)

    def test_getting_one_sale_attendant(self):
        '''Test for getting one sale for an attendant'''
        resp = self.test_client.get("/api/v2/sales/1",
                                    headers={
                                        'x-access-token': self.attendant_token
                                    })
        self.assertEqual(resp.status_code, 200)

    def test_getting_one_sale_with_wrong_saleId(self):
        '''Test for getting one sale when a person enters wrong saleID'''
        resp = self.test_client.get("/api/v2/sales/400",
                                    headers={
                                        'x-access-token': self.attendant_token
                                    })
        self.assertEqual(resp.status_code, 404)