users = []


class User_Model():
    def __init__(self, email, password, role):
        self.id = len(users) + 1
        self.email = email
        self.password = password
        self.role = role

    def save(self):
        new_user = {
                "id": self.id,
                "email": self.email,
                "password": self.password,
                "role": self.role
            }
        users.append(new_user)


def destroy():
    users.clear()
