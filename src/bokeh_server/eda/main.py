"""Create multi-tab visualization for exploratory data analysis.

Tabs:
    -   Summary: Table containing statistics, pie chart, interactive box plots.

    -   Crossfilter: Interactive scatterplot with adjustable axes.

    -   Gridplot: Matrix of scatterplots with histograms along diagonal.
"""

# %% Imports
# Standard system imports
import pickle
from pathlib import Path

# Related third party imports

# Local application/library specific imports
from bokeh.models import Tabs
from bokeh.plotting import curdoc
from bokeh_server.eda.tabs.crossfilter_tab import crossfilter_cls, \
    crossfilter_reg
from bokeh_server.eda.tabs.features_tab import feature_importance
from bokeh_server.eda.tabs.gridplot_tab import gridplot_cls, gridplot_reg
from bokeh_server.eda.tabs.summary_tab import summary_cls, summary_reg


# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
# Read pickled data contained in Docker volume
data_path = Path('src/bokeh_server/data/eda_data')
with open(data_path, 'rb') as data_file:
    pickled_data = pickle.load(data_file)
data = pickled_data['data']
metadata = pickled_data['metadata']
# Extract metadata
dataset = metadata['dataset']
ml_type = metadata['type']
target = metadata['target']
# Delete index column from data table and create lists of valid columns
id_col = dataset + '_id'
del data[id_col]
table_cols = list(data.keys())
numeric_cols = [x for x in table_cols if type(data[x][0]) in (float, int)]
# Bokeh scatter markers in order of preference
marker_order = ['circle', 'square', 'plus', 'star', 'triangle', 'diamond',
                'inverted_triangle',  'hex', 'circle_cross', 'diamond_cross',
                'square_cross', 'circle_dot', 'triangle_dot', 'diamond_dot',
                'square_dot', 'star_dot', 'hex_dot', 'triangle_pin',
                'square_pin', 'circle_x', 'square_x', 'circle_y', 'asterisk',
                'cross', 'dash', 'dot', 'x', 'y']


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------
tab2, top4_features = feature_importance(data, metadata, numeric_cols)
if ml_type == 'classification':
    tab1 = summary_cls(data, numeric_cols, metadata)
    tab3 = crossfilter_cls(data, numeric_cols, metadata, marker_order)
    tab4 = gridplot_cls(data, top4_features, metadata, marker_order)
elif ml_type == 'regression':
    tab1 = summary_reg(data, numeric_cols, metadata)
    tab3 = crossfilter_reg(data, numeric_cols, metadata, marker_order)
    tab4 = gridplot_reg(data, top4_features, metadata, marker_order)
final_layout = Tabs(tabs=[tab1, tab2, tab3, tab4])

curdoc().add_root(final_layout)
