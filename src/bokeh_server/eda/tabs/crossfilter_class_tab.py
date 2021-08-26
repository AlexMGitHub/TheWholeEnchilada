"""Return tab containing a plot with selectable axes and marker properties.

Based on Bokeh crossfilter gallery example available at:
https://github.com/bokeh/bokeh/blob/master/examples/app/crossfilter

Modified for classification problems.

Plots:
    -   scatter_plot: Scatter plot of numeric data from dataset

Widgets:
    -   selectx: Select data plotted along the x-axis of scatter_plot

    -   selecty: Select data plotted along the y-axis of scatter_plot

    -   selectsize: Select data used to scale size of markers
"""

# %% Imports
# Standard system imports

# Related third party imports
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, Panel
from bokeh.palettes import Category10, Category20, Turbo256
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, factor_mark
import numpy as np
import pandas as pd

# Local application/library specific imports


# %% Define tab
def crossfilter_class_tab(data, numeric_cols, metadata, marker_order):
    """Return a plot with selectable axes and marker properties."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    # Define constants
    TARGET = metadata['target']
    CLASSES = list(np.unique(data[TARGET]))  # Classes in dataset
    MARKERS = [x for idx, x in enumerate(marker_order) if idx < len(CLASSES)]
    SIZES = list(range(6, 22, 3))  # Range of marker sizes
    N_SIZES = len(SIZES)
    DEFAULT_MARKER_SIZE = 12
    NUM_ROWS = len(data[numeric_cols[0]])  # Number of rows in dataset

    # Add marker size field to source
    source = ColumnDataSource(data)
    source.data["marker_sizes"] = [DEFAULT_MARKER_SIZE] * NUM_ROWS

    # Define color map and markers
    if len(CLASSES) <= 10:
        colors = Category10[len(CLASSES)]
    elif len(CLASSES) <= 20:
        colors = Category20[len(CLASSES)]
    else:
        color_idx = np.linspace(0, len(Turbo256), num=len(CLASSES),
                                endpoint=False, dtype=int)
        colors = [Turbo256[x] for x in color_idx]
    cmap = factor_cmap(TARGET, palette=colors, factors=CLASSES)
    markers = factor_mark(TARGET, markers=MARKERS, factors=CLASSES)

    # -------------------------------------------------------------------------
    # Widgets
    # -------------------------------------------------------------------------
    selectx = Select(title="X-Axis:", value=numeric_cols[0],
                     options=[numeric_cols[0]]+numeric_cols[2:],
                     sizing_mode="stretch_width")
    selecty = Select(title="Y-Axis:", value=numeric_cols[1],
                     options=numeric_cols[1:],
                     sizing_mode="stretch_width")
    selectsize = Select(title="Size", value='None',
                        options=['None']+numeric_cols[2:],
                        sizing_mode="stretch_width")

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    def create_plot(x, y):
        """Create Crossfilter scatter plot."""
        group_by_size()
        scatter_plot = figure(title=f'{y.title()} vs. {x.title()}',
                              height=800, width=1000,
                              sizing_mode="scale_width",
                              max_width=1000, output_backend="webgl",
                              background_fill_color="#DDDDDD",
                              outline_line_color="white",
                              toolbar_location="above")
        scatter_plot.scatter(x=x, y=y, color=cmap, source=source,
                             legend_field=TARGET, fill_alpha=0.4,
                             marker=markers, size='marker_sizes')
        # Style scatter plot
        scatter_plot.grid.grid_line_dash = [6, 4]
        scatter_plot.grid.grid_line_color = "white"
        scatter_plot.axis.major_label_text_font_size = "1em"
        scatter_plot.axis.major_label_text_font_style = "bold"
        scatter_plot.axis.axis_label_text_font_size = "1em"
        scatter_plot.axis.axis_label_text_font_style = "bold"
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
        scatter_plot.add_layout(scatter_plot.legend[0], 'right')
        # Add axis titles
        scatter_plot.xaxis.axis_label = x.title()
        scatter_plot.yaxis.axis_label = y.title()
        return scatter_plot

    # -------------------------------------------------------------------------
    # Callbacks
    # -------------------------------------------------------------------------
    def nix(vals, lst):
        """Return list omitting specified values."""
        return [x for x in lst if x not in vals]

    def group_by_size():
        """Define marker sizes according to selectsize dropdown menu."""
        if selectsize.value == 'None':
            source.data["marker_sizes"] = [DEFAULT_MARKER_SIZE] * NUM_ROWS
        else:
            groups = pd.qcut(data[selectsize.value], N_SIZES, labels=False)
            source.data["marker_sizes"] = [SIZES[x] for x in groups]

    def selectx_change(attrname, old, new):
        """Callback for selectx dropdown menu to change X-axis values."""
        selecty.options = nix([new], numeric_cols)
        selectsize.options = ['None'] + nix([new, selecty.value], numeric_cols)
        if selectsize.value not in selectsize.options:
            selectsize.value = 'None'
        plot = create_plot(new, selecty.value)
        plot.xaxis.axis_label = selectx.value
        update(plot)

    def selecty_change(attrname, old, new):
        """Callback for selecty dropdown menu to change Y-axis values."""
        selectx.options = nix([new], numeric_cols)
        selectsize.options = ['None'] + nix([new, selectx.value], numeric_cols)
        if selectsize.value not in selectsize.options:
            selectsize.value = 'None'
        plot = create_plot(selectx.value, new)
        plot.yaxis.axis_label = selecty.value
        update(plot)

    def selectsize_change(attrname, old, new):
        """Callback for selectsize dropdown menu to change size of markers."""
        plot = create_plot(selectx.value, selecty.value)
        update(plot)

    def update(plot):
        """Update layout with new Crossfilter scatterplot."""
        tab_layout.children[1] = plot

    selectx.on_change('value', selectx_change)
    selecty.on_change('value', selecty_change)
    selectsize.on_change('value', selectsize_change)

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------
    plot = create_plot(numeric_cols[0], numeric_cols[1])
    tab_layout = row(column(selectx, selecty, selectsize, sizing_mode="fixed",
                            height=250, width=200), plot)
    tab = Panel(child=tab_layout, title='Crossfilter')

    return tab
