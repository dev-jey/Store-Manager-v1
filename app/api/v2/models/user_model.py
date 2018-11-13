'''This module does all user data manipulation'''
from .main_model import InitializeConnection


class User_Model(InitializeConnection):

    '''Initializes a new user object'''

    def __init__(self, email=None, password=None, admin=False):
        InitializeConnection.__init__(self)
        self.email = email
        self.password = password
        self.admin = admin

    def save(self):
        '''method for saving users'''
        self.cursor.execute(
            "INSERT INTO users(email,password,admin) VALUES(%s,%s,%s)", (
                self.email, self.password, self.admin,)
        )

    def get(self):
        '''Method to get all users from db'''
        sql = "SELECT * FROM users"
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        allusers = []
        for user in users:
            list_of_users = list(user)
            oneuser = {}
            oneuser["id"] = list_of_users[0]
            oneuser["email"] = list_of_users[1]
            oneuser["password"] = list_of_users[2]
            oneuser["admin"] = list_of_users[3]
            allusers.append(oneuser)
        return allusers

    def update(self, userId):
        '''Method should  update a user and set him/her to admin'''
        self.cursor.execute(
            "UPDATE users SET admin = %s WHERE id = %s", (True, userId,)
        )

    def logout(self, token, date):
        '''method to logout a user from the system'''
        self.cursor.execute(
            "INSERT INTO blacklist (token, date) VALUES (%s,%s)",
            (token, date,)
        )

    def __repr__(self):
        return self.conn.close()
