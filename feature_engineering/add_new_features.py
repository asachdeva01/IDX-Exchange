"""
Feature Engineering Entry Point

Adds all derived features to the sold and listings datasets.
Designed to be run standalone or imported by the EDA notebook.
"""
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from helpers.engineer_features import (
    add_market_condition,
    add_price_reduction_flags,
    add_dom_buckets,
    add_price_tiers,
)


def engineer_sold_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all feature engineering steps to the sold dataset."""
    print("--- Sold Data Features ---")
    df = add_market_condition(df)
    df = add_price_reduction_flags(df)
    df = add_dom_buckets(df)
    df = add_price_tiers(df, price_col='ClosePrice')
    return df


def engineer_listing_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all feature engineering steps to the listings dataset."""
    print("--- Listings Data Features ---")
    df = add_price_reduction_flags(df)
    df = add_price_tiers(df, price_col='ListPrice')
    return df
