"""Pytest fixtures for unit tests."""

# %% Imports
# Standard system imports
import os
from pathlib import Path
import shutil

# Related third party imports
import pytest

# Local application/library specific imports
from app import create_app


# %% Unit test fixtures
@pytest.fixture(scope="session")
def client():
    """Use Flask's test client as a Pytest fixture to unit test webapp."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF token for testing
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def credentials():
    """Return MySQL credentials stored in Docker secrets files."""
    username = os.environ['MYSQL_USER']
    with open(os.environ['MYSQL_PASSWORD_FILE'], 'r') as secret_file:
        password = secret_file.read()
    return username, password


@pytest.fixture(scope="function")
def data_files():
    """Copy data files to Docker data volume for testing.

    Return generator of destination paths of the copied files.
    """
    src = Path('tests/unit/data')
    dest = Path('src/bokeh_server/data')
    src_files = src.glob('*')
    for file in src_files:
        shutil.copy(file, dest)
    return dest.glob('*')
