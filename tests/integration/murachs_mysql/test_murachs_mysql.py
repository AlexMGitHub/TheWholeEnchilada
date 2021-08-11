"""Test solutions to exercises in Murach's MySQL.

###############################################################################
# test_murachs_mysql.py
#
# Revision:     1.00
# Date:         8/2/2021
# Author:       Alex
#
# Purpose:      Runs functional tests on exercises from "Murach's MySQL", 3rd
#               edition by Joel Murach.  Queries a MySQL server running in a
#               separate Docker container.
#
###############################################################################
"""

# %% Imports
# Standard system imports
import time
import os

# Related third party imports
import pytest
from dotenv import load_dotenv
from mysql.connector import connect as SQLConnect
from mysql.connector import Error as SQLError
from mysql.connector.errors import DatabaseError

# Local application/library specific imports
from murachs_mysql import murachs_mysql as soln


# %% Murach's MySQL Exercises
@pytest.fixture(name="mysql_connection", scope="session")
def mysql_connection():
    """Fixture to initialize MySQL databases before testing solutions."""
    load_dotenv('.env_secrets')         # Load MySQL passwords into environment
    sql_databases = "/twe/src/murachs_mysql/sql/create_databases.sql"
    cnx = connect_to_mysql()
    cursor = cnx.cursor(buffered=True)  # Buffered cursor auto fetches results
    create_databases(cursor, sql_databases)     # Create databases for tests
    cursor.execute("USE ap")                    # Set database to 'ap'
    cursor.close()
    yield cnx       # Pass connection to tests, teardown after testing complete
    cnx.close()     # Close connection to MySQL server as part of teardown


def connect_to_mysql():
    """Connect to MySQL server.

    MySQL server takes time to boot-up.  Retry connection if it initially
    fails.
    """
    connected = False
    connection_attempts = 0
    while not connected and connection_attempts < 10:
        try:
            cnx = SQLConnect(user='root',
                             password=os.environ['MYSQL_ROOT_PASSWORD'],
                             host='db',
                             auth_plugin='caching_sha2_password',
                             get_warnings=True,
                             raise_on_warnings=False)
            connected = True    # Successfully connected to server
        except DatabaseError as err:
            print(err)
            connection_attempts += 1
            time.sleep(1)       # Wait a second before retrying connection
    if not connected:
        raise DatabaseError("Failed to connect to MySQL server.")
    return cnx


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


def test_chapter3_solutions(mysql_connection):
    """Test solutions to chapter 3 exercises in Murach's MySQL."""
    chap3 = soln.chap3_solutions()          # List of queries
    cursor = mysql_connection.cursor()
    results_size = ((122, 3),   # Exercise 3.8, (123 rows, 3 cols) in result
                    (41, 1),    # Exercise 3.9, (41 rows, 1 col) in result
                    (12, 4),    # Exercise 3.10
                    (5, 4),     # Exercise 3.11
                    (11, 4),    # Exercise 3.12
                    (1, 1),     # Exercise 3.13
                    (1, 3)      # Exercise 3.14
                    )
    for solution, (rows, cols) in zip(chap3, results_size):
        cursor.execute(solution)            # Execute solution query
        cursor.fetchall()                   # Fetch all results of query
        col_names = cursor.column_names
        assert cursor.rowcount == rows      # Check number of rows in result
        assert len(col_names) == cols       # Check number columns in result


def test_chapter4_solutions(mysql_connection):
    """Test solutions to chapter 4 exercises in Murach's MySQL."""
    chap4 = soln.chap4_solutions()          # List of queries
    cursor = mysql_connection.cursor()
    results_size = ((114, 22),  # Exercise 4.1, (114 rows, 22 cols) in result
                    (11, 4),    # Exercise 4.2, (11 rows, 4 cols) in result
                    (122, 3),   # Exercise 4.3
                    (118, 5),   # Exercise 4.4
                    (2, 3),     # Exercise 4.5
                    (54, 2),    # Exercise 4.6
                    (122, 2)    # Exercise 4.7
                    )
    for solution, (rows, cols) in zip(chap4, results_size):
        cursor.execute(solution)            # Execute solution query
        cursor.fetchall()                   # Fetch all results of query
        col_names = cursor.column_names
        assert cursor.rowcount == rows      # Check number of rows in result
        assert len(col_names) == cols       # Check number columns in result


