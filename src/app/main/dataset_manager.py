"""Define classes used to manage datasets.

Classes:
    -   DatasetManager: Class to manage datasets available to user.
"""

# %% Imports
# Standard system imports
from pathlib import Path
import pickle

# Related third party imports

# Local application/library specific imports
from .. import db


# %% Dataset classes
class DatasetManager:
    """Class to manage datasets available to user."""

    def __init__(self, session):
        """Accept Flask session and initialize paths and metadata."""
        self.session = session
        self.datasets_path = Path('src/app/static/datasets')
        self.data_path = Path('src/bokeh_server/data/eda_data')
        self.train_data_path = Path('src/bokeh_server/data/train_data')
        self.metadata = {
            'iris': {
                'dataset': 'iris',
                'type': 'classification',
                'target': 'class'
            },
            'boston': {
                'dataset': 'boston',
                'type': 'regression',
                'target': 'CRIM'
            },
            'autompg': {
                'dataset': 'autompg',
                'type': 'regression',
                'target': 'mpg'
            },
            'wine': {
                'dataset': 'wine',
                'type': 'classification',
                'target': 'quality'
            }
        }

    def current_dataset(self):
        """Return currently selected dataset."""
        return self.session.get('dataset')

    def set_current_dataset(self, dataset):
        """Set session's dataset variable."""
        self.session['dataset'] = dataset

    def list_datasets_paths(self):
        """Return list of paths of available datasets."""
        return sorted(list(self.datasets_path.glob('*/')))

    def list_datasets_names(self):
        """Return list of names of available datasets."""
        datasets = self.list_datasets_paths()
        return [x.name for x in datasets]

    def list_loaded(self):
        """Return list of datasets loaded into MySQL database."""
        data_names = self.list_datasets_names()
        is_loaded = [db.query_table_exists(x) for x in data_names]
        return [name for name, loaded in zip(data_names, is_loaded) if loaded]

    def get_data(self, dataset):
        """Return dictionary containing MySQL table."""
        return db.get_table(dataset)

    def get_metadata(self, dataset):
        """Return metadata for dataset including summary statistics."""
        summary = self.get_summary(dataset)
        metadata = self.metadata[dataset]
        metadata['summary'] = summary
        return metadata

    def get_summary(self, dataset):
        """Return dictionary containing summary statistics of dataset."""
        return db.describe_table(dataset)

    def dump_data(self, dataset):
        """Pickle dataset data and metadata and write to Docker volume."""
        data = self.get_data(dataset)
        metadata = self.get_metadata(dataset)
        pickle_data = {'data': data, 'metadata': metadata}
        with open(self.data_path, 'wb') as data_file:
            pickle.dump(pickle_data, data_file)

    def build_datasets_table(self):
        """Return data needed to build table used by load_datasets() route."""
        app_path = Path('src/app')
        datasets = self.list_datasets_paths()
        idx = list(range(1, len(datasets)+1))
        data_paths = [list((dpath/'data').glob('*.*'))[0].
                      relative_to(app_path) for dpath in datasets]
        data_names = self.list_datasets_names()
        desc_paths = [list((dpath/'desc').glob('*.*'))[0].
                      relative_to(app_path) for dpath in datasets]
        descrips = [x.name for x in desc_paths]
        sql_paths = [list((dpath/'sql').glob('*.sql'))[0].
                     relative_to(app_path) for dpath in datasets]
        sql_names = [x.name for x in sql_paths]
        loaded = [db.query_table_exists(x) for x in data_names]
        table_size = [db.query_table_size(x) for x in data_names]
        loaded_names = [x for x, y in zip(data_names, loaded) if y]
        return idx, data_paths, data_names, desc_paths, descrips, sql_paths, \
            sql_names, loaded, table_size, loaded_names


if __name__ == '__main__':
    mgr = DatasetManager({'dataset': 'iris'})
    mgr.build_datasets_table()
