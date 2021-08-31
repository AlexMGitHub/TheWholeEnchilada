"""Return tab containing mutual information and PCA plots.

Plots:
    -   mi_plot: A horizontal bar plot of MI scores in descending order.

    -   pca_plot: A line graph of the cumulative sum of explained variance.
"""

# %% Imports
# Standard system imports
from pathlib import Path
import pickle

# Related third party imports
from bokeh.io import show
from bokeh.layouts import row
from bokeh.models import Panel
from bokeh.palettes import Category10, Category20, Turbo256
from bokeh.plotting import figure
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Local application/library specific imports


# %% Define tab
def feature_importance(data, metadata):
    """Return plots describing importance of data features."""
    # -------------------------------------------------------------------------
    # Functions
    # -------------------------------------------------------------------------
    def make_mi_scores(X, y):
        """From Ryan Holbrook's feature engineering course on Kaggle."""
        disc_feats = X.dtypes == int
        mi_scores = mutual_info_classif(X, y, discrete_features=disc_feats)
        mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
        mi_scores = mi_scores.sort_values(ascending=True)
        return mi_scores

    def make_pca_components(X_scaled):
        """Fit PCA to scaled data and calculate cumulative variance."""
        # Scale data
        scaler = StandardScaler()
        X_scaled_arr = scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled_arr, columns=X.columns)
        # Create principal components
        pca = PCA()
        pca.fit(X_scaled)
        # Cumulative variance will begin at 0% for zero components
        components = list(range(pca.n_components_ + 1))  # +1 for zeroth comp
        evr = pca.explained_variance_ratio_  # Explained variance
        cum_var = np.cumsum(np.insert(evr, 0, 0))  # Insert zero variance
        return cum_var, components

    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------
    target = metadata['target']
    dataset = metadata['dataset']
    data_df = pd.DataFrame.from_dict(data)
    X = data_df.drop(columns=[target])
    y = data_df[target]
    # Calculate mutual information
    mi_scores = make_mi_scores(X, y)
    features = list(mi_scores.index)
    scores = list(mi_scores.values)
    # Calculate PCA components
    cum_var, components = make_pca_components(X)
    # Define plot colors
    if len(features) <= 10:
        colors = Category10[len(features)]
    elif len(features) <= 20:
        colors = Category20[len(features)]
    else:
        color_idx = np.linspace(0, len(Turbo256), num=len(features),
                                endpoint=False, dtype=int)
        colors = [Turbo256[x] for x in color_idx]
    # Set layout constants
    MARGIN = 30
    PLOT_WIDTH = 600
    PLOT_HEIGHT = 600

    # -------------------------------------------------------------------------
    # Plots
    # -------------------------------------------------------------------------
    # Define Mutual Information plot
    mi_plot = figure(y_range=features, background_fill_color="#DDDDDD",
                     output_backend="webgl", toolbar_location=None, tools="",
                     title='Mutual Information Scores for '
                     f'{dataset} dataset (target={target})',
                     width=PLOT_HEIGHT, height=PLOT_WIDTH,
                     margin=(0, MARGIN, 0, 0),
                     sizing_mode="scale_height")
    mi_plot.hbar(y=features, right=scores, height=0.8, color=colors)
    # Style MI plot
    mi_plot.grid.grid_line_dash = [6, 4]
    mi_plot.grid.grid_line_color = "white"
    mi_plot.axis.major_label_text_font_size = "1em"
    mi_plot.axis.major_label_text_font_style = "bold"
    mi_plot.axis.axis_label_text_font_size = "1em"
    mi_plot.axis.axis_label_text_font_style = "bold"
    mi_plot.title.text_font_size = "1em"
    mi_plot.title.text_font_style = "bold"
    mi_plot.xaxis.axis_label = "MI Score"

    # Define PCA plot
    pca_plot = figure(background_fill_color="#DDDDDD",
                      output_backend="webgl", toolbar_location=None, tools="",
                      title='PCA Cumulative Explained Variance Percentage for '
                      f'{dataset} dataset', width=PLOT_WIDTH,
                      height=PLOT_HEIGHT, sizing_mode="scale_height")
    pca_plot.line(x=components, y=cum_var, line_width=2)
    pca_plot.circle(x=components, y=cum_var, size=10)
    # Style PCA plot
    pca_plot.grid.grid_line_dash = [6, 4]
    pca_plot.grid.grid_line_color = "white"
    pca_plot.axis.major_label_text_font_size = "1em"
    pca_plot.axis.major_label_text_font_style = "bold"
    pca_plot.axis.axis_label_text_font_size = "1em"
    pca_plot.axis.axis_label_text_font_style = "bold"
    pca_plot.title.text_font_size = "1em"
    pca_plot.title.text_font_style = "bold"
    pca_plot.xaxis.axis_label = "Component Number"

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------
    tab_layout = row(mi_plot, pca_plot, width=2*PLOT_WIDTH+MARGIN)
    tab = Panel(child=tab_layout, title='Feature Importance')
    return tab, features[-4:]  # Four most important features


if __name__ == '__main__':
    data_path = Path('src/bokeh_server/data/eda_data')
    with open(data_path, 'rb') as data_file:
        pickled_data = pickle.load(data_file)
    data = pickled_data['data']
    metadata = pickled_data['metadata']
    dataset = metadata['dataset']
    id_col = dataset + '_id'
    del data[id_col]
    tab = feature_importance(data, metadata)
    show(tab.child)
