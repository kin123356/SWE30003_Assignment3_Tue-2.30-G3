import json
import os
from models.user import User
from models.admin import Admin

class AccountManager:
    def __init__(self, filename="accounts.json"):
        self.filename= filename
        #Checks if accounts file exists and creates it if not
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump({"users": {}, "admins": {}}, f, indent=4)

    #Opens file and returns json
    def load_accounts(self):
        with open(self.filename, "r") as f:
            return json.load(f)
    
    #Opens file and writes user to file in json
    def save_accounts(self, accounts):
        with open(self.filename, "w") as f:
            json.dump(accounts, f, indent=4)

    #Checks if account exists in file, then adds it if it doesnt
    def create_user(self, user: User):
        data = self.load_accounts()
        if user.username in data["users"]:
            return False
        data["users"][user.username] = user.to_dict()
        self.save_accounts(data)
        return True

    def create_admin(self, admin: Admin):
        data = self.load_accounts()
        if admin.username in data["admins"]:
            return False
        data["admins"][admin.username] = admin.to_dict()
        self.save_accounts(data)
        return True

    def authenticate(self, username, password):
            data = self.load_accounts()

            # check admin list
            if username in data["admins"] and data["admins"][username]["password"] == password:
                return "admin"

            # check user list
            if username in data["users"] and data["users"][username]["password"] == password:
                return "user"

            return None