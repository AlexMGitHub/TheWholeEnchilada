"""Return plot of confusion matrix."""

# %% Imports
# Standard system imports

# Related third party imports
from bokeh.palettes import Inferno256
from bokeh.plotting import figure
import numpy as np
from sklearn.metrics import confusion_matrix

# Local application/library specific imports


# %% Define Confusion Matrix
def create_confusion_matrix(y_true, y_pred, title, col_width):
    """Return plot of confusion matrix."""
    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    train_cm = confusion_matrix(y_true, y_pred)
    train_cm_norm = confusion_matrix(y_true, y_pred, normalize='true')
    # Sklearn confusion matrix sorts class labels
    factors = sorted(list(np.unique(y_true)))
    # Build rows (y) and columns (x) of confusion matrix
    x = factors*len(factors)  # Columns of labels repeated every row
    y = [factor for factor in factors for f in factors]  # Rows of labels
    # Create color map for CM based on normalized CM matrix values
    cmap = [Inferno256[int(x*255)] for x in train_cm_norm.flatten()]
    # Invert color of text relative to background color of matrix cell
    text_cmap = ['#' + '{:06x}'.format(0xffffff - int(x[1:], 16))
                 for x in cmap]
    # Create text labels from un-normalized confusion matrix values
    text_vals = [x for x in train_cm.flatten()]

    # -------------------------------------------------------------------------
    # Confusion Matrix
    # -------------------------------------------------------------------------
    cm = figure(title=title, toolbar_location=None,
                x_range=factors, y_range=factors[::-1], width=col_width,
                height=col_width,
                x_axis_label="Predicted", y_axis_label="True",
                sizing_mode="stretch_width")
    cm.rect(x, y, color=cmap, width=1, height=1)
    cm.text(x, y, text=text_vals, text_color=text_cmap, text_align="center",
            y_offset=10)
    # Set label font size
    cm.xaxis.axis_label_text_font_size = "1em"
    cm.yaxis.axis_label_text_font_size = "1em"
    cm.xaxis.major_label_text_font_size = "1em"
    cm.yaxis.major_label_text_font_size = "1em"

    return cm
