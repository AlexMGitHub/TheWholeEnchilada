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
import pandas as pd

# Local application/library specific imports
from bokeh.io import show
from bokeh.models import ColumnDataSource, Tabs
from bokeh.plotting import curdoc
from bokeh_server.eda.tabs.crossfilter_class_tab import crossfilter_class_tab
from bokeh_server.eda.tabs.summary_tab import summary_tab
from bokeh_server.eda.tabs.gridplot_tab import gridplot_tab


# %% Setup
def read_data(data_path):
    """Unpickle and return data generated by Flask webapp."""
    with open(data_path, 'rb') as data_file:
        return pickle.load(data_file)


def pd_data(data_path):
    return pd.read_csv(data_path, header=None,
                       names=['sepal_width', 'sepal_length', 'petal_width',
                              'petal_length', 'class'])


# Docker data
data_path = list(Path('src/bokeh_server/data/').glob('*.data'))[0]
data = read_data(data_path)
metadata = data['metadata']
dataset = metadata['dataset']
table = data['table']
# Delete index column
id_col = dataset + '_id'
del table[id_col]
table_cols = list(table.keys())
ml_type = metadata['type']
target = metadata['target']

numeric_cols = [x for x in table_cols if type(table[x][0]) in (float, int)]

# Bokeh scatter markers in order of preference
marker_order = ['circle', 'square', 'plus', 'star', 'triangle', 'diamond',
                'inverted_triangle',  'hex', 'circle_cross', 'diamond_cross',
                'square_cross', 'circle_dot', 'triangle_dot', 'diamond_dot',
                'square_dot', 'star_dot', 'hex_dot', 'triangle_pin',
                'square_pin', 'circle_x', 'square_x', 'circle_y', 'asterisk',
                'cross', 'dash', 'dot', 'x', 'y']


"""
# Local data
data_path = list(Path('src/bokeh_server/data/').glob('*.txt'))[0]
data_df = pd_data(data_path)
data_cols = list(data_df.columns)
data = data_df.to_dict('list')
summary_list = [{'column': 'petal_length', 'data_type': 'double', 'count': 150, 'avg': 3.7580000000000027, 'std': 1.759404065775303, 'min': 1.0, 'max': 6.9, '25%': 1.6, '50%': 4.35, '75%': 5.1}, {'column': 'petal_width', 'data_type': 'double', 'count': 150, 'avg': 1.199333333333334, 'std': 0.7596926279021596, 'min': 0.1, 'max': 2.5, '25%': 0.3, '50%': 1.3, '75%': 1.8}, {
    'column': 'sepal_length', 'data_type': 'double', 'count': 150, 'avg': 5.843333333333335, 'std': 0.8253012917851417, 'min': 4.3, 'max': 7.9, '25%': 5.1, '50%': 5.8, '75%': 6.4}, {'column': 'sepal_width', 'data_type': 'double', 'count': 150, 'avg': 3.057333333333334, 'std': 0.4344109677354942, 'min': 2.0, 'max': 4.4, '25%': 2.8, '50%': 3.0, '75%': 3.3}]

numeric_cols = [x for x in data_cols
                if not x.endswith('_id') and type(data[x][0]) in (float, int)]


source = ColumnDataSource(data)
# Bokeh scatter markers in order of preference
marker_order = ['circle', 'square', 'plus', 'star', 'triangle', 'diamond',
                'inverted_triangle',  'hex', 'circle_cross', 'diamond_cross',
                'square_cross', 'circle_dot', 'triangle_dot', 'diamond_dot',
                'square_dot', 'star_dot', 'hex_dot', 'triangle_pin',
                'square_pin', 'circle_x', 'square_x', 'circle_y', 'asterisk',
                'cross', 'dash', 'dot', 'x', 'y']

# Temp
metadata = {
    'dataset': 'iris',
    'type': 'classification',
            'target': 'class'
}
"""
# %% Layout
tab1 = summary_tab(table, numeric_cols, metadata)
tab2 = crossfilter_class_tab(table, numeric_cols, metadata, marker_order)
tab3 = gridplot_tab(table, numeric_cols, metadata, marker_order)
final_layout = Tabs(tabs=[tab1, tab2, tab3])
# Local
#curdoc().theme = Theme(filename='src/bokeh_server/eda/theme2.yaml')
# show(final_layout)
# Server
curdoc().add_root(final_layout)