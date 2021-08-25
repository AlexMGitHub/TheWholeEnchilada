"""Define classes used to interact with MySQL database.

Classes:
    -   MySQLDatabase: Store connection to MySQL database.
"""

# %% Imports
# Standard system imports
import os
from pathlib import Path
import math

# Related third party imports
from mysql.connector import connect, Error as SQLError
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
        self.database = os.environ['MYSQL_DATABASE']

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
                          database=self.database,
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

    def query_table_exists(self, table):
        """Determine if specified table exists in MySQL database."""
        cnx = self.connection
        if not isinstance(cnx, self.connection_types):
            raise DatabaseError('No connection to database!')
        cursor = cnx.cursor(buffered=True)  # Buffered cursor fetches results
        query = f"""SHOW tables LIKE "{table}";"""
        cursor.execute(query)
        rowcount = cursor.rowcount
        cursor.close()
        if rowcount == 0:  # Table doesn't exist
            return False
        return True

    def create_table(self, sql_path):
        """Load SQL file containing table into ml_data database."""
        file_path = Path('/twe/src/app') / sql_path
        cnx = self.connection
        if not isinstance(cnx, self.connection_types):
            raise DatabaseError('No connection to database!')
        cursor = cnx.cursor()
        with open(file_path, 'r') as f:
            lines = f.readlines()
        queries = ''.join(lines)
        try:
            for query in queries.split(';'):
                cursor.execute(query)
            cursor.close()
            cnx.commit()
        except SQLError as err:
            print("Failed creating database: {}".format(err))
        cursor.close()

    def query_table_size(self, table):
        """Return number of rows and columns contained in table."""
        cnx = self.connection
        if not isinstance(cnx, self.connection_types):
            raise DatabaseError('No connection to database!')
        cursor = cnx.cursor(buffered=True)  # Buffered cursor fetches results
        try:
            query = f"""DESCRIBE {table};"""
            cursor.execute(query)
            colcount = cursor.rowcount  # Result lists columns of table
            query = f"""SELECT COUNT(*) FROM {table};"""
            cursor.execute(query)
            rowcount = cursor.fetchone()[0]
            cursor.close()
            return rowcount, colcount
        except SQLError:
            return (0, 0)

    def describe_table(self, table):
        """Generate summary statistics of numeric columns of table."""
        cnx = self.connection
        if not isinstance(cnx, self.connection_types):
            raise DatabaseError('No connection to database!')
        columns, data_types, summary = [], [], []
        percentiles = [0.25, 0.5, 0.75]
        cursor = cnx.cursor(buffered=True)  # Buffered cursor fetches results
        # Determine which columns have numeric data types
        query_numeric_columns = f"""
        SELECT column_name, data_type FROM information_schema.columns
                WHERE table_schema="{self.database}" AND
                    table_name="{table}" AND
                    data_type IN("int", "float", "double", "decimal") AND
                    column_key != "PRI";"""
        try:
            cursor.execute(query_numeric_columns)
            for column, data_type in cursor:
                columns.append(column)
                data_types.append(data_type)
        except SQLError:
            return None
        # Apply aggregate functions to each numeric column
        for idx, (column, data_type) in enumerate(zip(columns, data_types)):
            query_aggregate_functions = f"""
            SELECT COUNT({column}), AVG({column}), STD({column}),
            MIN({column}), MAX({column})
            FROM {table};
            """
            cursor.execute(query_aggregate_functions)
            for count, avg, std, mini, maxi in cursor:
                summary.append({
                    'column':       column,
                    'data_type':    data_type,
                    'count':        count,
                    'avg':          avg,
                    'std':          std,
                    'min':          mini,
                    'max':          maxi
                })
            # Calculate 25th, 50th, and 75th percentiles for each column
            for perc in percentiles:
                whole = False
                index = math.ceil(count * perc)
                if index == count * perc:
                    whole = True  # Index is whole number
                query_percentiles = f"""
                SELECT {column}, row_index
                FROM
                    (
                    SELECT {column}, ROW_NUMBER() OVER w AS 'row_index'
                    FROM {table}
                    WINDOW w AS (ORDER BY {column} ASC)
                    ) AS temp
                WHERE row_index >= {index}
                LIMIT 2;
                """
                cursor.execute(query_percentiles)
                val1 = cursor.fetchone()[0]
                val2 = cursor.fetchone()[0]
                if whole:
                    percentile = (val1 + val2) / 2
                else:
                    percentile = val1
                perc_key = str(round(100*perc)) + '%'
                summary[idx][perc_key] = percentile  # Add percentile to dict
        cursor.close()
        return summary

    def get_table(self, table):
        """Return table as dictionary where keys are the table column names."""
        cnx = self.connection
        if not isinstance(cnx, self.connection_types):
            raise DatabaseError('No connection to database!')
        # Get column names of table and assign to dict as keys
        cursor = cnx.cursor()  # Unbuffered cursor, must fetch results
        query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}'
        """
        cursor.execute(query)
        table_results = {}
        for (key,) in cursor:  # Returns list of tuples containing single value
            table_results[key] = []
        cursor.close()
        # Use dictionary cursor to get contents of table with columns as keys
        dict_cursor = cnx.cursor(dictionary=True)
        query = f"""SELECT * FROM {table}"""
        dict_cursor.execute(query)
        for row in dict_cursor:
            for key, value in row.items():
                table_results[key].append(value)
        dict_cursor.close()
        return table_results
