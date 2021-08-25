"""Return data tables.

Widgets:
    -   summary_title: Div containing title of summary_table

    -   summary_table: Contains summary statistics for numeric data columns

    -   data_title: Div containing title of data_table

    -   data_table: Contains all rows and columns of dataset
"""

# %% Imports
# Standard system imports

# Related third party imports
from bokeh.models import ColumnDataSource, DataTable, TableColumn, Div
from bokeh.layouts import column

# Local application/library specific imports


# %% Define tables
def data_tables(data, data_cols, source, summary_list, dataset_name, metadata):
    """Return data tables summarizing dataset."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    # Parse summary dictionary and use it to create a ColumnDataSource
    row_labels = ['Data Type', 'Count', 'Mean', 'STD', 'Min', '25%',
                  '50%', '75%', 'Max']
    summary = {'row_labels': row_labels}
    summary_cols = [TableColumn(field='row_labels', title='Column')]
    for col_dict in summary_list:
        summary_cols.append(TableColumn(field=col_dict['column'],
                                        title=col_dict['column'],
                                        width=len(col_dict['column'])))
        summary[col_dict['column']] = [
            col_dict['data_type'],
            col_dict['count'],
            round(col_dict['avg'], 2),
            round(col_dict['std'], 2),
            round(col_dict['min'], 2),
            round(col_dict['25%'], 2),
            round(col_dict['50%'], 2),
            round(col_dict['75%'], 2),
            round(col_dict['max'], 2)
        ]
    summary_source = ColumnDataSource(summary)

    # -------------------------------------------------------------------------
    # Widgets
    # -------------------------------------------------------------------------
    # Title for summary table
    summary_title = Div(
        text="""
        <div style="display: table; height: 50px; overflow: hidden;">
            <div style="display: table-cell; vertical-align: middle;">
                <h1 class="bokeh_header">Summary Statistics</h1>
            </div>
        </div>""",
        height=50)

    # Summary table of statistics
    summary_table = DataTable(
        source=summary_source, columns=summary_cols, index_position=None,
        sizing_mode='stretch_width', height=275, autosize_mode="fit_viewport")

    # Title for data table
    data_title = Div(
        text="""
        <style>
            .bokeh_header {font-size: 30px; margin: auto;}
        </style>
        """
        f"""
        <div style="display: table; height: 50px; overflow: hidden;">
            <div style="display: table-cell; vertical-align: middle;">
                <h1 class="bokeh_header">{dataset_name} data</h1>
            </div>
        </div>""",
        height=50)

    # Data table containing all rows and columns of dataset
    columns = [TableColumn(field=col, title=col) for col in data.keys()]
    data_table = DataTable(
        source=source, columns=columns, sortable=True,
        sizing_mode='stretch_width', autosize_mode="fit_viewport")

    return column(summary_title, summary_table), column(data_title, data_table)
