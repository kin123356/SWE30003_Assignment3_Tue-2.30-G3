class User:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.role = "user"

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "name": self.name
        }

