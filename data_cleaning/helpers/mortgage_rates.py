"""
FRED Mortgage Rate Enrichment

Loads the MORTGAGE30US CSV (30-year fixed mortgage rate from the St. Louis
Federal Reserve), resamples from weekly to monthly averages, and merges
onto MLS transaction datasets using a year-month key.
"""
import pandas as pd
from pathlib import Path


def load_mortgage_rates(csv_path: str | Path) -> pd.DataFrame:
    """Load the FRED MORTGAGE30US CSV and resample weekly rates to monthly averages.

    Args:
        csv_path: Path to the MORTGAGE30US.csv file.

    Returns:
        DataFrame with columns ['year_month', 'rate_30yr_fixed'] where
        year_month is a pandas Period('M') and rate is the monthly average.
    """
    mortgage = pd.read_csv(csv_path, parse_dates=['observation_date'])
    mortgage.columns = ['date', 'rate_30yr_fixed']

    # Resample weekly rates to monthly averages
    mortgage['year_month'] = mortgage['date'].dt.to_period('M')
    mortgage_monthly = (
        mortgage
        .groupby('year_month')['rate_30yr_fixed']
        .mean()
        .reset_index()
    )

    print(f"Mortgage rates loaded: {len(mortgage_monthly)} months "
          f"({mortgage_monthly['year_month'].min()} to {mortgage_monthly['year_month'].max()})")
    return mortgage_monthly


def merge_mortgage_rates(
    df: pd.DataFrame,
    mortgage_monthly: pd.DataFrame,
    date_col: str
) -> pd.DataFrame:
    """Merge monthly mortgage rates onto an MLS dataset using a date column.

    Creates a year_month key from the specified date column, performs a left
    merge, and reports how many rows have null rates after the join.

    Args:
        df: MLS dataset (sold or listings).
        mortgage_monthly: Output of load_mortgage_rates().
        date_col: Name of the date column to key off (e.g., 'CloseDate', 'ListingContractDate').

    Returns:
        DataFrame with 'year_month' and 'rate_30yr_fixed' columns added.
    """
    df['year_month'] = pd.to_datetime(df[date_col]).dt.to_period('M')
    merged = df.merge(mortgage_monthly, on='year_month', how='left')

    null_count = merged['rate_30yr_fixed'].isnull().sum()
    print(f"Merged on {date_col}: {null_count:,} rows with null rate "
          f"({null_count / len(merged) * 100:.2f}%)")
    return merged
