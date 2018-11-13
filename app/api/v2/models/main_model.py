import datetime
from .db_models import Db

class InitializeConnection():
    '''Initializes connection to the db'''
    def __init__(self):
        self.db = Db()
        self.conn = self.db.createConnection()
        self.db.createTables()
        self.cursor = self.conn.cursor()
        self.date = datetime.datetime.now()
