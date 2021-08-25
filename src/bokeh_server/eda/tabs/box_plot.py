"""Return interactive box plot showing distribution of data per class.

Based on Bokeh boxplot.py gallery example available at:
https://docs.bokeh.org/en/latest/docs/gallery/boxplot.html
"""

# %% Imports
# Standard system imports

# Related third party imports
import numpy as np
import pandas as pd

# Local application/library specific imports
from bokeh.layouts import column
from bokeh.models import Select
from bokeh.plotting import figure


# %% Create box plot
def create_box_plot(data, metadata):
    """Create box plot for each numeric column in data."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    MAX_PLOT_SIZE = 400
    TARGET = metadata['target']
    df = pd.DataFrame(data)
    cats = list(np.unique(data[TARGET]))
    data_columns = [x for x in df.columns if x != TARGET]

    # find the quartiles and IQR for each category
    groups = df.groupby(TARGET)
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr

    # find the outliers for each category
    def outliers(group, col):
        cat = group.name
        return group[(group[col] > upper.loc[cat][col]) |
                     (group[col] < lower.loc[cat][col])][col]

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    def build_box_plot(data_column):
        out = groups.apply(outliers, data_column).dropna()

        # prepare outlier data for plotting, we need coordinates for every
        # outlier.
        if not out.empty:
            outx = list(out.index.get_level_values(0))
            outy = list(out.values)

        p = figure(tools="", background_fill_color="#efefef",
                   x_range=cats, toolbar_location=None,
                   output_backend="webgl",
                   sizing_mode='stretch_height',
                   max_width=MAX_PLOT_SIZE)

        # if no outliers, shrink lengths of stems to be no longer than the
        # minimums or maximums
        qmin = groups.quantile(q=0.00)
        qmax = groups.quantile(q=1.00)
        upper[data_column] = [min([x, y]) for (x, y) in zip(
            list(qmax.loc[:, data_column]), upper[data_column])]
        lower[data_column] = [max([x, y]) for (x, y) in zip(
            list(qmin.loc[:, data_column]), lower[data_column])]

        # stems
        p.segment(cats, upper[data_column], cats,
                  q3[data_column], line_color="black")
        p.segment(cats, lower[data_column], cats,
                  q1[data_column], line_color="black")

        # boxes
        p.vbar(cats, 0.7, q2[data_column], q3[data_column],
               fill_color="#E08E79", line_color="black")
        p.vbar(cats, 0.7, q1[data_column], q2[data_column],
               fill_color="#3B8686", line_color="black")

        # whiskers (almost-0 height rects simpler than segments)
        p.rect(cats, lower[data_column], 0.2, 0.01, line_color="black")
        p.rect(cats, upper[data_column], 0.2, 0.01, line_color="black")

        # outliers
        if not out.empty:
            p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = "white"
        p.grid.grid_line_width = 2
        p.xaxis.major_label_text_font_size = "1em"
        p.yaxis.axis_label = data_column
        p.axis.major_label_text_font_style = "bold"
        p.axis.axis_label_text_font_style = "bold"

        return p

    # -------------------------------------------------------------------------
    # Widgets
    # -------------------------------------------------------------------------
    selectdata = Select(title="Data Column:", value=data_columns[0],
                        options=data_columns, sizing_mode="stretch_width",
                        max_width=200)

    # -------------------------------------------------------------------------
    # Callbacks
    # -------------------------------------------------------------------------
    def selectdata_change(attrname, old, new):
        plot = build_box_plot(new)
        update(plot)

    def update(plot):
        box_layout.children[1] = plot

    selectdata.on_change('value', selectdata_change)

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------
    plot = build_box_plot(data_columns[0])
    box_layout = column(selectdata, plot)

    return box_layout
