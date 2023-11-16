# Imports the 'os' module, which provides a portable way of using operating system-dependent functionality.
import os

# Import necessary modules and functions from the Flask library
from flask import (
    Flask,  # Import Flask class for creating the web application
    flash,  # Import flash messaging for sending feedback to the user
    render_template,  # Import function for rendering HTML templates
    redirect,  # Import function for URL redirection
    request,  # Import request object to access incoming request data
    session,  # Import session object for handling user sessions
    url_for,  # Import function for generating URLs for specific functions/routes
)

# Imports the 'PyMongo' class from the 'flask_pymongo' module, which is a Flask extension for interacting with MongoDB.
from flask_pymongo import PyMongo

# Imports the 'ObjectId' class from the 'bson.objectid' module, which represents a unique identifier for documents in MongoDB.
from bson.objectid import ObjectId

# Importing specific functions (generate_password_hash, check_password_hash) from the werkzeug.security module.
from werkzeug.security import generate_password_hash, check_password_hash

# Checks if a file named 'env.py' exists.
if os.path.exists("env.py"):
    # If 'env.py' exists, imports the content of 'env.py'.
    import env

# Creates a Flask web application instance named 'app'.
app = Flask(__name__)

# Sets the MongoDB database name by retrieving it from the environment variable 'MONGO_DBNAME'.
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# Sets the URI (connection string) for MongoDB by retrieving it from the environment variable 'MONGO_URI'.
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# Sets the secret key for the Flask application by retrieving it from the environment variable 'SECRET_KEY'.
app.secret_key = os.environ.get("SECRET_KEY")

# It creates a PyMongo object named 'mongo' that represents the connection to the MongoDB database.
mongo = PyMongo(app)


# This decorator marks the following function to be the handler for the specified route ("/")
# When a request is made to the root URL ("/"), this function will be invoked.
@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    # Retrieve tasks from the MongoDB database using the `find()` method from the `tasks` collection.
    tasks = mongo.db.tasks.find()
    # Render the HTML template named "tasks.html" and pass the retrieved tasks data to it.
    # This HTML template will use the tasks data to display information on the webpage.
    return render_template(
        "tasks.html", tasks=tasks
    )  # (task=tasks) 1st task is what the template will use and the second tasks is what was found in the database.


# This line creates a route "/register" that listens for both GET and POST requests.
@app.route("/register", methods=["GET", "POST"])
# This function, named register, is executed when the "/register" route is accessed.
def register():
    # Check if the request method is POST
    if request.method == "POST":
        # Access the MongoDB collection 'users' and search for a document
        # where the 'username' field matches the username provided in the form
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )  # .lower() converts the username to lowercase

        if existing_user:  # Checks if the variable 'existing_user' evaluates to True
            flash(
                "Username already exists"
            )  # If 'existing_user' is True, a message "Username already exists" is flashed (typically used to display temporary messages)
            return redirect(
                url_for("register")
            )  # Redirects the user to the 'register' route/page

        # Create a dictionary named 'register' to store user registration information.
        register = {
            # Assign the value of the 'username' key in the dictionary to the lowercase version of the username obtained from the form input.
            "username": request.form.get("username").lower(),
            # Assign the value of the 'password' key in the dictionary to a hashed version of the password obtained from the form input using a hashing function (generate_password_hash).
            "password": generate_password_hash(request.form.get("password")),
        }
        # Insert the 'register' dictionary containing user registration information into the 'users' collection in the MongoDB database.
        mongo.db.users.insert_one(register)

        # Put the user into 'session' cookie
        # Set the value of the "user" key in the session cookie to the lowercase value of the input received from a form field named "username"
        session["user"] = request.form.get("username").lower()
        # Display a message to the user indicating that the registration was successful
        flash("Registration Successfull")

    # This line renders the "register.html" template and returns it as a response.
    return render_template("register.html")


# Runs the Flask application only if this script is executed directly (not imported).
if __name__ == "__main__":
    # Runs the Flask app using the host and port specified in the environment variables 'IP' and 'PORT', respectively.
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
