"""Return table containing classification summary report."""

# %% Imports
# Standard system imports

# Related third party imports
from bokeh.layouts import column
from bokeh.models import DataTable, Div, TableColumn

# Local application/library specific imports


# %% Define report table
def create_report_table(data_df, source, title, col_width):
    """Create table containing classification report summary."""
    # Title for report table
    div_title = Div(
        text="""
        <style>
            .bokeh_header {font-size: 30px; margin: auto;}
            .bokeh_title {border-bottom: 3px solid black;}
        </style>
        """
        f"""
        <div style="display: table; height: 50px; overflow: hidden;">
            <div style="display: table-cell; vertical-align: middle;
            width: {col_width}px; text-align: center;" class="bokeh_title">
                <h1 class="bokeh_header">{title}</h1>
            </div>
        </div>""",
        height=50)
    # Data table containing report
    columns = [TableColumn(field=col, title=col) for col in data_df.columns]
    report_table = DataTable(
        source=source, columns=columns, sortable=False,
        sizing_mode="scale_height", autosize_mode="fit_viewport", width=380,
        index_position=None, height=200)

    return column(div_title, report_table)
