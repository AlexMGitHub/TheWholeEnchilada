"""Test authorization functionality of webapp.

###############################################################################
# test_auth.py
#
# Revision:     1.00
# Date:         8/14/2021
# Author:       Alex
#
# Purpose:      Runs unit tests to validate webapp authorization functionality.
#
###############################################################################
"""

# %% Imports
# Standard system imports

# Related third party imports

# Local application/library specific imports


# %% Authorization unit tests
def login(client, username, password):
    """Login to webapp with test client."""
    return client.post('/auth/login', data=dict(
        username=username,
        password=password,
        remember_me=False
    ), follow_redirects=True)


def logout(client):
    """Logout of webapp with test client."""
    return client.get('/auth/logout', follow_redirects=True)


def test_login_logout(client, credentials):
    """Test login and logout functionality."""
    username, password = credentials
    response_value = login(client, username, password)
    assert b'Dashboard homepage view' in response_value.data
    assert "200" in response_value.status
    response_value = logout(client)
    assert b'You have been logged out' in response_value.data
    assert "200" in response_value.status
    response_value = login(client, '', '')
    assert b'Enter username and password' in response_value.data
    assert "200" in response_value.status
    response_value = login(client, username, 'invalid')
    assert b'Invalid username or password' in response_value.data
    assert "200" in response_value.status
    response_value = login(client, 'invalid', password)
    assert b'Invalid username or password' in response_value.data
    assert "200" in response_value.status


def test_errors(client, credentials):
    """Test error pages."""
    username, password = credentials
    response_value = login(client, username, password)  # Log in to webapp
    response_value = client.post('/invalid')    # Expect 404 not found error
    assert b'404' in response_value.data
    assert "404" in response_value.status
    response_value = logout(client)             # Log out of webapp
    response_value = client.post('/invalid')    # Expect 404 not found error
    assert b'404' in response_value.data
    assert "404" in response_value.status
