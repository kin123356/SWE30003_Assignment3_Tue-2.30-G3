from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.accountManager import AccountManager
from models.user import User
from models.admin import Admin

account_manager = AccountManager()

app = Flask(__name__)
app.secret_key = "test"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        account_type = request.form["account"]

        if account_type == "admin":
            new_admin = Admin(username, password, name)
            created = account_manager.create_admin(new_admin)
        else:
            new_user = User(username, password, name)
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        role = account_manager.authenticate(username, password)
        if role == "admin":
            session["username"] = username
            session["role"] = "admin"
            return redirect(url_for("adminDashboard"))
        elif role == "user":
            session["username"] = username
            session["role"] = "user"
            return redirect(url_for("userDashboard"))
        else:
            flash("Invalid credentials.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/userDashboard")
def userDashboard():
    if session.get("role") != "user":
        return redirect(url_for("login"))
    return render_template("userDashboard.html", username=session["username"])

@app.route("/adminDashboard")
def adminDashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("adminDashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)