"""Display results of trained model.

Results are displayed according to whether the dataset is a regression or a
classification problem.
"""

# %% Imports
# Standard system imports
from pathlib import Path
import pickle

# Related third party imports
from bokeh.io import curdoc

# Local application/library specific imports
from bokeh_server.results.plots.regression_results import regression_results
from bokeh_server.results.plots.classification_results \
    import classification_results


# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
data_path = Path('src/bokeh_server/data/eda_data')
with open(data_path, 'rb') as data_file:
    pickled_data = pickle.load(data_file)
metadata = pickled_data['metadata']
ml_type = metadata['type']


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------
if ml_type == 'classification':
    results_layout = classification_results()
elif ml_type == 'regression':
    results_layout = regression_results()
curdoc().add_root(results_layout)
