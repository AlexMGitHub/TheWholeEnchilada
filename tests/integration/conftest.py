"""Pytest fixtures for integration tests."""

# %% Imports
# Standard system imports
import os

# Related third party imports
import pytest
from mysql.connector import Error as SQLError

# Local application/library specific imports
from app.db_connector import MySQLDatabase


# %% Integration test fixtures
def create_databases(cursor, filename):
    """Create new databases from an .SQL file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    queries = ''.join(lines)
    try:
        for query in queries.split(';'):
            cursor.execute(query)
    except SQLError as err:
        print("Failed creating database: {}".format(err))
        exit(1)


@pytest.fixture(scope="session")
def credentials():
    """Return MySQL root credentials stored in Docker secrets files."""
    with open(os.environ['MYSQL_ROOT_PASSWORD_FILE'], 'r') as secret_file:
        password = secret_file.read()
    return 'root', password


@pytest.fixture(name="mysql_connection", scope="session")
def mysql_connection(credentials):
    """Fixture to initialize MySQL databases before testing solutions."""
    username, password = credentials
    sql_databases = "/twe/src/murachs_mysql/sql/create_databases.sql"
    db = MySQLDatabase()
    cnx = db.connect_to_db(username, password)
    cursor = cnx.cursor(buffered=True)  # Buffered cursor auto fetches results
    create_databases(cursor, sql_databases)     # Create databases for tests
    cursor.execute("USE ap")                    # Set database to 'ap'
    cursor.close()
    yield cnx       # Pass connection to tests, teardown after testing complete
    cnx.close()     # Close connection to MySQL server as part of teardown
