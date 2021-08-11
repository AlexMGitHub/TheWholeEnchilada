"""Main blueprint error handlers.

Error handlers:
    -   page_not_found(): Handles HTTP 404 errors.

    -   internal_server_error(): Handles HTTP 500 errors.
"""

# %% Imports
# Standard system imports

# Related third party imports
from flask import render_template

# Local application/library specific imports
from . import main


# %% Error handlers
@main.app_errorhandler(404)
def page_not_found(e):
    """Return page for HTTP 404 "page not found" response code."""
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """Return page for HTTP 500 "internal server error" response code."""
    return render_template('500.html'), 500
