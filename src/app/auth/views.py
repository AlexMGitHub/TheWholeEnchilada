"""Authentication blueprint routes and view functions.

Routes/view functions:
    -   login(): Login page for webapp.  Authenticates username and password.

    -   logout(): Logout page for webapp.  Closes connection to MySQL server.
"""

# %% Imports
# Standard system imports

# Related third party imports
from flask import render_template, session, redirect, \
    url_for, flash, request
from flask_login import login_user, logout_user, login_required

# Local application/library specific imports
from . import auth
from .forms import LoginForm
from ..models import User
from .. import db


# %% Routes and view functions
@auth.route('/login', methods=["GET", "POST"])
def login():
    """Return sign-in page requesting user log in.

    Validated form input is used to attempt to connect to the MySQL server.
    If connection succeeds, user is logged into the webapp using Flask-Login.

    If connection fails, the user is returned to the login page with the error
    message displayed as an alert.
    """
    form = LoginForm()
    if form.is_submitted() and not form.validate():
        flash('Enter username and password', category="warning")
    if form.validate_on_submit():
        cnx = db.connect_to_db(form.username.data, form.password.data)
        if isinstance(cnx, db.connection_types):
            next_page = request.args.get('next')
            user = User(form.username.data)             # Create user object
            login_user(user, form.remember_me.data)     # Login user
            session['username'] = form.username.data    # Store username
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            if '(28000)' in str(cnx):
                msg = 'Invalid username or password'  # ACCESS_DENIED error
            else:
                msg = str(cnx)  # Unknown error, pass error to login page
            flash(msg, category="danger")  # Alert displayed on login form
    return render_template('auth/signin.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Return sign-in page after user logs out; indicate successful logout.

    Closes connection to MySQL server and sets cnx session variable to None.
    Logs out user via Flask-Login's logout_user function.
    User is redirected to login page that displays a successful logout message.
    """
    db.logout()                         # Logout of MySQL server
    logout_user()                       # Logout user using Flask-Login
    session['username'] = None
    session['dataset'] = None
    flash('You have been logged out', category='success')
    return redirect(url_for('auth.login'))
