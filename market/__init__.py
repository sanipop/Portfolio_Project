# Importing necessary modules for creating a Flask web application.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Creating a Flask application instance.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
# Initializing SQLAlchemy, Bcrypt, and LoginManager extensions with the Flask app instance.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Configuring the login view and message category for LoginManager.
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# Importing routes from the market module.
from market import routes
