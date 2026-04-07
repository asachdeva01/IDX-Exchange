import pandas as pd
import numpy as np


def iqr_bounds(series: pd.Series, multiplier: float = 1.5) -> tuple:
    """Calculate IQR-based lower and upper bounds for outlier detection.

    Returns (lower_bound, upper_bound).
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - multiplier * iqr, q3 + multiplier * iqr


def flag_outliers(df: pd.DataFrame, column: str, multiplier: float = 1.5) -> pd.DataFrame:
    """Add a boolean outlier flag column for the specified numeric field.

    Creates a new column named '{column}_outlier' that is True for values
    outside the IQR bounds. Does not remove any rows.
    """
    lower, upper = iqr_bounds(df[column].dropna(), multiplier)
    flag_col = f"{column}_outlier"
    df[flag_col] = (df[column] < lower) | (df[column] > upper)

    n_outliers = df[flag_col].sum()
    print(f"{column}: {n_outliers:,} outliers flagged "
          f"({n_outliers / len(df) * 100:.1f}%) — bounds [{lower:,.2f}, {upper:,.2f}]")
    return df


def filter_outliers(df: pd.DataFrame, columns: list, multiplier: float = 1.5) -> pd.DataFrame:
    """Flag outliers for multiple columns and return a filtered copy excluding flagged rows.

    The original DataFrame gets outlier flag columns added in place.
    Returns a new DataFrame with outlier rows removed.
    """
    for col in columns:
        df = flag_outliers(df, col, multiplier)

    flag_cols = [f"{col}_outlier" for col in columns]
    any_outlier = df[flag_cols].any(axis=1)

    filtered = df[~any_outlier].copy()
    print(f"\nOriginal rows: {len(df):,} | After filtering: {len(filtered):,} "
          f"| Removed: {any_outlier.sum():,}")
    return filtered