def test_chapter5_solutions(mysql_connection):
    """Test solutions to chapter 5 exercises in Murach's MySQL."""
    chap5 = soln.chap5_solutions()          # List of queries
    cursor = mysql_connection.cursor()
    exp_results = (1,           # Exercise 5.1, 1 affected row
                   1,           # Exercise 5.2, 1 affected row
                   1,           # Exercise 5.3
                   1,           # Exercise 5.4
                   2,           # Exercise 5.5
                   1,           # Exercise 5.6
                   1,           # Exercise 5.7
                   0,           # Exercise 5.8
                   2,           # Exercise 5.9, statement 1
                   1            # Exercise 5.9, statement 2
                   )
    for solution, num_rows in zip(chap5, exp_results):
        cursor.execute(solution)            # Execute solution query
        assert cursor.rowcount == num_rows  # Verify number of affected rows


def test_chapter6_solutions(mysql_connection):
    """Test solutions to chapter 6 exercises in Murach's MySQL."""
    chap6 = soln.chap6_solutions()          # List of queries
    cursor = mysql_connection.cursor()
    results_size = ((34, 2),    # Exercise 6.1, (34 rows, 2 cols) in result
                    (34, 2),    # Exercise 6.2, (34 rows, 2 cols) in result
                    (34, 3),    # Exercise 6.3
                    (10, 3),    # Exercise 6.4
                    (10, 3),    # Exercise 6.5
                    (22, 2),    # Exercise 6.6
                    (2, 2),     # Exercise 6.7
                    (40, 4),    # Exercise 6.8
                    (11, 4),    # Exercise 6.9
                    (11, 5),    # Exercise 6.10
                    (5, 3)      # Exercise 6.11
                    )
    for solution, (rows, cols) in zip(chap6, results_size):
        cursor.execute(solution)            # Execute solution query
        cursor.fetchall()                   # Fetch all results of query
        col_names = cursor.column_names
        assert cursor.rowcount == rows      # Check number of rows in result
        assert len(col_names) == cols       # Check number columns in result


def test_chapter7_solutions(mysql_connection):
    """Test solutions to chapter 7 exercises in Murach's MySQL."""
    chap7 = soln.chap7_solutions()          # List of queries
    cursor = mysql_connection.cursor()
    results_size = ((34, 1),    # Exercise 7.1, (34 rows, 1 col) in result
                    (20, 2),    # Exercise 7.2, (20 rows, 2 cols) in result
                    (54, 2),    # Exercise 7.3
                    (6, 4),     # Exercise 7.4
                    (1, 1),     # Exercise 7.5
                    (38, 3),    # Exercise 7.6
                    (34, 4),    # Exercise 7.7
                    (34, 4),    # Exercise 7.8
                    (1, 1)      # Exercise 7.9
                    )
    for solution, (rows, cols) in zip(chap7, results_size):
        cursor.execute(solution)            # Execute solution query
        cursor.fetchall()                   # Fetch all results of query
        col_names = cursor.column_names
        assert cursor.rowcount == rows      # Check number of rows in result
        assert len(col_names) == cols       # Check number columns in result


def test_chapter8_solutions(mysql_connection):
    """Test solutions to chapter 8 exercises in Murach's MySQL."""
    chap8 = soln.chap8_solutions()          # List of queries
    cursor = mysql_connection.cursor()
    results_size = ((114, 4),   # Exercise 8.1, (114 rows, 4 cols) in result
                    (114, 3)    # Exercise 8.2, (114 rows, 3 cols) in result
                    )
    for solution, (rows, cols) in zip(chap8, results_size):
        cursor.execute(solution)            # Execute solution query
        cursor.fetchall()                   # Fetch all results of query
        col_names = cursor.column_names
        assert cursor.rowcount == rows      # Check number of rows in result
        assert len(col_names) == cols       # Check number columns in result


def test_chapter9_solutions(mysql_connection):
    """Test solutions to chapter 9 exercises in Murach's MySQL."""
    chap9 = soln.chap9_solutions()          # List of queries
    cursor = mysql_connection.cursor()
    results_size = ((114, 4),   # Exercise 9.1, (114 rows, 4 cols) in result
                    (0, 0),     # Exercise 9.2, USE ex database
                    (6, 4),     # Exercise 9.2
                    (0, 0),     # Exercise 9.2, USE ap database
                    (122, 6),   # Exercise 9.3
                    (29, 7),    # Exercise 9.4
                    (0, 0),     # Exercise 9.5, USE ap database
                    (5, 3),     # Exercise 9.5
                    (0, 0),     # Exercise 9.5, USE ap database
                    (11, 3)     # Exercise 9.6
                    )
    for solution, (rows, cols) in zip(chap9, results_size):
        cursor.execute(solution)            # Execute solution query
        cursor.fetchall()                   # Fetch all results of query
        col_names = cursor.column_names
        assert cursor.rowcount == rows      # Check number of rows in result
        assert len(col_names) == cols       # Check number columns in result
