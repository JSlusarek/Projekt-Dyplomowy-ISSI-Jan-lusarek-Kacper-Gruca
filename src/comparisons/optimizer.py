import pandas as pd


def find_optimal_device(df, weights):
    """
    Finds the optimal device based on weighted scores of different criteria.

    Parameters:
        df (pd.DataFrame): The DataFrame from compare_water_boiling_devices.
        weights (dict): Mapping from column names to their respective weights. Weights must sum to 1.

    Returns:
        pd.DataFrame: Original DataFrame with an added 'score' column, sorted descending by score.
    """
    if not abs(sum(abs(w) for w in weights.values()) - 1.0) < 1e-6:
        raise ValueError("Absolute sum of weights must be 1.0")


    df = df.copy()
    df["score"] = 0.0
    for col, weight in weights.items():
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max > col_min:
            normalized = (df[col] - col_min) / (col_max - col_min)
        else:
            normalized = 0
        df["score"] += normalized * weight
    return df.sort_values(by="score", ascending=False).reset_index(drop=True)
