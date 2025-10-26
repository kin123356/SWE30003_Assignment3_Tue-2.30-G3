class User:
    def __init__(self, name, email, phone, username, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password
        self.role = "user"

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "username": self.username,
            "password": self.password
        }

