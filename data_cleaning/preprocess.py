"""
Data Cleaning & Preprocessing Pipeline

Loads the raw sold and listings datasets and applies all cleaning steps:
1. Drop duplicate columns from API extraction
2. Parse date fields and create year-month features
3. Generate missing value reports

This script is designed to be run standalone or imported by the EDA notebook.
"""
import pandas as pd

from data_cleaning.helpers.duplicates import drop_duplicate_columns
from data_cleaning.helpers.dates import parse_sold_dates, parse_listing_dates
from data_cleaning.helpers.missing import missing_value_report


def preprocess_sold(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning steps to the sold transactions dataset."""
    df = parse_sold_dates(df)
    sold_missing = missing_value_report(df, "Sold Transactions")
    return df


def preprocess_listings(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning steps to the listings dataset."""
    df = drop_duplicate_columns(df)
    df = parse_listing_dates(df)
    list_missing = missing_value_report(df, "New Listings")
    return df


if __name__ == "__main__":
    # Standalone execution expects CSVs in the current working directory
    sold = pd.read_csv('priceratio.csv', encoding='ISO-8859-1')
    listings = pd.read_csv('newlistings.csv', encoding='ISO-8859-1')

    print(f"Sold transactions: {sold.shape[0]:,} rows x {sold.shape[1]} columns")
    print(f"New listings:      {listings.shape[0]:,} rows x {listings.shape[1]} columns")
    print()

    sold = preprocess_sold(sold)
    print()
    listings = preprocess_listings(listings)
