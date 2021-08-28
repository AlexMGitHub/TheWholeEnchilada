"""Return interface for selection of training options.

Columns:
    -   Features: Checkbox group of features to be used during training

    -   Model: Select machine learning model and training data split

    -   Hyperparameters: Set range of hyperparameters for grid search

    -   Train: Button to begin training and status update text.
"""

# %% Imports
# Standard system imports
import pandas as pd
from pathlib import Path
import threading
from time import sleep

# Related third party imports
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Button, CheckboxGroup, Div, RangeSlider, Select, \
    Slider

# Local application/library specific imports
from twe_learn.train_model import train_model

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
doc = curdoc()  # Must have reference to current document for multithreading


def pd_data(data_path):
    return pd.read_csv(data_path, header=None,
                       names=['sepal_width', 'sepal_length', 'petal_width',
                              'petal_length', 'class'])


# Local data
data_path = list(Path('src/bokeh_server/data/').glob('*.txt'))[0]
data_df = pd_data(data_path)
data_cols = list(data_df.columns)
data = data_df.to_dict('list')
numeric_cols = [x for x in data_cols
                if not x.endswith('_id') and type(data[x][0]) in (float, int)]
X = data_df[['sepal_width', 'sepal_length', 'petal_width', 'petal_length']]
y = data_df['class']

# Set heights, widths, and margin of columns
FEATURES_WIDTH = 200
MODEL_WIDTH = 300
HYPERPARAMS_WIDTH = 300
TRAIN_WIDTH = 400
MARGIN = 15
COL_HEIGHT = 400


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
MODELS = ['Gradient Boosting', 'K-Nearest Neighbors', 'Logistic Regression',
          'Naive Bayes', 'Random Forest', 'SVC (linear kernel)',
          'SVC (rbf kernel)']
model_select = Select(title="Model Type:", value='Logistic Regression',
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
# Define list of hyperparameters used by models
hp_list = ['C', 'max_depth', 'n_neighbors',
           'learning_rate', 'max_iter', 'n_estimators', 'n_neighbors']
c_steps = 'tbd'
# Define range sliders
c_range_slider = RangeSlider(
    start=0, end=100, value=(1, 90), step=10, title="C",
    disabled=False, bar_color='#3FB8AF', visible=True, name='C')
learning_rate_range_slider = RangeSlider(
    start=0, end=100, value=(1, 90), step=10, title="learning_rate",
    disabled=True, visible=False, name='learning_rate')
max_depth_range_slider = RangeSlider(
    start=0, end=100, value=(1, 90), step=10, title="max_depth",
    disabled=True, visible=False, name='max_depth')
max_iter_range_slider = RangeSlider(
    start=0, end=100, value=(1, 90), step=10, title="max_iter",
    disabled=True, visible=False, name='max_iter')
n_estimators_range_slider = RangeSlider(
    start=0, end=100, value=(1, 90), step=10, title="n_estimators",
    disabled=True, visible=False, name='n_estimators')
n_neighbors_range_slider = RangeSlider(
    start=0, end=100, value=(1, 90), step=10, title="n_neighbors",
    disabled=True, visible=False, name='n_neighbors')
# Add hyperparameter title and range sliders to column
hp_sliders = (c_range_slider, learning_rate_range_slider,
              max_depth_range_slider, max_iter_range_slider,
              n_estimators_range_slider, n_neighbors_range_slider)
hyperparams = column(hp_title, *hp_sliders,
                     width=HYPERPARAMS_WIDTH, height=COL_HEIGHT,
                     background="#e8e8e8",
                     margin=(0, MARGIN, 0, MARGIN))
# Dictionary cross-referencing model to applicable hyperparameter sliders
enabled_hp_sliders = {
    'Gradient Boosting': [learning_rate_range_slider,
                          n_estimators_range_slider, max_depth_range_slider],
    'K-Nearest Neighbors': [n_neighbors_range_slider],
    'Logistic Regression': [c_range_slider],
    'Naive Bayes': [],
    'Random Forest': [n_estimators_range_slider, max_depth_range_slider],
    'SVC (linear kernel)': [c_range_slider],
    'SVC (rbf kernel)': [c_range_slider]
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
                 height=250)
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
        'features': [LABELS[x] for x in features_checkbox_group.active],
        'model': model_select.value,
        'train_split': train_split_slider.value,
        'params': [(x.name, list(range(x.value[0], x.value[1], x.step)))
                   for x in enabled_hp_sliders[model_select.value]]
    }
    (text1, text2, text3) = train_model(
        X[training_settings['features']], y, training_settings)
    text = '<b>Settings:</b><br>'
    for key, val in training_settings.items():
        text += f"{key}: {val}<br>"
    text += "<br><b>Results:</b><br>" + \
        str(text1) + '<br>' + str(text2) + '<br>' + str(text3)
    status_div.text += text + "<br><br><b>Training complete!</b>"


features_checkbox_group.on_change('active', features_change)
model_select.on_change('value', model_change)
train_button.on_click(train_button_press)


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------
train_layout = row(features, models, hyperparams, train)
doc.add_root(train_layout)
