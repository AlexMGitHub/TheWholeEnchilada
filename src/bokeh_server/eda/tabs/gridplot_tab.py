"""Return tab containing a grid of plots.

Plots:
    -   grid: A scatterplot matrix of every pair-wise combination of numeric
              data.  Diagonal entries are plotted as histograms.
"""

# %% Imports
# Standard system imports

# Related third party imports
from bokeh.layouts import gridplot, row as bokeh_row
from bokeh.models import ColumnDataSource, Legend, LegendItem, Panel
from bokeh.palettes import Category10, Category20, Turbo256
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, factor_mark
import numpy as np

# Local application/library specific imports


# %% Define tab
def gridplot_tab(data, numeric_cols, metadata, marker_order):
    """Return a gridplot containing every pair-wise combination of data."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    # Define constants
    TARGET = metadata['target']
    CLASSES = list(np.unique(data[TARGET]))
    MARKERS = [x for idx, x in enumerate(marker_order) if idx < len(CLASSES)]
    DEFAULT_MARKER_SIZE = 9
    MAX_SIZE = 1000  # Maximum width of gridplot
    MAX_PLOT_SIZE = MAX_SIZE // len(numeric_cols)  # Max width of subplots

    # Define color map and markers
    if len(numeric_cols) <= 10:
        colors = Category10[len(CLASSES)]
    elif len(numeric_cols) <= 20:
        colors = Category20[len(CLASSES)]
    else:
        color_idx = np.linspace(0, len(Turbo256), num=len(CLASSES),
                                endpoint=False, dtype=int)
        colors = [Turbo256[x] for x in color_idx]
    cmap = factor_cmap(TARGET, palette=colors, factors=CLASSES)
    markers = factor_mark(TARGET, markers=MARKERS, factors=CLASSES)

    source = ColumnDataSource(data)

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    def create_plot(x, y):
        """Create a scatterplot of x and y data with class hue semantic."""
        scatter_plot = figure(max_width=MAX_PLOT_SIZE, output_backend="webgl",
                              toolbar_location=None,
                              background_fill_color="#DDDDDD",
                              outline_line_color="white")
        scatter_plot.scatter(x=x, y=y, color=cmap, source=source,
                             fill_alpha=0.4, marker=markers,
                             size=DEFAULT_MARKER_SIZE)
        # Style scatter plot
        scatter_plot.grid.grid_line_dash = [6, 4]
        scatter_plot.grid.grid_line_color = "white"
        # Add axis titles
        scatter_plot.xaxis.axis_label = x.title()
        scatter_plot.yaxis.axis_label = y.title()
        # Disable and hide toolbar
        scatter_plot.toolbar.active_drag = None
        scatter_plot.toolbar.active_scroll = None
        scatter_plot.toolbar.active_tap = None
        return scatter_plot

    def create_histogram(field):
        """Create a histogram plot with class hue semantic."""
        hist_plot = figure(max_width=MAX_PLOT_SIZE, output_backend="webgl",
                           toolbar_location=None,
                           background_fill_color="#DDDDDD",
                           outline_line_color="white")
        for idx, data_class in enumerate(CLASSES):
            color = colors[idx]
            ungrouped_data = data[field]
            ungrouped_classes = data[TARGET]
            grouped = [ungrouped_data[x] for x in range(len(ungrouped_data))
                       if ungrouped_classes[x] == data_class]
            hist, edges = np.histogram(grouped, density=True, bins='auto')
            hist_plot.quad(top=hist, bottom=0, left=edges[:-1],
                           right=edges[1:], fill_color=color,
                           line_color="white", alpha=0.5)
            hist_plot.y_range.start = 0
        # Style histogram
        hist_plot.grid.grid_line_dash = [6, 4]
        hist_plot.grid.grid_line_color = "white"
        # Add axis titles
        hist_plot.xaxis.axis_label = field.title()
        hist_plot.yaxis.axis_label = field.title()
        # Disable and hide toolbar
        hist_plot.toolbar.active_drag = None
        hist_plot.toolbar.active_scroll = None
        hist_plot.toolbar.active_tap = None
        return hist_plot

    def create_blank_plot():
        """Hack to produce a legend outside of the grid plot."""
        p = figure(sizing_mode='stretch_height', width=250,
                   toolbar_location=None, output_backend="webgl")
        legenditem_list = []
        for idx, data_class in enumerate(CLASSES):
            color = colors[idx]
            marker = MARKERS[idx]
            r = p.scatter(color=color, source=source,
                          fill_alpha=0.4, marker=marker,
                          size=DEFAULT_MARKER_SIZE)
            legenditem_list.append(LegendItem(label=data_class, renderers=[r]))
        # Add and style legend
        legend = Legend(items=legenditem_list)
        p.add_layout(legend, 'left')
        p.legend.background_fill_color = "#DDDDDD"
        p.legend.border_line_color = "white"
        p.legend.label_text_font_style = "bold"
        p.legend.label_text_font_size = "1em"
        p.legend.glyph_width = 30
        p.legend.glyph_height = 30
        p.legend.spacing = 0
        p.legend.border_line_width = 2
        p.legend.border_line_color = "black"
        p.legend.padding = 5
        p.legend.margin = 30
        p.legend.label_standoff = 0

        # Style blank plot
        p.outline_line_width = 0
        # Disable and hide toolbar
        p.toolbar.active_drag = None
        p.toolbar.active_scroll = None
        p.toolbar.active_tap = None
        return p

    # Create grid plot
    grid_layout = []
    for ridx, row in enumerate(numeric_cols):
        grid_row = []
        for cidx, col in enumerate(numeric_cols):
            if ridx == cidx:
                grid_row.append(create_histogram(row))
            else:
                grid_row.append(create_plot(col, row))
        grid_layout.append(grid_row)

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------
    blank_plot = create_blank_plot()
    grid = gridplot(grid_layout, sizing_mode='scale_width',
                    toolbar_location=None)
    test = bokeh_row(grid, blank_plot)
    tab = Panel(child=test, title='Grid Plot')

    return tab
