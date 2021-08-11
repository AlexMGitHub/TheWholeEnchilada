"""Collection of forms used in webapp.

Forms:
    -   LoginForm: Defines fields for login form.
"""

# %% Imports
# Standard system imports

# Related third party imports
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

# Local application/library specific imports


# %% Forms
class LoginForm(FlaskForm):
    """Implements login form functionality."""

    username = StringField('Enter username', validators=[DataRequired()])
    password = PasswordField('Enter password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')
