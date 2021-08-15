"""Collection of classes to convert data in text files to SQL files.

Classes:
    -   IrisSQL: Class to convert the Iris dataset to an SQL file.
"""

# %% Imports
# Standard system imports
from pathlib import Path

# Related third party imports

# Local application/library specific imports


# %% Text to SQL classes
class IrisSQL:
    """Class to convert the Iris dataset to an SQL file."""

    def __init__(self, iris_text_fname):
        """Accept Iris text filename."""
        self.iris_text_fname = iris_text_fname

    def format_iris_line(self, line, idx, last_line=False):
        """Reformat line from Iris text file as SQL-formatted values."""
        v = line.split(',')         # Split line using comma delimiter
        if last_line:
            punctuation = ';'       # Last line of query requires semi-colon
        else:
            punctuation = ',\n'     # Item in list requires comma and newline
        return f"({idx}, {v[0]}, {v[1]}, {v[2]}, {v[3]}, "\
            f"'{v[4].rstrip()}'){punctuation}"

    def iris_to_sql(self):
        """Merge Iris SQL template with formatted text data."""
        db = Path('/twe/src/db')
        iris_text = db / 'text' / self.iris_text_fname
        iris_template = db / 'sql' / 'templates' / 'iris_template.sql'
        iris_sql = db / 'sql' / 'create_iris.sql'
        with open(iris_sql, 'w') as sql:
            with open(iris_template, 'r') as template_file:
                template = template_file.read()
            sql.write(template)
            with open(iris_text, 'r') as text_file:
                prev_line = text_file.readline()
                for idx, line in enumerate(text_file):
                    sql.write(self.format_iris_line(prev_line, idx+1))
                    prev_line = line
                sql.write(self.format_iris_line(line, idx+2, last_line=True))
        return iris_sql
