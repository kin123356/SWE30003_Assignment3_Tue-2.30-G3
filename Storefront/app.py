from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models.accountManager import AccountManager
from models.user import User
from models.admin import Admin
from models.productCatalogue import ProductCatalogue
from models.catalogueManager import CatalogueManager
from models.product import Product
from models.shoppingCart import ShoppingCart
from models.order import Order
from models.orderManager import OrderManager
from models.payment import Payment
from models.shipment import Shipment
from models.inventory import Inventory
from models.salesAnalytics import SalesAnalytics
from models.notificationSystem import NotificationSystem

account_manager = AccountManager()
catalogue = ProductCatalogue()
catalogue_manager = CatalogueManager()
order_manager = OrderManager()
inventory = Inventory()
sales_analytics = SalesAnalytics()
notification_system = NotificationSystem()

app = Flask(__name__)
app.secret_key = "test"

@app.route("/")
def home():
    if 'cart' not in session:
        # Initialize cart for new sessions
        cart = ShoppingCart()
        session['cart'] = cart.items
    products = catalogue.load_products()
    cart_items = session.get('cart', {})
    return render_template("index.html", products=products, cart_items=cart_items)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        success = account_manager.create_user(User(first_name, last_name, email, phone, password))
        if success:
            flash("Account created successfully! Please log in.")
            return redirect(url_for("login"))
        else:
            flash("An account with this email address already exists.")
            return redirect(url_for("signup"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    #Logs user out when navigating so they cant login twice
    session.clear()
    if request.method == "POST":
        email = request.form["username"] # The form field is named 'username' but contains the email
        password = request.form["password"]

        user, role = account_manager.authenticate_by_email(email, password)
        if user and role:
            session['email'] = user['email']
            session['first_name'] = user['first_name']
            session["role"] = role
            if role == 'admin':
                return redirect(url_for('adminDashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash("Invalid Credentials")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/recover", methods=["GET", "POST"])
def recover_account():
    if request.method == "POST":
        email = request.form["email"]
        if account_manager.recover_account(email):
            flash("A password recovery link has been sent to your email.")
        else:
            flash("Email not found.")
        return redirect(url_for('login'))
    return render_template("recover_account.html")

@app.route("/userDashboard")
def userDashboard():
    if session.get("role") != "user" or 'first_name' not in session:
        return redirect(url_for("login"))
    
    orders = order_manager.get_orders_for_user(session['email'])
    return render_template("userDashboard.html", first_name=session["first_name"], orders=orders)

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
            inventory.set_stock(product_id, quantity)
            flash("Product stock updated successfully!")
        
        #Handle deleting product
        elif "create_admin" in request.form:
            first_name = request.form["admin_first_name"]
            last_name = request.form["admin_last_name"]
            email = request.form["admin_email"]
            password = request.form["admin_password"]
            success = account_manager.create_admin(Admin(first_name, last_name, email, password))
            if success:
                flash(f"Admin account for '{email}' created successfully!")
            else:
                flash("An account with this email already exists.")

        elif "delete_product" in request.form:
            product_name = request.form["product_id"]
            success = catalogue_manager.delete_product(product_name)
            if success:
                flash(f"Product '{product_name}' deleted successfully")
            else:
                flash("Product not found")

        return redirect(url_for("adminDashboard"))

    # Analytics
    total_sales = sales_analytics.get_total_sales()
    top_products = sales_analytics.get_top_selling_products()

    # Show all products on the dashboard
    products = catalogue_manager.load_products()
    return render_template(
        "adminDashboard.html", 
        first_name=session["first_name"], 
        products=products,
        total_sales=total_sales,
        top_products=top_products
    )

@app.route("/update_cart/<product_name>", methods=["POST"])
def update_cart(product_name):
    if 'first_name' not in session:
        return jsonify({'error': 'Please log in to modify your cart.'}), 401

    data = request.get_json()
    quantity = int(data.get('quantity', 0))

    product = catalogue.get_product(product_name)
    if not product:
        return jsonify({'error': 'Product not found.'}), 404

    cart = ShoppingCart()
    cart.items = session.get('cart', {})

    # If item is not in cart and we are adding it for the first time
    if product.name not in cart.items and quantity > 0:
        cart.add_item(product, quantity)
    # If item is already in cart
    elif product.name in cart.items:
        if quantity > 0:
            if quantity > 10:
                quantity = 10
            cart.update_quantity(product.name, quantity)
        else:
            cart.remove_item(product.name)
    
    session['cart'] = cart.items
    return jsonify({'success': True, 'cart': cart.items})

@app.route("/checkout", methods=["POST"])
def checkout():
    if 'first_name' not in session:
        return redirect(url_for('login'))

    cart = ShoppingCart()
    cart.items = session.get('cart', {})
    if not cart.get_items():
        flash("Your cart is empty.")
        return redirect(url_for('cart'))

    # Decrease stock for each item in the cart
    for item in cart.get_items():
        inventory.update_stock(item['product']['name'], -item['quantity'])

    # Create a new order
    order = Order(
        user_id=session['email'],
        items=[{'product': Product.from_dict(item['product']), 'quantity': item['quantity']} for item in cart.get_items()],
        total=cart.calculate_total()
    )
    order_manager.place_order(order)

    # Send order confirmation notification
    if 'email' in session:
        notification_system.send_order_confirmation(session['email'], order.order_id)

    # Simulate payment processing
    payment = Payment(order.order_id, order.total)
    if payment.process_payment():
        order_manager.update_order_status(order.order_id, 'Paid')

        # Simulate shipment creation
        # In a real app, you'd get the address from the user
        shipment = Shipment(order.order_id, '123 Example St')
        if shipment.create_shipment():
            order_manager.update_order_status(order.order_id, 'Shipped')
            if 'email' in session:
                notification_system.send_shipment_notification(session['email'], order.order_id, shipment.shipment_id)


    # Clear the cart
    cart.clear_cart()
    session['cart'] = cart.items

    flash("Your order has been placed successfully!")
    return redirect(url_for('userDashboard'))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    if session.get("role") != "user":
        return redirect(url_for("login"))
    
    cart = ShoppingCart()
    cart.items = session.get('cart', {})
    # Reconstruct Product objects for rendering
    cart_items = []
    for item_data in cart.get_items():
        product = Product.from_dict(item_data['product'])
        cart_items.append({'product': product, 'quantity': item_data['quantity']})
    total = cart.calculate_total()

    return render_template("cart.html", first_name=session["first_name"], cart_items=cart_items, total=total)

if __name__ == "__main__":
    app.run(debug=True)