import sys
import os
sys.path.append(os.path.abspath(os.path.join("../../")))
import numpy as np
import pandas as pd
from src.recommendation_engine.validate_user_input import validate_user_input


def predict_profile_for_user(user_input: dict, model, feature_order: list):
    """
    Predicts the user's profile class based on their preferences scaled to model input format.

    Parameters
    ----------
    user_input : dict
        Dictionary containing user preferences. Expected value range:
        - For most features: 1 to 10
        - For `device_cost`: -10 to 10

        Example:
        {
            "cost_pln": 8,
            "co2_emission_kg": 5,
            "normalized_comfort": 6,
            "normalized_failure_rate": 3,
            "device_cost": -4,
            "cooking_quality": 9
        }

    model : sklearn.base.BaseEstimator
        Trained scikit-learn model (e.g., HistGradientBoostingClassifier) capable of predicting user profiles.

    feature_order : list of str
        Ordered list of features used during model training. Ensures the correct alignment of input features.

    Returns
    -------
    str
        Predicted user profile class label (e.g., "Saver", "EcoFriendly", "ComfortOriented").
    
    Raises
    ------
    ValueError
        If required inputs are missing or out of expected range.
    """

    def rescale(value, feature):
        if value is None:
            return None
        if feature == "device_cost":
            return np.clip(value / 10, -1, 1)       # -10 do 10
        return np.clip(value / 10, 0, 1)            # 1 do 10
    
    validated_user_input = validate_user_input(user_input)

    # scales the uscer input according to the expected order
    input_scaled = {
        feat: rescale(validated_user_input.get(feat, np.nan), feat)
        for feat in feature_order
    }

    df_input = pd.DataFrame([input_scaled])
    return model.predict(df_input)[0]
