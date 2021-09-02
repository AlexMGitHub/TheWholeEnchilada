"""Display classification results of trained model.

Results:
    -   actual_vs_pred: Scatter plot of predicted values vs. actual values

    -   resid_hist: Histogram of regression residuals

    -   resid_vs_pred_plot: Return plot containing residuals versus predictions
"""

# %% Imports
# Standard system imports
from pathlib import Path
import pickle

# Related third party imports
from bokeh.io import show
from bokeh.layouts import column, row
from bokeh.models.sources import ColumnDataSource
from bokeh.palettes import Category10
from bokeh.plotting import figure
from bokeh.models import DataTable, Div, Select, TableColumn
import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Local application/library specific imports


# %% Define globals
MAX_PLOT_SIZE = 400
COLOR = Category10[3][0]


# %% Define plots
def actual_vs_pred(y_true, y_pred, target):
    """Return scatterplot of actual vs. predicted values."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    # Define constants
    MARKER = 'circle'
    DEFAULT_MARKER_SIZE = 9
    # Define source
    source = ColumnDataSource({'y_pred': y_pred, 'y_true': y_true})

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    scatter_plot = figure(max_width=MAX_PLOT_SIZE, output_backend="webgl",
                          background_fill_color="#DDDDDD",
                          outline_line_color="white", toolbar_location='right',
                          width=MAX_PLOT_SIZE, sizing_mode="scale_width",
                          height=MAX_PLOT_SIZE)
    scatter_plot.scatter(x='y_pred', y='y_true', color=COLOR, source=source,
                         fill_alpha=0.4, marker=MARKER,
                         size=DEFAULT_MARKER_SIZE, legend_label=target)
    # Style scatter plot
    scatter_plot.grid.grid_line_dash = [6, 4]
    scatter_plot.grid.grid_line_color = "white"
    scatter_plot.axis.major_label_text_font_size = "1em"
    scatter_plot.axis.major_label_text_font_style = "bold"
    scatter_plot.axis.axis_label_text_font_size = "1em"
    scatter_plot.axis.axis_label_text_font_style = "bold"
    # Add title and axis labels
    scatter_plot.title = f'{target}: True vs. Predicted Values'
    scatter_plot.xaxis.axis_label = 'Predicted'
    scatter_plot.yaxis.axis_label = 'True'
    # Style legend
    scatter_plot.legend.background_fill_color = "#DDDDDD"
    scatter_plot.legend.border_line_color = "white"
    scatter_plot.legend.label_text_font_style = "bold"
    scatter_plot.legend.label_text_font_size = "1em"
    scatter_plot.legend.glyph_width = 30
    scatter_plot.legend.glyph_height = 30
    scatter_plot.legend.spacing = 0
    scatter_plot.legend.border_line_width = 2
    scatter_plot.legend.border_line_color = "black"
    scatter_plot.legend.padding = 5
    scatter_plot.legend.margin = 30
    scatter_plot.legend.label_standoff = 0
    scatter_plot.legend.location = "top_left"
    return scatter_plot


def resid_hist(y_true, y_pred, target):
    """Create a histogram plot of error residuals."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    residuals = y_true - y_pred

    hist_plot = figure(max_width=MAX_PLOT_SIZE, output_backend="webgl",
                       toolbar_location=None,
                       background_fill_color="#DDDDDD",
                       outline_line_color="white",
                       width=MAX_PLOT_SIZE, sizing_mode="scale_width",
                       height=MAX_PLOT_SIZE)
    hist, edges = np.histogram(residuals, density=True, bins='auto')
    hist_plot.quad(top=hist, bottom=0, left=edges[:-1],
                   right=edges[1:], fill_color=COLOR,
                   line_color="white", alpha=0.5, legend_label=target)
    hist_plot.y_range.start = 0
    # Style histogram
    hist_plot.grid.grid_line_dash = [6, 4]
    hist_plot.grid.grid_line_color = "white"
    hist_plot.axis.major_label_text_font_size = "1em"
    hist_plot.axis.major_label_text_font_style = "bold"
    hist_plot.axis.axis_label_text_font_size = "1em"
    hist_plot.axis.axis_label_text_font_style = "bold"
    # Add title and axis labels
    hist_plot.title = f"{target}: Residuals Histogram"
    hist_plot.xaxis.axis_label = 'Residuals'
    hist_plot.yaxis.axis_label = 'Density'
    # Disable and hide toolbar
    hist_plot.toolbar.active_drag = None
    hist_plot.toolbar.active_scroll = None
    hist_plot.toolbar.active_tap = None
    # Style legend
    hist_plot.legend.background_fill_color = "#DDDDDD"
    hist_plot.legend.border_line_color = "white"
    hist_plot.legend.label_text_font_style = "bold"
    hist_plot.legend.label_text_font_size = "1em"
    hist_plot.legend.glyph_width = 30
    hist_plot.legend.glyph_height = 30
    hist_plot.legend.spacing = 0
    hist_plot.legend.border_line_width = 2
    hist_plot.legend.border_line_color = "black"
    hist_plot.legend.padding = 5
    hist_plot.legend.margin = 30
    hist_plot.legend.label_standoff = 0
    hist_plot.legend.location = "top_left"
    return hist_plot


