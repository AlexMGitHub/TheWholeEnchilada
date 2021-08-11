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


def tests(test_arg):
    """Run tests specified by test_arg.

    The variable test_arg can be a directory such as "tests/integration/" or
    a path to a specific test module, or a particular function within a test
    module.  See Pytest documentation for details.

    Pytest must be run as a subprocess, otherwise the results will not change
    upon subsequent testing.  This is due to Python cachine modules inside the
    same process.
    """
    subprocess.run(
        ["python", "-m", "pytest", "-v",                        # Verbose mode
         test_arg,                  # Test directory or module to run
         "--html=src/app/static/test-report/report.html",       # HTML report
         "--css=src/app/static/test-report/my_report.css",      # Custom CSS
         "--self-contained-html"    # HTML and CSS in single file
         ])
