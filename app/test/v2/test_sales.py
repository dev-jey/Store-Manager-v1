
from .base_test import *


class TestSales(TestsForApi):

    def test_post_sale_successful(self):
        '''Test for posting a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "title": "tecno",
                                         "quantity": 1
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "successfully sold")
        self.assertEqual(resp.status_code, 201)

    def test_post_sale_non_existent_product(self):
        '''Test for posting a sale in which the product doesnt exist'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "title": "tecno yo",
                                         "quantity": 1
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["Message"], "Product non-existent")
        self.assertEqual(resp.status_code, 404)

    def test_post_sales_no_title_given(self):
        '''Test for posting a sale with no title'''
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
                         "Must enter the title key well")
        self.assertEqual(resp.status_code, 400)

    def test_post_sale_no_quantity_given(self):
        '''Test for posting a sale with no quantity'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "title": "tecno"
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"],
                         "Must enter the quantity key well")
        self.assertEqual(resp.status_code, 400)

    def test_post_with_no_given_data(self):
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

    def test_post_sale_product_id_wrong_data_type(self):
        '''Test to assert the correct datatype for product id when
        making a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "title": 2901,
                                         "quantity": 1
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "title must be a string")
        self.assertEqual(resp.status_code, 400)

    def test_post_sale_wrong_quantity_data_type(self):
        '''Test to assert the correct datatype for quantity when
        making a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "title": "orange",
                                         "quantity": "one"
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Quantity must be an integer")
        self.assertEqual(resp.status_code, 400)

    def test_post_sale_many_fields_given(self):
        '''Test to assert the result if many fields are given'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "title": "orange",
                                         "quantity": 1,
                                         "role": "Admin"
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(
            response["message"], "Too many fields provided, only the title and quantity is required")
        self.assertEqual(resp.status_code, 400)
    
    def test_post_sale_negative_quantity_given(self):
        '''Test to assert the quantity less than zero'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "title": "orange",
                                         "quantity": -1000
                                     }),
                                     headers={
                                         'x-access-token': self.attendant_token,
                                         'content-type': 'application/json'
                                     })
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Quantity must be more than 0")
        self.assertEqual(resp.status_code, 400)

    def test_post_sale_admin(self):
        '''Test for administrator posting a sale'''
        resp = self.test_client.post("/api/v2/sales",
                                     data=json.dumps({
                                         "title": "orange",
                                         "quantity": 1
                                     }),
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

    def test_get_one_sale_admin(self):
        '''Test for getting one sale for an admin'''
        resp = self.test_client.get("/api/v2/sales/1",
                                    headers={
                                        'x-access-token': self.admin_token
                                    })
        self.assertEqual(resp.status_code, 200)

    def test_get_one_sale_attendant(self):
        '''Test for getting one sale for an attendant'''
        resp = self.test_client.get("/api/v2/sales/1",
                                    headers={
                                        'x-access-token': self.attendant_token
                                    })
        self.assertEqual(resp.status_code, 200)

    def test_get_one_sale_wrong_id_given(self):
        '''Test for getting one sale when a person enters wrong saleID'''
        resp = self.test_client.get("/api/v2/sales/400",
                                    headers={
                                        'x-access-token': self.attendant_token
                                    })
        self.assertEqual(resp.status_code, 404)
