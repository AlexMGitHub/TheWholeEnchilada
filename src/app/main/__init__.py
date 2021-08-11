"""Main blueprint creation."""
from flask import Blueprint

main = Blueprint('main', __name__)

# These imports must be made after the Blueprint is defined to avoid errors
from . import views, errors  # nopep8
