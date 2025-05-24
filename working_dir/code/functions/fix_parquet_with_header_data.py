import polars as pl

def fix_parquet_with_header_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    Fix a Polars DataFrame where the first row of actual data was incorrectly used as column headers.

    This function assumes the current column names represent the first lost data row,
    restores that row, and renames the columns to ['timestamp', 'value']. It changes the
    format of the 'timestamp' column to a Polars Datetime type.

    Parameters
    ----------
    df : pl.DataFrame
        A Polars DataFrame where the first data row was incorrectly saved as column headers.

    Returns
    -------
    pl.DataFrame
        A corrected DataFrame with the lost row restored and columns renamed to ['timestamp', 'value'].
    """

    # Save original column names (contain real data)
    first_row_raw = df.columns

    # Rename columns to generic placeholders
    df.columns = [f"column_{i}" for i in range(len(df.columns))]

    # Convert string row to proper types
    parsed_row = [first_row_raw[0], int(first_row_raw[1])]

    # Create the lost data row with correct types
    header_row = pl.DataFrame([parsed_row], schema=df.columns, orient="row")

    # Concatenate the recovered row and actual data
    df_fixed = pl.concat([header_row, df])

    # Rename to final desired column names
    df_fixed.columns = ["timestamp", "value"]

    df_fixed = df_fixed.with_columns(
        pl.col("timestamp").str.strptime(pl.Datetime, format="%Y-%m-%d %H:%M:%S")
    )

    return df_fixed
