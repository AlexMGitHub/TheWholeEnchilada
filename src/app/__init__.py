"""Application factory and blueprint registration."""

# %% Imports
# Standard system imports
import os

# Related third party imports
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

# Local application/library specific imports
from .db_connector import MySQLDatabase


# %% App factory
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

db = MySQLDatabase()  # Create object representing MySQL database


def create_app():  # config_name):
    """Application factory function for webapp."""
    app = Flask(__name__)
    # Read SECRET_KEY from Docker secrets file
    with open(os.environ['FLASK_SECRET_KEY_FILE'], 'r') as secret_file:
        app.config['SECRET_KEY'] = secret_file.read()
    # Initialize login manager and blueprints
    login_manager.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
