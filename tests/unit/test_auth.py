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
from flask import url_for, current_app, session

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


def has_no_empty_params(rule):
    """Filter out rules that can't be navigated to or require parameters."""
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def get_links():
    """Code from solution: https://stackoverflow.com/a/13318415."""
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "run_" not in url:  # Don't add URLs that run tests
                if "auth/" not in url:  # Don't add login/logout URLs
                    links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return links


def test_page_access(client, credentials, data_files):
    """Test pages to see if they can be accessed with/without login."""
    with client.session_transaction() as sess:
        sess['dataset'] = 'iris'
    username, password = credentials
    response_value = login(client, username, password)  # Sign in
    assert b'Dashboard homepage view' in response_value.data
    links = get_links()  # Get (incomplete) list of URLs in app
    for url, endpoint in links:  # Check pages load as expected
        response_value = client.get(url, follow_redirects=True)
        assert (endpoint+':').encode('UTF-8') in response_value.data
        assert "200" in response_value.status
    response_value = logout(client)  # Log out of webapp
    for url, endpoint in links:  # Check access denied
        response_value = client.get(url, follow_redirects=True)
        assert b'Please sign in' in response_value.data
        assert "200" in response_value.status


def test_bokeh_access(client, credentials, data_files):
    """Test Bokeh visualization routes redirect user if missing information."""
    with client.session_transaction() as sess:
        sess['dataset'] = None
    username, password = credentials
    response_value = login(client, username, password)  # Sign in
    assert b'Dashboard homepage view' in response_value.data
    # With no dataset selected main.datasets should load
    response_value = client.get('/datasets/', follow_redirects=True)
    assert b'main.datasets:' in response_value.data
    assert "200" in response_value.status
    # With no dataset selected main.train should redirect to main.datasets
    response_value = client.get('/train/', follow_redirects=True)
    assert b'main.datasets:' in response_value.data
    assert "200" in response_value.status
    # With no dataset selected main.results should redirect to main.datasets
    response_value = client.get('/results/', follow_redirects=True)
    assert b'main.datasets:' in response_value.data
    assert "200" in response_value.status
    # Select a dataset
    with client.session_transaction() as sess:
        sess['dataset'] = 'iris'  # Select iris dataset
    # With a dataset selected main.datasets should redirect to main.eda
    response_value = client.get('/datasets/', follow_redirects=True)
    assert b'main.eda:' in response_value.data
    assert "200" in response_value.status
    # Delete contents of data volume
    for file in data_files:
        file.unlink()
    # Without data main.train should redirect to main.eda
    response_value = client.get('/train/', follow_redirects=True)
    assert b'main.eda:' in response_value.data
    assert "200" in response_value.status
    # Without data main.results should redirect to main.train
    response_value = client.get('/results/', follow_redirects=True)
    assert b'main.train:' in response_value.data
    assert "200" in response_value.status


def test_param_routes(client, credentials):
    """Test routes that accept parameters in URL."""
    with client.session_transaction() as sess:
        sess['dataset'] = None
    username, password = credentials
    response_value = login(client, username, password)  # Sign in
    assert b'Dashboard homepage view' in response_value.data
    # Without dataset selected should be redirected to main.datasets
    response_value = client.get('/datasets/eda/', follow_redirects=True)
    assert b'main.datasets:' in response_value.data
    # Select dataset using URL
    response_value = client.get('/datasets/eda/iris', follow_redirects=True)
    assert session['dataset'] == 'iris'  # Verify dataset selected
    # Verify embedding text data from files works correctly
    response_value = client.get('/data_file/static/datasets/iris/desc/'
                                'iris.txt/display', follow_redirects=True)
    assert b'data_file.html:' in response_value.data
    assert "200" in response_value.status
