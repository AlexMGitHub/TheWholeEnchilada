"""Main blueprint routes and view functions.

Routes/view functions:
    -   index(): Main page of webapp.  Landing page after user logs in.
"""

# %% Imports
# Standard system imports
import os

# Related third party imports
from flask import render_template
from flask_login import login_required

# Local application/library specific imports
from . import main


# %% Routes and view functions
@main.route('/', methods=["GET", "POST"])
@login_required
def index():
    """Index page of webapp."""
    return render_template('dashboard.html')
