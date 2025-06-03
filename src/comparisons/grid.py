import pandas as pd
import numpy as np
import itertools
from joblib import Parallel, delayed
import sys
import os
sys.path.append(os.path.abspath(os.path.join("../")))
from src.comparisons.optimizer import find_optimal_device


def generate_weight_combinations(features, step=0.5):
    """
    Generate all valid combinations of weights for a given set of features.

    Each weight can take values in the range [-1, 1] with the specified step size.
    Only combinations where the sum of the absolute values of weights equals 1
    (i.e., normalized importance distribution) are retained.

    Parameters:
    -----------
    features : list of str
        List of feature names for which weights will be generated.
    step : float, optional (default=0.5)
        Step size for generating weight values between -1 and 1.

    Returns:
    --------
    list of tuples
        List of valid weight combinations (tuples of floats) that satisfy the constraint.
    """

    possible_weights = np.arange(-1, 1 + step, step)
    combinations = itertools.product(possible_weights, repeat=len(features))
    valid_combinations = [
        comb for comb in combinations if np.isclose(sum(abs(w) for w in comb), 1.0)
    ]
    return valid_combinations



def evaluate_combination(df, features, weights_tuple):
    """
    Evaluate a single weight configuration and identify the optimal device.

    Applies the given weight tuple to the specified feature columns in the DataFrame,
    computes a weighted score for each device, and selects the device with the highest score.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing device information and feature values.
    features : list of str
        List of feature column names to which weights will be applied.
    weights_tuple : tuple of float
        Tuple of weights (in the range [-1, 1]) corresponding to each feature.

    Returns:
    --------
    dict
        Dictionary containing:
        - weights assigned to each feature,
        - the name of the optimal device ('optimal_device'),
        - the corresponding score of that device ('optimal_score').
    """
    weights = dict(zip(features, weights_tuple))
    scored_df = find_optimal_device(df, weights)
    optimal_device = scored_df.iloc[0]['name']
    optimal_score = scored_df.iloc[0]['score']
    return {**weights, 'optimal_device': optimal_device, 'optimal_score': optimal_score}



def compute_all_combinations_parallel(df, features, step=0.5, n_jobs=-1):
    """
    Compute the optimal device for all valid combinations of feature weights in parallel.

    This function generates all normalized weight combinations using `generate_weight_combinations`,
    evaluates each combination using `evaluate_weight_configuration`, and collects results
    using parallel computation for speed.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with device data and relevant features.
    features : list of str
        List of feature column names for weight assignment.
    step : float, optional (default=0.5)
        Step size for generating possible weight values between -1 and 1.
    n_jobs : int, optional (default=-1)
        Number of parallel jobs to run. Use -1 to utilize all available CPUs.

    Returns:
    --------
    pd.DataFrame
        DataFrame where each row corresponds to a weight configuration,
        the selected optimal device, and its score.
    """

    weight_combinations = generate_weight_combinations(features, step)
    results = Parallel(n_jobs=n_jobs)(
        delayed(evaluate_combination)(df, features, weights_tuple) 
        for weights_tuple in weight_combinations
    )
    return pd.DataFrame(results)