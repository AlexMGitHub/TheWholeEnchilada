"""Return tab containing various summaries of data.

Plots:
    -   pie_chart: A pie chart of the class distribution of the data.

    -   box_plots: An interactive box plot chart for numeric data columns.

Widgets:
    -   div_spacer: Add space between rows and columns of layout

Data Tables:
    -   summary_table: Contains summary statistics for numeric data columns

    -   data_table: Contains all rows and columns of dataset
"""

# %% Imports
# Standard system imports

# Related third party imports
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Div, Panel

# Local application/library specific imports
from bokeh_server.eda.tabs.box_plot import create_box_plot
from bokeh_server.eda.tabs.data_tables import data_tables
from bokeh_server.eda.tabs.pie_chart import create_pie_chart


# %% Define tab
def summary_tab(data, numeric_cols, metadata):
    """Return data tables summarizing dataset."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    source = ColumnDataSource(data)
    summary_list = metadata['summary']
    dataset_name = metadata['dataset']
    MARGIN = 30  # Layout margin

    # -------------------------------------------------------------------------
    # Data Tables
    # -------------------------------------------------------------------------
    summary_table, data_table = data_tables(data, numeric_cols, source,
                                            summary_list, dataset_name,
                                            metadata)

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    pie_chart = create_pie_chart(data, metadata, MARGIN)
    box_plots = create_box_plot(data, metadata)

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------
    tab_layout = row(column(box_plots, pie_chart),
                     column(summary_table, data_table))

    tab = Panel(child=tab_layout, title='Summary')

    return tab
