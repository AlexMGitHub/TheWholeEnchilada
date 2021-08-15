"""Run a Flask webapp.

###############################################################################
# webapp.py
#
# Revision:     1.00
# Date:         8/9/2021
# Author:       Alex
#
# Purpose:      Runs a Flask webapp that logs in to a MySQL server and allows
#               the user to query data, train machine learning models, and
#               display the results in an interactive web page.
#
###############################################################################
"""

# %% Imports
# Standard system imports
import subprocess
import os

# Related third party imports
from flask_debugtoolbar import DebugToolbarExtension

# Local application/library specific imports
from app import create_app


# %% Webapp code
app = create_app()
# Flask-Debug toolbar will only run if Flask is in development mode
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
