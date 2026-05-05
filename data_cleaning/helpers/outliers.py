"""
IQR-based outlier detection and filtering.

Implements the tiered approach: flag extreme values first, then optionally
produce a separate filtered analysis dataset rather than permanently
deleting records.
"""
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
    """Flag outliers for multiple columns and return a clean filtered copy.

    Two-stage filtering for the analysis-ready dataset:
        1. Business-rule filter — drop rows with invalid values
           (ClosePrice <= 0, LivingArea <= 0, DaysOnMarket < 0, NaN in any).
        2. IQR filter — drop rows outside Tukey bounds for each column.

    The original DataFrame gets outlier flag columns added in place.
    Returns a new DataFrame with both invalid and outlier rows removed.
    """
    for col in columns:
        df = flag_outliers(df, col, multiplier)

    # Stage 1: business-rule filter — invalid values that IQR may not catch
    business_rule_invalid = pd.Series(False, index=df.index)
    for col in columns:
        if col not in df.columns:
            continue
        series = df[col]
        if col == 'DaysOnMarket':
            business_rule_invalid |= series.isna() | (series < 0)
        else:
            business_rule_invalid |= series.isna() | (series <= 0)

    # Stage 2: IQR outlier filter
    flag_cols = [f"{col}_outlier" for col in columns]
    any_outlier = df[flag_cols].any(axis=1)

    drop_mask = business_rule_invalid | any_outlier
    filtered = df[~drop_mask].copy()

    print(f"\nOriginal rows:        {len(df):,}")
    print(f"  Invalid (rule):     {business_rule_invalid.sum():,}")
    print(f"  IQR outliers:       {any_outlier.sum():,}")
    print(f"  Combined removed:   {drop_mask.sum():,}")
    print(f"After filtering:      {len(filtered):,}")
    return filtered


def compare_before_after(
    df_before: pd.DataFrame,
    df_after: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Generate a side-by-side comparison of size and median values before
    and after outlier filtering.

    Returns a DataFrame with rows for each column showing the before/after
    median, mean, and overall row count change.
    """
    rows: list[dict] = []
    for col in columns:
        before = df_before[col].dropna()
        after = df_after[col].dropna()
        rows.append({
            'Column': col,
            'Median (Before)': round(before.median(), 2),
            'Median (After)': round(after.median(), 2),
            'Mean (Before)': round(before.mean(), 2),
            'Mean (After)': round(after.mean(), 2),
            'Max (Before)': round(before.max(), 2),
            'Max (After)': round(after.max(), 2),
        })

    comparison = pd.DataFrame(rows).set_index('Column')

    print("=" * 70)
    print(f"OUTLIER FILTERING — BEFORE/AFTER COMPARISON")
    print(f"  Rows before: {len(df_before):,}")
    print(f"  Rows after:  {len(df_after):,}")
    print(f"  Removed:     {len(df_before) - len(df_after):,} "
          f"({(len(df_before) - len(df_after)) / len(df_before) * 100:.2f}%)")
    print("=" * 70)
    print(comparison.to_string())

    return comparison
