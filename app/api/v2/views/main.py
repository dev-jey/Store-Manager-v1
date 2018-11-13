from .restrict import Restrictions
from ..models.product_models import Product_Model
from ..models.sale_models import Sales_Model
from ..models.user_model import User_Model

class Initialize():
    def __init__(self):
        self.restrict1 = Restrictions()
        self.only_admin = self.restrict1.only_admin
        self.must_login = self.restrict1.must_login
        self.no_products = self.restrict1.no_products
        self.only_attendant = self.restrict1.only_attendant
        self.product = Product_Model()
        self.sales_obj = Sales_Model()
        self.fail_login = self.restrict1.login_failed
        self.item = User_Model()