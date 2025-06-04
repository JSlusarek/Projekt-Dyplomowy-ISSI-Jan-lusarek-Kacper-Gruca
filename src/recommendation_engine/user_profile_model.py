import sys
import os
sys.path.append(os.path.abspath(os.path.join("../../")))
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def train_profile_model(df: str):

    # Define columns
    base_columns = ["cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost"]
    specific_columns = ["heating_quality", "cooking_quality", "computing_quality", "cooling_quality"]
    all_features = base_columns + specific_columns

    # Filter and prepare data
    df = df[all_features + ["profile", "optimal_device"]]
    df = df.dropna(subset=base_columns + ["profile"])

    # Train/test split
    X = df[all_features]
    y = df["profile"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    # Train classifier
    clf = HistGradientBoostingClassifier(random_state=42, max_iter=100)
    clf.fit(X_train, y_train)

    # Predict and report
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)

    return clf, y_pred, report
