import polars as pl
import duckdb
import numpy as np
from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../../")))

QUALITY_COLS = ["heating_quality", "cooling_quality", "cooking_quality", "computing_quality"]
DEST_COLS = ["co2_emission_kg", "cost_pln", "normalized_comfort", "normalized_failure_rate", "device_cost"]
ALL_WEIGHT_COLS = DEST_COLS + QUALITY_COLS


def load_and_merge_parquets(folder: Path) -> pl.DataFrame:
    """
    Function to load and merge all Parquet files in a given folder into a single DataFrame in Polars.
    Args:
        folder (Path): Path to the folder containing Parquet files.
    """

    con = duckdb.connect()
    query = f"""
    COPY (
        SELECT * FROM read_parquet('{str(folder)}/*.parquet', union_by_name=True)
    ) TO '{str(folder / "merged_grid.parquet")}' (FORMAT PARQUET);
    """
    con.execute(query)
    return pl.read_parquet(folder / "merged_grid.parquet")


def clean_data(df: pl.DataFrame) -> pl.DataFrame:
    """
    Function to clean the DataFrame by removing rows with invalid values in destination columns
    and stymulant columns, and negating certain numeric columns.
    Args:
        df (pl.DataFrame): Input DataFrame with raw data.
    """

    mask_wrong_dest = pl.any_horizontal([
        pl.col(c) > 0 for c in ["co2_emission_kg", "normalized_comfort", "normalized_failure_rate", "cost_pln"]
    ])
    mask_wrong_stymulant = pl.any_horizontal([
        pl.col(c).is_not_null() & (pl.col(c) < 0) for c in QUALITY_COLS
    ])
    df = df.filter(~mask_wrong_dest & ~mask_wrong_stymulant)

    exclude = set(QUALITY_COLS + ["device_cost"])
    numeric_cols = [
        col for col in df.columns if df.schema[col] in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]
    ]
    cols_to_negate = [col for col in numeric_cols if col not in exclude]

    return df.with_columns([
        pl.when(pl.col(col) != 0).then(-pl.col(col)).otherwise(pl.col(col)).alias(col)
        for col in cols_to_negate
    ])


def compute_abs_weights(df: pl.DataFrame) -> pl.DataFrame:
    """ Function to compute absolute weights for the specified columns in the DataFrame.
    It creates a new column 'abs_weights_list_clean' that contains a list of absolute values
    for the specified weight columns, ensuring that null values are handled correctly.
    Args:
        df (pl.DataFrame): Input DataFrame with raw data.
    """

    return df.with_columns([
        pl.concat_list([
            pl.when(pl.col(c).is_not_null()).then(pl.col(c).abs()) for c in ALL_WEIGHT_COLS
        ]).alias("abs_weights_list_clean")
    ])


def compute_balance_flag(df: pl.DataFrame) -> pl.DataFrame:
    """ Function to compute a balance flag for the DataFrame.
    It checks if all absolute weights in the 'abs_weights_list_clean' column are equal
    and creates a new boolean column 'is_balanced' indicating whether the weights are balanced.
    Args:
        df (pl.DataFrame): Input DataFrame with absolute weights.
    """

    vectors = df["abs_weights_list_clean"].to_list()
    vectors = [[v for v in vec if v is not None] for vec in vectors]
    is_balanced = np.array([
        np.all(np.array(vec) == vec[0]) if len(vec) > 0 else False for vec in vectors
    ])
    return df.with_columns([
        pl.Series(name="is_balanced", values=is_balanced)
    ])


def unique_param_expr(not_null_counts) -> pl.Expr:
    """ Function to create an expression that determines the unique parameter based on not null counts.
    It checks which of the quality columns has a non-null value when exactly one of them is not null.
    Args:
        not_null_counts (pl.Expr): Expression representing the count of non-null values across quality columns.
    """

    return (
        pl.when(not_null_counts == 1)
        .then(
            pl.when(pl.col("heating_quality").is_not_null()).then(pl.lit("heating_quality"))
            .when(pl.col("cooling_quality").is_not_null()).then(pl.lit("cooling_quality"))
            .when(pl.col("cooking_quality").is_not_null()).then(pl.lit("cooking_quality"))
            .when(pl.col("computing_quality").is_not_null()).then(pl.lit("computing_quality"))
        )
    )


