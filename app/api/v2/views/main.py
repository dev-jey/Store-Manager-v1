from .restrict import Restrictions
from ..models.product_models import Product_Model
from ..models.cart_model import Cart_Model
from ..models.user_model import User_Model
from ..models.sales_model import Sale_Model
class Initialize():
    def __init__(self):
        self.restrict1 = Restrictions()
        self.no_products = self.restrict1.no_products
        self.no_items = self.restrict1.no_items
        self.no_sales = self.restrict1.no_sales
        self.product = Product_Model()
        self.cart_obj = Cart_Model()
        self.sales_obj = Sale_Model()
        self.fail_login = self.restrict1.login_failed
        self.item = User_Model()