def resid_vs_pred_plot(y_true, y_pred, target):
    """Return plot containing residuals versus predictions."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    # Define constants
    MARKER = 'circle'
    DEFAULT_MARKER_SIZE = 9
    # Define source
    residuals = y_true - y_pred
    source = ColumnDataSource({'y_pred': y_pred, 'residuals': residuals})

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    scatter_plot = figure(max_width=MAX_PLOT_SIZE, output_backend="webgl",
                          background_fill_color="#DDDDDD",
                          outline_line_color="white",
                          toolbar_location='right',
                          width=MAX_PLOT_SIZE, sizing_mode="scale_width",
                          height=MAX_PLOT_SIZE)
    scatter_plot.scatter(x='y_pred', y='residuals', color=COLOR, source=source,
                         fill_alpha=0.4, marker=MARKER,
                         size=DEFAULT_MARKER_SIZE, legend_label=target)
    # Style scatter plot
    scatter_plot.grid.grid_line_dash = [6, 4]
    scatter_plot.grid.grid_line_color = "white"
    scatter_plot.axis.major_label_text_font_size = "1em"
    scatter_plot.axis.major_label_text_font_style = "bold"
    scatter_plot.axis.axis_label_text_font_size = "1em"
    scatter_plot.axis.axis_label_text_font_style = "bold"
    # Add title and axis labels
    scatter_plot.title = f"{target}: Residuals vs. Predictions"
    scatter_plot.xaxis.axis_label = 'Predicted'
    scatter_plot.yaxis.axis_label = 'Residuals'
    # Style legend
    scatter_plot.legend.background_fill_color = "#DDDDDD"
    scatter_plot.legend.border_line_color = "white"
    scatter_plot.legend.label_text_font_style = "bold"
    scatter_plot.legend.label_text_font_size = "1em"
    scatter_plot.legend.glyph_width = 30
    scatter_plot.legend.glyph_height = 30
    scatter_plot.legend.spacing = 0
    scatter_plot.legend.border_line_width = 2
    scatter_plot.legend.border_line_color = "black"
    scatter_plot.legend.padding = 5
    scatter_plot.legend.margin = 30
    scatter_plot.legend.label_standoff = 0
    scatter_plot.legend.location = "top_left"
    return scatter_plot


def regression_results():
    """Return table and plots of regression results using different metrics."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    # Load EDA data and metadata
    data_path = Path('src/bokeh_server/data/eda_data')
    with open(data_path, 'rb') as data_file:
        pickled_data = pickle.load(data_file)
    metadata = pickled_data['metadata']
    dataset = metadata['dataset']
    target = metadata['target']
    # Load model and training data
    model_filename = Path('src/bokeh_server/data/model')
    data_filename = Path('src/bokeh_server/data/train_data')
    model = joblib.load(model_filename)
    data = joblib.load(data_filename)
    training_settings = data['training_settings']
    X_train = data['X_train']
    X_test = data['X_test']
    y_train = data['y_train']
    y_test = data['y_test']
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    # Calculate error
    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    rmse_train = mean_squared_error(y_train, y_pred_train, squared=False)
    rmse_test = mean_squared_error(y_test, y_pred_test, squared=False)
    mae_train = mean_absolute_error(y_train, y_pred_train)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    # Create source
    results_dict = {
        'Metrics': ['MSE', 'RMSE', 'MAE', 'R\u00b2'],
        'Training Data': [round(mse_train, 2), round(rmse_train, 2),
                          round(mae_train, 2), round(r2_train, 2)],
        'Test Data': [round(mse_test, 2), round(rmse_test, 2),
                      round(mae_test, 2), round(r2_test, 2)]
    }
    source = ColumnDataSource(results_dict)
    # Layout parameters
    col_width = 300  # Results table width
    settings_width = 500  # Training settings div width

    # -------------------------------------------------------------------------
    # Data Table
    # -------------------------------------------------------------------------
    # Title for results table
    results_div = Div(
        text="""
        <style>
            .bokeh_header {font-size: 20px; margin: auto;}
            .bokeh_title {border-bottom: 3px solid black;}
        </style>
        """
        f"""
        <div style="display: table; height: 50px; overflow: hidden;">
            <div style="display: table-cell; vertical-align: middle;
            width: {col_width}px; text-align: center;" class="bokeh_title">
                <h1 class="bokeh_header">{dataset} Results</h1>
            </div>
        </div>""",
        height=50, width=225)
    # Data table containing results
    columns = [TableColumn(field=col, title=col) for col in results_dict]
    results_table = DataTable(
        source=source, columns=columns, sortable=False,
        sizing_mode="stretch_width", autosize_mode="fit_viewport",
        width=col_width, index_position=None, height=150)

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    avp = actual_vs_pred(y_test, y_pred_test, target)
    hist_plot = resid_hist(y_test, y_pred_test, target)
    rvp = resid_vs_pred_plot(y_test, y_pred_test, target)

    # -------------------------------------------------------------------------
    # Widgets
    # -------------------------------------------------------------------------
    select_data = Select(title="Train/Test Data:", value='Test',
                         options=['Test', 'Training'], width=100)

    # -------------------------------------------------------------------------
    # Callbacks
    # -------------------------------------------------------------------------
    def select_data_change(attrname, old, new):
        """Toggle test/train data for select_data dropdown menu."""
        if new == 'Training':
            avp = actual_vs_pred(y_train, y_pred_train, target)
            hist_plot = resid_hist(y_train, y_pred_train, target)
            rvp = resid_vs_pred_plot(y_train, y_pred_train, target)
        elif new == 'Test':
            avp = actual_vs_pred(y_test, y_pred_test, target)
            hist_plot = resid_hist(y_test, y_pred_test, target)
            rvp = resid_vs_pred_plot(y_test, y_pred_test, target)
        update(avp, hist_plot, rvp)

    def update(avp, hist_plot, rvp):
        """Update layout with new plots."""
        results_layout.children[0].children[1] = avp
        results_layout.children[1].children[0] = hist_plot
        results_layout.children[1].children[1] = rvp

    select_data.on_change('value', select_data_change)

    # -------------------------------------------------------------------------
    # Div Containing Settings
    # -------------------------------------------------------------------------
    # Create settings div title
    settings_div = Div(text="""
    <style>
        .bokeh_header2 {font-size: 30px; margin: auto;}
        .bokeh_title2 {border-bottom: 3px solid black;}
    </style>
    """f"""
    <div style="display: table; height: 50px; overflow: hidden;">
        <div style="display: table-cell; vertical-align: middle;
        width: {settings_width}px; text-align: center;" class="bokeh_title2">
            <h1 class="bokeh_header2">{dataset} Training Settings</h1>
        </div>
    </div>
    <div>
    """, height=50)
    # Add model params to div
    for key, value in training_settings.items():
        settings_div.text += f"<b>{key}:</b> {value}<br>"
    settings_div.text += f"""
    <br><b>Chosen Params:</b> {model.best_estimator_}</div>"""

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------
    results_layout = row(
        column(column(
            column(results_div, results_table),
            row(select_data, margin=(50, 0, 0, 300)), height=MAX_PLOT_SIZE),
            avp, margin=(0, 30, 0, 0)),
        column(hist_plot, rvp),
        column(settings_div, width=settings_width, margin=(0, 0, 0, 30))
    )

    return results_layout


if __name__ == '__main__':
    plot = regression_results()
    show(plot)