def enrich_with_stats(df: pl.DataFrame) -> pl.DataFrame:
    """ Function to enrich the DataFrame with statistical features.
    It computes the unique parameter, maximum quality value, absolute device cost,
    and maximum absolute weight for each row.
    Args:
        df (pl.DataFrame): Input DataFrame with raw data.
    """

    not_null_counts = pl.sum_horizontal([
        pl.col(c).is_not_null().cast(pl.Int8) for c in QUALITY_COLS
    ])
    return df.with_columns([
        unique_param_expr(not_null_counts).alias("unique_parameter"),
        pl.max_horizontal([pl.col(c) for c in QUALITY_COLS]).alias("max_quality_value"),
        pl.col("device_cost").abs().alias("abs_device_cost"),
        pl.max_horizontal([pl.col(c).abs() for c in ALL_WEIGHT_COLS]).alias("max_abs_weight")
    ])


def assign_profile(df: pl.DataFrame) -> pl.DataFrame:
    """ Function to assign user profiles based on the computed statistics.
    It creates a new column 'profile' that categorizes each row into a specific user profile
    based on the balance flag and the maximum absolute weight.
    Args:
        df (pl.DataFrame): Input DataFrame with enriched statistics.
    """

    return df.with_columns([
        pl.when(pl.col("is_balanced")).then(pl.lit("Balanced"))
        .when((~pl.col("is_balanced")) & (pl.col("max_quality_value") == pl.col("max_abs_weight")) & (pl.col("max_quality_value") > 0)).then(pl.lit("QualitySeeker"))
        .when((~pl.col("is_balanced")) & (pl.col("device_cost") > 0) & (pl.col("abs_device_cost") == pl.col("max_abs_weight"))).then(pl.lit("Bourgeois"))
        .when((~pl.col("is_balanced")) & (pl.col("device_cost") < 0) & (pl.col("abs_device_cost") == pl.col("max_abs_weight"))).then(pl.lit("Budget"))
        .when((~pl.col("is_balanced")) & (pl.col("co2_emission_kg").abs() == pl.col("max_abs_weight"))).then(pl.lit("EcoFriendly"))
        .when((~pl.col("is_balanced")) & (pl.col("cost_pln").abs() == pl.col("max_abs_weight"))).then(pl.lit("Saver"))
        .when((~pl.col("is_balanced")) & (pl.col("normalized_comfort").abs() == pl.col("max_abs_weight"))).then(pl.lit("ComfortSeeker"))
        .when((~pl.col("is_balanced")) & (pl.col("normalized_failure_rate").abs() == pl.col("max_abs_weight"))).then(pl.lit("RiskAware"))
        .otherwise(pl.lit("Unknown")).alias("profile")
    ])


def main():
    folder = Path("../../DATA/GRID").expanduser()
    print("Merging Parquets......")
    df_raw = load_and_merge_parquets(folder)
    print("Successfully merged Parquets!")
    print("Cleaning data......")
    df_clean = clean_data(df_raw)
    print("Data cleaned successfully!")
    print("Computing absolute weights......")
    df_weights = compute_abs_weights(df_clean)
    print("Absolute weights computed successfully!")
    print("Computing balance flag......")
    df_flagged = compute_balance_flag(df_weights)
    print("Balance flag computed successfully!")
    print("Enriching with statistics......")
    df_stats = enrich_with_stats(df_flagged)
    print("Statistics enriched successfully!")
    print("Assigning user profiles......")
    df_final = assign_profile(df_stats)
    print("User profiles assigned successfully!")
    print("Finalizing DataFrame......")
    df_final = df_final.drop(["abs_weights_list_clean", "is_balanced", "max_quality_value", "abs_device_cost", "max_abs_weight"])
    print("Final DataFrame ready!")
    df_final.write_parquet(folder / "grid_user_profile.parquet")
    print(f'************Correctly saved file grid_user_profile.parquet to: {folder}***************')


if __name__ == "__main__":
    main()
