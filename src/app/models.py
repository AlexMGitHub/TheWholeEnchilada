"""Define models used by webapp.

Models:
    -   User: Inherits from UserMixin class to represent a webapp user.
"""

# %% Imports
# Standard system imports

# Related third party imports
from flask_login import UserMixin

# Local application/library specific imports
from . import login_manager
from . import db


# %% User Models
class User(UserMixin):
    """User class to represent a user logged into the webapp."""

    def __init__(self, id):
        """Accept and store a user ID."""
        self.id = id

    def is_administrator(self):
        """Return True if user is administrator, otherwise False."""
        return self.id == 'root'


@login_manager.user_loader
def load_user(user_id):
    """Check that user is still logged into database.

    If user is logged into database, return True.  Otherwise return None.
    """
    if db.query_db_user(user_id):
        return User(user_id)
    return None
