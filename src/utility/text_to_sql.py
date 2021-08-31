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

    def __init__(self):
        """Define paths to Iris files."""
        iris = Path('/twe/src/app/static/datasets/iris')
        self.iris_sql = list((iris / 'sql').glob('*.sql'))[0]
        self.iris_template = list((iris / 'template').glob('*.sql'))[0]
        self.iris_data = list((iris / 'data').glob('*.txt'))[0]
        self.iris_desc = list((iris / 'desc').glob('*.txt'))[0]

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
        with open(self.iris_sql, 'w') as sql:
            with open(self.iris_template, 'r') as template_file:
                template = template_file.read()
            sql.write(template)
            with open(self.iris_data, 'r') as text_file:
                prev_line = text_file.readline()
                for idx, line in enumerate(text_file):
                    sql.write(self.format_iris_line(prev_line, idx+1))
                    prev_line = line
                sql.write(self.format_iris_line(line, idx+2, last_line=True))
        return self.iris_sql


class BostonSQL:
    """Class to convert the Boston dataset to an SQL file."""

    def __init__(self):
        """Define paths to Boston files."""
        boston = Path('/twe/src/app/static/datasets/boston')
        self.boston_sql = list((boston / 'sql').glob('*.sql'))[0]
        self.boston_template = list((boston / 'template').glob('*.sql'))[0]
        self.boston_data = list((boston / 'data').glob('*.txt'))[0]
        self.boston_desc = list((boston / 'desc').glob('*.txt'))[0]

    def format_boston_line(self, line, idx, last_line=False):
        """Reformat line from Boston text file as SQL-formatted values."""
        if last_line:
            punctuation = ';'       # Last line of query requires semi-colon
        else:
            punctuation = ',\n'     # Item in list requires comma and newline
        return f"({idx},{line.rstrip()}){punctuation}"

    def boston_to_sql(self):
        """Merge Boston SQL template with formatted text data."""
        with open(self.boston_sql, 'w') as sql:
            with open(self.boston_template, 'r') as template_file:
                template = template_file.read()
            sql.write(template)
            with open(self.boston_data, 'r') as text_file:
                prev_line = text_file.readline()
                for idx, line in enumerate(text_file):
                    sql.write(self.format_boston_line(prev_line, idx+1))
                    prev_line = line
                sql.write(self.format_boston_line(line, idx+2, last_line=True))
        return self.boston_sql


class WineSQL():
    """Class to convert the Wine dataset to an SQL file."""

    def __init__(self):
        """Define paths to Wine files."""
        wine = Path('src/app/static/datasets/wine')
        self.wine_sql = list((wine / 'sql').glob('*.sql'))[0]
        self.wine_template = list((wine / 'template').glob('*.sql'))[0]
        self.wine_data = list((wine / 'data').glob('*.txt'))[0]
        self.wine_desc = list((wine / 'desc').glob('*.txt'))[0]

    def format_wine_line(self, line, idx, last_line=False):
        """Reformat line from Wine text file as SQL-formatted values."""
        v = line.split(';')         # Split line using semicolon delimiter
        v[-1] = f"'{v[-1].rstrip()}'"  # Represent quality score as a string
        if last_line:
            punctuation = ';'       # Last line of query requires semi-colon
        else:
            punctuation = ',\n'     # Item in list requires comma and newline
        return f"({idx}, " + ', '.join(v).rstrip() + f"){punctuation}"

    def wine_to_sql(self):
        """Merge Wine SQL template with formatted text data."""
        with open(self.wine_sql, 'w') as sql:
            with open(self.wine_template, 'r') as template_file:
                template = template_file.read()
            sql.write(template)
            with open(self.wine_data, 'r') as text_file:
                prev_line = text_file.readline()
                for idx, line in enumerate(text_file):
                    sql.write(self.format_wine_line(prev_line, idx+1))
                    prev_line = line
                sql.write(self.format_wine_line(line, idx+2, last_line=True))
        return self.wine_sql


if __name__ == '__main__':
    wine = WineSQL()
    wine.wine_to_sql()
