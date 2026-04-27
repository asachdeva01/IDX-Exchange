"""
Feature engineering helper functions.

Each function adds one or more derived columns to a DataFrame.
"""
import pandas as pd
import numpy as np


def add_market_condition(df: pd.DataFrame) -> pd.DataFrame:
    """Flag each transaction as Seller's or Buyer's Market based on price ratio.

    Seller's Market: sold at or above original asking price (priceratio >= 1.0).
    """
    df['market_condition'] = np.where(
        df['priceratio'] >= 1.0, "Seller's Market", "Buyer's Market"
    )
    print(f"Market condition: {df['market_condition'].value_counts().to_dict()}")
    return df


def add_price_reduction_flags(df: pd.DataFrame, list_col: str = 'ListPrice',
                               orig_col: str = 'OriginalListPrice') -> pd.DataFrame:
    """Flag whether a listing had a price reduction and compute the reduction amount."""
    df['price_reduction'] = df[orig_col] - df[list_col]
    df['was_reduced'] = (df[orig_col] > df[list_col]).astype(int)
    print(f"Was reduced: {df['was_reduced'].value_counts().to_dict()}")
    return df


def add_dom_buckets(df: pd.DataFrame) -> pd.DataFrame:
    """Segment DaysOnMarket into buckets for analysis."""
    df['dom_bucket'] = pd.cut(
        df['DaysOnMarket'],
        bins=[0, 7, 14, 30, 60, 90, float('inf')],
        labels=['0-7', '8-14', '15-30', '31-60', '61-90', '90+'],
        right=True
    )
    print(f"DOM buckets: {df['dom_bucket'].value_counts().sort_index().to_dict()}")
    return df


def add_timeline_durations(df: pd.DataFrame) -> pd.DataFrame:
    """Compute listing-to-contract and contract-to-close durations in days.

    - listing_to_contract_days: PurchaseContractDate - ListingContractDate
    - contract_to_close_days:   CloseDate - PurchaseContractDate

    Columns that don't exist are silently skipped.
    """
    added: list[str] = []

    if 'PurchaseContractDate' in df.columns and 'ListingContractDate' in df.columns:
        df['listing_to_contract_days'] = (
            pd.to_datetime(df['PurchaseContractDate'], errors='coerce')
            - pd.to_datetime(df['ListingContractDate'], errors='coerce')
        ).dt.days
        added.append('listing_to_contract_days')

    if 'CloseDate' in df.columns and 'PurchaseContractDate' in df.columns:
        df['contract_to_close_days'] = (
            pd.to_datetime(df['CloseDate'], errors='coerce')
            - pd.to_datetime(df['PurchaseContractDate'], errors='coerce')
        ).dt.days
        added.append('contract_to_close_days')

    for col in added:
        median_val = df[col].median()
        mean_val = df[col].mean()
        print(f"{col}: median={median_val:.0f} days, mean={mean_val:.1f} days")

    return df


def add_price_tiers(df: pd.DataFrame, price_col: str = 'ClosePrice') -> pd.DataFrame:
    """Segment transactions into price tiers."""
    df['price_tier'] = pd.cut(
        df[price_col],
        bins=[0, 300000, 500000, 750000, 1000000, 2000000, float('inf')],
        labels=['Under 300K', '300K-500K', '500K-750K', '750K-1M', '1M-2M', '2M+']
    )
    print(f"Price tiers: {df['price_tier'].value_counts().sort_index().to_dict()}")
    return df
