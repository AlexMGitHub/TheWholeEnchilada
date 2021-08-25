"""Return pie chart showing class distribution of dataset.

Based on Bokeh pie chart gallery example available at:
https://docs.bokeh.org/en/latest/docs/gallery/pie_chart.html
"""

# %% Imports
# Standard system imports
from math import pi

# Related third party imports
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10, Category20, Turbo256
from bokeh.plotting import figure
from bokeh.transform import cumsum
import numpy as np

# Local application/library specific imports


# %% Create pie chart
def create_pie_chart(data, metadata):
    """Create pie chart plot."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    TARGET = metadata['target']
    CLASSES = list(np.unique(data[TARGET]))
    COUNTS = [data[TARGET].count(x) for x in CLASSES]
    pie_total = sum(COUNTS)
    angle = [(2*pi*cnt)/pie_total for cnt in COUNTS]

    # Define color map and markers
    if len(CLASSES) <= 10:
        colors = Category10[len(CLASSES)]
    elif len(CLASSES) <= 20:
        colors = Category20[len(CLASSES)]
    else:
        color_idx = np.linspace(0, len(Turbo256), num=len(CLASSES),
                                endpoint=False, dtype=int)
        colors = [Turbo256[x] for x in color_idx]

    # Define plot source
    source = ColumnDataSource({'angle': angle, 'color': colors,
                               'classes': CLASSES, 'counts': COUNTS})

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    p = figure(plot_height=350, title="Class Distribution",
               toolbar_location=None, tools="hover",
               tooltips="@classes: @counts", x_range=(-0.5, 1.0),
               output_backend="webgl", sizing_mode="scale_both")

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True),
            end_angle=cumsum('angle'), line_color="white", fill_color='color',
            legend_field='classes', source=source)

    # Style plot
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.outline_line_color = "#DDDDDD"
    p.outline_line_width = 0
    # Style legend
    p.legend.label_text_font_style = "bold"
    p.legend.border_line_color = "#DDDDDD"
    p.legend.border_line_width = 0

    return p
