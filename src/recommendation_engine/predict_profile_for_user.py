import sys
import os
sys.path.append(os.path.abspath(os.path.join("../../")))
import numpy as np
import pandas as pd
from src.recommendation_engine.validate_user_input import validate_user_input

""" 
def predict_profile_for_user(user_input: dict, model, feature_order: list):
    

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
    return model.predict(df_input)[0],model.predict(df_input)[1]


"""

import numpy as np
import pandas as pd

def predict_profile_for_user(user_input: dict, model, feature_order: list):
    """ 
    Predicts the user's profile class based on their preferences scaled to model input format. 

    Returns the most probable and second-most probable class.
    """

    def rescale(value, feature):
        if value is None:
            return None
        if feature == "device_cost":
            return np.clip(value / 10, -1, 1)  # -10 to 10
        return np.clip(value / 10, 0, 1)       # 1 to 10

    validated_user_input = validate_user_input(user_input)

    # scale and align
    input_scaled = {
        feat: rescale(validated_user_input.get(feat, np.nan), feat)
        for feat in feature_order
    }

    df_input = pd.DataFrame([input_scaled])

    # predict probabilities
    proba = model.predict_proba(df_input)[0]
    class_indices_sorted = np.argsort(proba)[::-1]  # descending sort

    top1_idx = class_indices_sorted[0]
    top2_idx = class_indices_sorted[1]

    top1_class = model.classes_[top1_idx]
    top2_class = model.classes_[top2_idx]

    return top1_class, top2_class
