"""Train model on data according to provided hyperparameters.

Performs grid search and saves grid search estimator and settings to volume.
"""

# %% Imports
# Standard system imports
from pathlib import Path

# Related third party imports
import joblib
import numpy as np
# Import models
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, SVC
# Preprocessing, model selection, pipeline, metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Local application/library specific imports


# %% Train model
def train_model(X, y, training_settings):
    """Train model and save estimator to volume."""
    # Model selection
    if training_settings['model'] == 'Gradient Boosting':
        model = GradientBoostingClassifier
    elif training_settings['model'] == 'K-Nearest Neighbors':
        model = KNeighborsClassifier
    elif training_settings['model'] == 'Logistic Regression':
        model = LogisticRegression
    elif training_settings['model'] == 'Naive Bayes':
        model = GaussianNB
    elif training_settings['model'] == 'Random Forest':
        model = RandomForestClassifier
    elif training_settings['model'] == 'SVC (linear kernel)':
        model = LinearSVC
    elif training_settings['model'] == 'SVC (rbf kernel)':
        model = SVC
    # Define hyperparameters used for GridSearch
    param_grid = {f'model__{x[0]}': x[1] for x in training_settings['params']}
    # Define pipeline
    estimators = [('scale', StandardScaler()),
                  ('model', model())
                  ]
    pipe = Pipeline(estimators)
    # Split data into train and test sets
    train_size = training_settings['train_split']
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        train_size=train_size,
                                                        random_state=214)
    # Perform grid search
    grid_search = GridSearchCV(pipe, param_grid=param_grid, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    # Save model and data to volume using joblib
    model_filename = Path('src/bokeh_server/data/model')
    data_filename = Path('src/bokeh_server/data/train_data')
    with open(model_filename, 'wb') as model_file:
        joblib.dump(grid_search, model_file)
    with open(data_filename, 'wb') as data_file:
        joblib.dump({'X_train': X_train,
                     'X_test': X_test,
                     'y_train': y_train,
                     'y_test': y_test,
                     'training_settings': training_settings
                     }, data_file)

    return grid_search.best_params_, grid_search.score(X_train, y_train), \
        grid_search.score(X_test, y_test)
