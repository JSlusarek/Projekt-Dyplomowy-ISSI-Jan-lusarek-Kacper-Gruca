def validate_user_input(user_input: dict) -> dict:
    """
    Validates user input for preference-based profile prediction.

    Ensures required fields are present and within valid ranges:
    - Base features must be provided and in scale [-10 to 10] or [1 to 10].
    - Specific features are optional but must be in range [1 to 10] if provided.

    Parameters
    ----------
    user_input : dict
        Dictionary of user preferences in user scale.

    Returns
    -------
    dict
        Cleaned input if valid, otherwise raises ValueError.
    """

    required_base = ["cost_pln", "co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "device_cost"]
    optional_specific = ["heating_quality", "cooking_quality", "computing_quality", "cooling_quality"]

    validated = {}

    for feature in required_base:
        if feature not in user_input:
            raise ValueError(f"Missing required input: {feature}")
        val = user_input[feature]
        if feature == "device_cost":
            if not isinstance(val, (int, float)) or not -10 <= val <= 10:
                raise ValueError(f"{feature} must be in range [-10, 10]")
        else:
            if not isinstance(val, (int, float)) or not 0 <= val <= 10:
                raise ValueError(f"{feature} must be in range [0, 10]")
        validated[feature] = val

    for feature in optional_specific:
        if feature in user_input:
            val = user_input[feature]
            if val is not None:
                if not isinstance(val, (int, float)) or not 0 <= val <= 10:
                    raise ValueError(f"{feature} must be in range [0, 10] if provided")
                validated[feature] = val
            else:
                validated[feature] = None
        else:
            validated[feature] = None

    return validated
