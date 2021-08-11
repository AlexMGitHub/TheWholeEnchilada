"""Solutions to exercises in Murach's MySQL.

###############################################################################
# murachs_mysql.py
#
# Revision:     1.00
# Date:         8/2/2021
# Author:       Alex
#
# Purpose:      Solutions to exercises from "Murach's MySQL", 3rd edition by
#               Joel Murach.
#
###############################################################################
"""

# %% Imports
# Standard system imports

# Related third party imports

# Local application/library specific imports


# %% Exercise solutions
def parse_sql_file(filename):
    """Parse .SQL file into a list containing SQL queries as strings."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    queries = ''.join(lines).split(';')     # Use ; to separate queries
    queries.pop()                           # Remove '' from end of list
    return queries


def chap3_solutions():
    """Read .SQL file containing solutions to chapter 3 exercises.

    Return the solutions as a list of SQL query strings.
    """
    filename = "/twe/src/murachs_mysql/sql/chapter3_exercises.sql"
    return parse_sql_file(filename)


def chap4_solutions():
    """Read .SQL file containing solutions to chapter 4 exercises.

    Return the solutions as a list of SQL query strings.
    """
    filename = "/twe/src/murachs_mysql/sql/chapter4_exercises.sql"
    return parse_sql_file(filename)


def chap5_solutions():
    """Read .SQL file containing solutions to chapter 5 exercises.

    Return the solutions as a list of SQL query strings.
    """
    filename = "/twe/src/murachs_mysql/sql/chapter5_exercises.sql"
    return parse_sql_file(filename)


def chap6_solutions():
    """Read .SQL file containing solutions to chapter 6 exercises.

    Return the solutions as a list of SQL query strings.
    """
    filename = "/twe/src/murachs_mysql/sql/chapter6_exercises.sql"
    return parse_sql_file(filename)


def chap7_solutions():
    """Read .SQL file containing solutions to chapter 7 exercises.

    Return the solutions as a list of SQL query strings.
    """
    filename = "/twe/src/murachs_mysql/sql/chapter7_exercises.sql"
    return parse_sql_file(filename)


def chap8_solutions():
    """Read .SQL file containing solutions to chapter 8 exercises.

    Return the solutions as a list of SQL query strings.
    """
    filename = "/twe/src/murachs_mysql/sql/chapter8_exercises.sql"
    return parse_sql_file(filename)


def chap9_solutions():
    """Read .SQL file containing solutions to chapter 9 exercises.

    Return the solutions as a list of SQL query strings.
    """
    filename = "/twe/src/murachs_mysql/sql/chapter9_exercises.sql"
    return parse_sql_file(filename)
