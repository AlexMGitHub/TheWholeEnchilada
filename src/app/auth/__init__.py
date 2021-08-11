"""Authentication blueprint creation."""
from flask import Blueprint

auth = Blueprint('auth', __name__)

# These imports must be made after the Blueprint is defined to avoid errors
from . import views  # nopep8
