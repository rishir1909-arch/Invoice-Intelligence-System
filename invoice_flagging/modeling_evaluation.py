from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, f1_score


def train_random_forest(X_train, y_train):
    """
    Train Random Forest using GridSearchCV.
    """
    rf = RandomForestClassifier(
        random_state=42,
        n_jobs=-1,
    )

    # Reduced grid (faster)
    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 5],
        "min_samples_split": [2],
        "min_samples_leaf": [1, 2],
        "criterion": ["gini"]
    }

    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        scoring="f1",
        cv=3,
        n_jobs=-1,
        verbose=2
    )

    grid_search.fit(X_train, y_train)
    return grid_search


def evaluate_classifier(model, X_test, y_test, model_name):
    """
    Evaluate classification model.
    """
    preds = model.predict(X_test)

    accuracy = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    report = classification_report(y_test, preds)

    print(f"\n{model_name} Performance")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"F1 Score: {f1:.2f}")
    print(report)