import json
import os
from models.user import User
from models.admin import Admin

class AccountManager:
    _instance = None

    #Singleton Pattern (Only one AccountManager can exist)
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, filename="accounts.json"):
        if self._initialized:
            return
        self._initialized = True
        self.filename= filename
        #Checks if accounts file exists and creates it if not
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                json.dump({"users": {}, "admins": {}}, f, indent=4)

            # Create default admin when generating file
            default_admin = Admin("Admin", "User", "admin@example.com", "admin")
            self.create_admin(default_admin)

    #Opens file and returns json
    def load_accounts(self):
        with open(self.filename, "r") as f:
            return json.load(f)
    
    #Opens file and writes user to file in json
    def save_accounts(self, accounts):
        with open(self.filename, "w") as f:
            json.dump(accounts, f, indent=4)

    def create_user(self, user: User):
        """Create a new user with email as the primary key."""
        data = self.load_accounts()
        if user.email in data["users"] or user.email in data["admins"]:
            return False  # User already exists
        data["users"][user.email] = user.to_dict()
        self.save_accounts(data)
        return True

    def create_admin(self, admin: Admin):
        data = self.load_accounts()
        if admin.email in data["admins"] or admin.email in data["users"]:
            return False
        data["admins"][admin.email] = admin.to_dict()
        self.save_accounts(data)
        return True

    def recover_account(self, email):
        """Simulate sending a password recovery email."""
        # In a real app, you would find the user by email and send a reset link.
        print(f"Simulating password recovery for email: {email}")
        return True


    def authenticate_by_email(self, email, password):
        """Authenticate a user by their email and password."""
        data = self.load_accounts()
        if email in data['users'] and data['users'][email]['password'] == password:
            return data['users'][email], 'user'
        if email in data['admins'] and data['admins'][email]['password'] == password:
            return data['admins'][email], 'admin'
        return None, None
