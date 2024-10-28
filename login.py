import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Use a more secure key in production

# MySQL Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:ananyavastare2345@localhost/UserDB"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)


# Define the User Model
class User(db.Model):
    __tablename__ = "users"  # Specify the correct table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)


# Create the database tables if they do not exist
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Print the received username and password for debugging
        print(f"Attempting login with Username: {username}, Password: {password}")

        # Query for the user
        user = User.query.filter_by(username=username).first()

        # Print user information for debugging
        if user:
            print(
                f"User found: {user.username}, Password: {user.password}"
            )  # For debugging
        else:
            print("User not found.")

        # Directly compare passwords
        if user and user.password == password:
            session["username"] = username
            flash("Login successful!", "success")
        else:
            flash("Invalid credentials. Please try again.", "danger")

    # Always render the login page, regardless of login attempt
    return render_template("login.html")


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        new_username = request.form.get("username").strip()
        new_password = request.form.get("password").strip()

        # Create a new user and add to the database
        new_user = User(username=new_username, password=new_password)
        db.session.add(new_user)
        db.session.commit()

        flash("User added successfully!", "success")
        return redirect(url_for("login"))  # Redirect to login after adding user

    return render_template("add_user.html")


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
