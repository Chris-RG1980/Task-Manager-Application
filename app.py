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
    # This line renders the "register.html" template and returns it as a response.
    return render_template("register.html")


# Runs the Flask application only if this script is executed directly (not imported).
if __name__ == "__main__":
    # Runs the Flask app using the host and port specified in the environment variables 'IP' and 'PORT', respectively.
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
