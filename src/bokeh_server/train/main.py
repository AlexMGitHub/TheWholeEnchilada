"""Return interface for selection of training options.

Columns:
    -   Features: Checkbox group of features to be used during training

    -   Model: Select machine learning model and training data split

    -   Hyperparameters: Set range of hyperparameters for grid search

    -   Train: Button to begin training and status update text.
"""

# %% Imports
# Standard system imports
from pathlib import Path
import pickle

# Related third party imports
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button, CheckboxGroup, Div, RangeSlider, Select, \
    Slider
import numpy as np
import pandas as pd

# Local application/library specific imports
from bokeh_server.train.twe_learn.train_model import train_model


# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
doc = curdoc()  # Must have reference to current document for multithreading

# Local data
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
data_cols = list(data.keys())
numeric_cols = [x for x in data_cols if type(data[x][0]) in (float, int)
                and x != target]
data_df = pd.DataFrame.from_dict(data)
X = data_df[numeric_cols]
y = data_df[target]

# Set heights, widths, and margin of columns
FEATURES_WIDTH = 200
MODEL_WIDTH = 300
HYPERPARAMS_WIDTH = 300
TRAIN_WIDTH = 400
MARGIN = 15
COL_HEIGHT = 500


# -----------------------------------------------------------------------------
# Features Column
# -----------------------------------------------------------------------------
features_title = Div(  # Title for features columns
    text="""
    <style>
        .bokeh_header {font-size: 30px; margin: auto;}
        .bokeh_title {border-bottom: 3px solid black;}
    </style>
    """
    f"""
    <div style="display: table; height: 50px; overflow: hidden;">
        <div style="display: table-cell; vertical-align: middle; width:
        {FEATURES_WIDTH}px; text-align: center;" class="bokeh_title">
            <h1 class="bokeh_header">Features</h1>
        </div>
    </div>""", height=50)
LABELS = numeric_cols
features_checkbox_group = CheckboxGroup(labels=LABELS,
                                        active=list(range(len(LABELS))))
features = column(features_title, features_checkbox_group,
                  width=FEATURES_WIDTH, height=COL_HEIGHT,
                  background="#e8e8e8")


# -----------------------------------------------------------------------------
# Model Column
# -----------------------------------------------------------------------------
model_title = Div(  # Title for model column
    text=f"""
    <div style="display: table; height: 50px; overflow: hidden;">
        <div style="display: table-cell; vertical-align: middle; width:
            {MODEL_WIDTH}px; text-align: center;" class="bokeh_title">
            <h1 class="bokeh_header">Model</h1>
        </div>
    </div>""", height=50)
if ml_type == 'classification':
    default_model = 'Logistic Regression'
    MODELS = ['Gradient Boosting CLF', 'K-Nearest Neighbors CLF',
              'Logistic Regression', 'Naive Bayes', 'Random Forest CLF',
              'SVC (linear kernel)', 'SVC (rbf kernel)']
elif ml_type == 'regression':
    default_model = 'Linear Regression'
    MODELS = ['Gradient Boosting REG', 'K-Nearest Neighbors REG',
              'Linear Regression', 'Lasso Regression', 'Ridge Regression',
              'Random Forest REG', 'SVR (linear kernel)',
              'SVR (rbf kernel)']

model_select = Select(title="Model Type:", value=default_model,
                      options=MODELS)
train_split_slider = Slider(start=0.05, end=0.95, value=0.80,
                            step=.05, title="Train Split", bar_color="#3FB8AF")
models = column(model_title, model_select, train_split_slider,
                width=MODEL_WIDTH, height=COL_HEIGHT, margin=(0, 0, 0, MARGIN),
                background="#e8e8e8")


# -----------------------------------------------------------------------------
# Hyperparameters Column
# -----------------------------------------------------------------------------
hp_title = Div(  # Title for hyperparameters column
    text=f"""
    <div style="display: table; height: 50px; overflow: hidden;">
        <div style="display: table-cell; vertical-align: middle; width:
        {HYPERPARAMS_WIDTH}px; text-align: center;" class="bokeh_title">
            <h1 class="bokeh_header">Hyperparameters</h1>
        </div>
    </div>""", height=50)
# Define default model
if ml_type == 'classification':
    clf_default = False
    reg_default = True
elif ml_type == 'regression':
    clf_default = True
    reg_default = False
# Define range sliders for hyperparameter
alpha_range_slider = RangeSlider(
    start=0.1, end=100.1, value=(0.1, 100.1), step=10, title="alpha",
    disabled=reg_default, bar_color='#3FB8AF', visible=not reg_default,
    name='alpha')
c_range_slider = RangeSlider(
    start=0.1, end=100.1, value=(0.1, 100.1), step=10, title="C",
    disabled=clf_default, bar_color='#3FB8AF', visible=not clf_default,
    name='C')
learning_rate_range_slider = RangeSlider(
    start=0.1, end=1, value=(0.1, 1), step=0.1, title="learning_rate",
    disabled=True, visible=False, name='learning_rate')
