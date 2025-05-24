import polars as pl


def aggregate_data_daily(df: pl.DataFrame) -> pl.DataFrame:    
    """
    Aggregate electric sensor data to daily totals.

    This function extracts the date from a timestamp column and calculates the 
    daily sum of values (e.g., energy usage) for each day present in the data.

    Parameters
    ----------
    df : pl.DataFrame
        A Polars DataFrame containing at least the following columns:
        - 'timestamp': a Datetime column or string-convertible to Datetime
        - 'value': a numeric column representing energy or power usage

    Returns
    -------
    pl.DataFrame
        A DataFrame grouped by date with the total sum of 'value' per day.
        Contains the following columns:
        - 'date' : date extracted from the timestamp (type: Date)
        - 'daily_sum' : aggregated sum of 'value' per date (type: Int64 or Float64)
    """

    daily_agg = (
        df.with_columns(pl.col("timestamp").dt.date().alias("date"))
        .group_by("date")
        .agg(pl.col("value").sum().alias("daily_sum"))
        .sort("date")
    )

    return daily_agg