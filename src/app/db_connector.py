"""Define classes used to interact with MySQL database.

Classes:
    -   MySQLDatabase: Store connection to MySQL database.
"""

# %% Imports
# Standard system imports
import os

# Related third party imports
from mysql.connector import connect
from mysql.connector.errors import DatabaseError
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection_cext import CMySQLConnection

# Local application/library specific imports


# %% Database models
class MySQLDatabase():
    """Store connection to MySQL database.

    Methods to connect to, disconnect from, and query MySQL database.
    """

    def __init__(self):
        """Set connection to None and define connection object types."""
        self.connection = None
        self.connection_types = (MySQLConnection, PooledMySQLConnection,
                                 CMySQLConnection)

    def connect_to_db(self, user, password):
        """Connect to MySQL server.

        If connection succeeds, return the MySQLConnection object.
        Otherwise, return the error message.
        """
        try:
            cnx = connect(user=user,
                          password=password,
                          host='db',
                          auth_plugin='caching_sha2_password',
                          database=os.environ['MYSQL_DATABASE'],
                          get_warnings=True,
                          raise_on_warnings=False)
            self.connection = cnx
            return cnx  # Successfully connected to MySQL server
        except DatabaseError as err:
            return err  # Connection failed, return error message

    def query_db_user(self, user_id):
        """Query the MySQL database to verify user exists in system."""
        cnx = self.connection
        if not isinstance(cnx, self.connection_types):
            return False
        cursor = cnx.cursor(buffered=True)  # Buffered cursor fetches results
        query = f"""SELECT USER()
                    WHERE USER() LIKE "{user_id}@%"
                    """
        cursor.execute(query)
        rowcount = cursor.rowcount
        cursor.close()
        if rowcount == 0:  # User doesn't exist
            return False
        return True

    def logout(self):
        """Close MySQL connection and set connection reference to None."""
        if not isinstance(self.connection, self.connection_types):
            return                  # Not connected to MySQL server
        self.connection.close()     # Close MySQL connection
        self.connection = None      # Remove reference to connection object