max_depth_range_slider = RangeSlider(
    start=3, end=10, value=(3, 10), step=1, title="max_depth",
    disabled=True, visible=False, name='max_depth')
n_estimators_range_slider = RangeSlider(
    start=50, end=250, value=(50, 250), step=50, title="n_estimators",
    disabled=True, visible=False, name='n_estimators')
n_neighbors_range_slider = RangeSlider(
    start=3, end=10, value=(3, 10), step=1, title="n_neighbors",
    disabled=True, visible=False, name='n_neighbors')
# Add hyperparameter title and range sliders to column
hp_sliders = (alpha_range_slider, c_range_slider, learning_rate_range_slider,
              max_depth_range_slider, n_estimators_range_slider,
              n_neighbors_range_slider)
hyperparams = column(hp_title, *hp_sliders,
                     width=HYPERPARAMS_WIDTH, height=COL_HEIGHT,
                     background="#e8e8e8",
                     margin=(0, MARGIN, 0, MARGIN))
# Dictionary cross-referencing model to applicable hyperparameter sliders
enabled_hp_sliders = {
    'Gradient Boosting CLF': [learning_rate_range_slider,
                              n_estimators_range_slider,
                              max_depth_range_slider],
    'Gradient Boosting REG': [learning_rate_range_slider,
                              n_estimators_range_slider,
                              max_depth_range_slider],
    'K-Nearest Neighbors CLF': [n_neighbors_range_slider],
    'K-Nearest Neighbors REG': [n_neighbors_range_slider],
    'Logistic Regression': [c_range_slider],
    'Linear Regression': [],
    'Lasso Regression': [alpha_range_slider],
    'Ridge Regression': [alpha_range_slider],
    'Naive Bayes': [],
    'Random Forest CLF': [n_estimators_range_slider, max_depth_range_slider],
    'Random Forest REG': [n_estimators_range_slider, max_depth_range_slider],
    'SVC (linear kernel)': [c_range_slider],
    'SVR (linear kernel)': [c_range_slider],
    'SVC (rbf kernel)': [c_range_slider],
    'SVR (rbf kernel)': [c_range_slider]
}


# -----------------------------------------------------------------------------
# Train Column
# -----------------------------------------------------------------------------
train_title = Div(  # Title for train column
    text=f"""
    <div style="display: table; height: 50px; overflow: hidden;">
        <div style="display: table-cell; vertical-align: middle; width:
        {TRAIN_WIDTH}px; text-align: center;" class="bokeh_title">
            <h1 class="bokeh_header">Train Model</h1>
        </div>
    </div>""", height=50)
# Define div to contain status information
status_div = Div(text="""<b>Ready to train...</b>""",
                 height=375)
# Define train button and add to column with title and status divs
train_button = Button(label="Train", button_type="primary")
train = column(train_title, status_div, train_button, width=TRAIN_WIDTH,
               height=COL_HEIGHT, background="#e8e8e8")


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------
def features_change(attrname, old, new):
    """Callback for features checkbox group."""
    if new == []:
        train_button.disabled = True
    else:
        train_button.disabled = False


def set_sliders(model):
    """Enable or disable hyperparameter sliders based on selected model."""
    for slider in hp_sliders:
        slider.disabled = True
        slider.visible = False
    for slider in enabled_hp_sliders[model]:
        slider.disabled = False
        slider.visible = True


def model_change(attrname, old, new):
    """Callback for model dropdown menu to change model type."""
    set_sliders(new)


def train_button_press(event):
    """Callback for when the Train button is pressed.

    Instantiates a thread to execute training while allowing callback to return
    a message indicating that training has commenced.

    Per documentation must schedule document updates via a next tick callback.
    """
    status_div.text = "<b>Beginning training...</b><br><br>"
    doc.add_next_tick_callback(run_training)


def run_training():
    """Fit machine learning pipeline based on selected parameters."""
    training_settings = {
        'dataset': dataset,
        'features': [LABELS[x] for x in features_checkbox_group.active],
        'model': model_select.value,
        'train_split': train_split_slider.value,
        'params': [(x.name, list(np.arange(x.value[0], x.value[1]+x.step,
                                           x.step)))
                   for x in enabled_hp_sliders[model_select.value]]
    }
    (params, train_score, test_score) = train_model(
        X[training_settings['features']], y, training_settings)
    text = '<b>Settings:</b><br>'
    for key, val in training_settings.items():
        text += f"{key}: {val}<br>"
    text += "<br><b>Results:</b><br>" + \
        str(params) + '<br>' + \
        f'<b>Train Score:</b> {train_score:.2f}' + '<br>' + \
        f'<b>Test Score:</b> {test_score:.2f}' + '<br>'
    status_div.text += text + "<br><b>Training complete!</b>"


features_checkbox_group.on_change('active', features_change)
model_select.on_change('value', model_change)
train_button.on_click(train_button_press)


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------
train_layout = row(features, models, hyperparams, train)
doc.add_root(train_layout)
