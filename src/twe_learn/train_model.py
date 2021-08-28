import numpy as np

# Import models
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC, SVC

# Scaling
from sklearn.preprocessing import StandardScaler

# Splitter and GridSearch
from sklearn.model_selection import train_test_split, GridSearchCV

# Pipeline
from sklearn.pipeline import Pipeline

# Metrics
from sklearn.metrics import accuracy_score


def train_model(X, y, training_settings):
    """"""
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

    # print(grid_search.cv_results_)
    print(grid_search.best_estimator_)
    print(grid_search.best_score_)
    print(grid_search.best_params_)
    print(grid_search.score(X_test, y_test))
    return grid_search.best_params_, grid_search.best_score_, grid_search.score(X_test, y_test)
