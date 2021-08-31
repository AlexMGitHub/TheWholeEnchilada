"""Display results of trained model.

Results:
    -   Training report: Table containing results on training data

    -   Test report: Table containing results on test data

    -   Training CM: Confusion matrix on training data

    -   Test CM: Confusion matrix on test data
"""

# %% Imports
# Standard system imports
from pathlib import Path

# Related third party imports
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div
import joblib
import pandas as pd
from sklearn.metrics import classification_report

# Local application/library specific imports
from bokeh_server.results.plots.confusion_matrix import create_confusion_matrix
from bokeh_server.results.plots.report_table import create_report_table


# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------
# Load data and model from volume
model_filename = Path('src/bokeh_server/data/model')
data_filename = Path('src/bokeh_server/data/train_data')
model = joblib.load(model_filename)
data = joblib.load(data_filename)
X_train = data['X_train']
X_test = data['X_test']
y_train = data['y_train']
y_test = data['y_test']
training_settings = data['training_settings']
dataset = training_settings['dataset']
# Classification report on training data
y_pred_train = model.predict(X_train)
train_report = classification_report(y_train, y_pred_train, output_dict=True,
                                     zero_division=0)
train_df = pd.DataFrame(train_report).transpose()
train_df.reset_index(inplace=True)  # Add index as a column to dataframe
train_df = train_df.round(2)  # Round values to two decimal places
train_source = ColumnDataSource(train_df)
# Classification report on test data
y_pred_test = model.predict(X_test)
test_report = classification_report(y_test, y_pred_test, output_dict=True,
                                    zero_division=0)
test_df = pd.DataFrame(test_report).transpose()
test_df.reset_index(inplace=True)  # Add index as a column to dataframe
test_df = test_df.round(2)  # Round values to two decimal places
test_source = ColumnDataSource(test_df)
# Layout constants
COL_WIDTH = 500
MARGIN = 30


# -----------------------------------------------------------------------------
# Data Tables
# -----------------------------------------------------------------------------
train_report = create_report_table(train_df, train_source,
                                   "Training Data Report", COL_WIDTH)
test_report = create_report_table(test_df, test_source,
                                  "Test Data Report", COL_WIDTH)


# -----------------------------------------------------------------------------
# Confusion Matrices
# -----------------------------------------------------------------------------
train_cm = create_confusion_matrix(y_train, y_pred_train,
                                   "Training Data Confusion Matrix", COL_WIDTH)

test_cm = create_confusion_matrix(y_test, y_pred_test,
                                  "Test Data Confusion Matrix", COL_WIDTH)


# -----------------------------------------------------------------------------
# Div Containing Settings
# -----------------------------------------------------------------------------
# Create settings div title
settings_div = Div(text="""
        <style>
            .bokeh_header {font-size: 30px; margin: auto;}
            .bokeh_title {border-bottom: 3px solid black;}
        </style>
        """f"""
        <div style="display: table; height: 50px; overflow: hidden;">
            <div style="display: table-cell; vertical-align: middle;
            width: {3*COL_WIDTH}px; text-align: center;" class="bokeh_title">
                <h1 class="bokeh_header"><b>{dataset}</b> Training Settings</h1>
            </div>
        </div>
        <div>
        """, height=50)
# Add model params to div
for key, value in training_settings.items():
    settings_div.text += f"<b>{key}:</b> {value}<br>"
settings_div.text += f"""
<br><b>Chosen Params:</b> {model.best_estimator_}</div>"""


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------
results_layout = column(
    row(column(train_report, test_report),
        column(train_cm, margin=(0, MARGIN, 0, MARGIN), width=COL_WIDTH),
        column(test_cm)),
    settings_div)

curdoc().add_root(results_layout)
