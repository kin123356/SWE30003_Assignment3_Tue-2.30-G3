from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.accountManager import AccountManager
from models.user import User
from models.admin import Admin
from models.productCatalogue import ProductCatalogue
from models.catalogueManager import CatalogueManager
from models.product import Product

account_manager = AccountManager()
catalogue = ProductCatalogue()
catalogue_manager = CatalogueManager()

app = Flask(__name__)
app.secret_key = "test"

@app.route("/")
def home():
    products = catalogue.load_products()
    return render_template("index.html", products=products)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        username = request.form["username"]
        password = request.form["password"]
        account_type = request.form["account"]

        if account_type == "admin":
            new_admin = Admin(name, email, phone, username, password)
            created = account_manager.create_admin(new_admin)
        else:
            new_user = User(name, email, phone, username, password)
            created = account_manager.create_user(new_user)

        if created:
            flash("Account created successfully! Please log in.")
            return redirect(url_for("login"))
        else:
            flash("Username already exists. Try a different one.")
            return redirect(url_for("signup"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    #Logs user out when navigating so they cant login twice
    session.clear()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        role = account_manager.authenticate(username, password)
        if role:
            session["username"] = username
            session["role"] = role
            if role == "admin":
                return redirect(url_for("adminDashboard"))
            else:
                return redirect(url_for("userDashboard"))
        else:
            flash("Invalid Credentials")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/userDashboard")
def userDashboard():
    if session.get("role") != "user":
        return redirect(url_for("login"))
    return render_template("userDashboard.html", username=session["username"])

@app.route("/adminDashboard", methods=["GET", "POST"])
def adminDashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    
    if request.method == "POST":
        # Handle adding a new product
        if "add_product" in request.form:
            name = request.form["name"]
            price = float(request.form["price"])
            stock = int(request.form["stock"])
            description = request.form["description"]

            new_product = Product(name, description, price, stock)
            success = catalogue_manager.add_product(new_product)
            if success:
                flash(f"Product '{name}' added successfully!")  
            else:
                flash("Product already exists")              

        
        # Handle updating stock
        elif "update_stock" in request.form:
            product_id = request.form["product_id"]
            quantity = int(request.form["quantity"])
            catalogue_manager.update_stock(product_id, quantity)
            flash("Product stock updated successfully!")
        
        #Handle deleting product
        elif "delete_product" in request.form:
            product_name = request.form["product_id"]
            success = catalogue_manager.delete_product(product_name)
            if success:
                flash(f"Product '{product_name}' deleted successfully")
            else:
                flash("Product not found")

        return redirect(url_for("adminDashboard"))

    # Show all products on the dashboard
    products = catalogue_manager.load_products()
    return render_template("adminDashboard.html", username=session["username"], products=products)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    if session.get("role") != "user":
        return redirect(url_for("login"))
    return render_template("cart.html", username=session["username"])
if __name__ == "__main__":
    app.run(debug=True)