import pandas as pd


def parse_sold_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse CloseDate and create year-month features for the sold dataset."""
    df['CloseDate'] = pd.to_datetime(df['CloseDate'], errors='coerce')
    df['sold_year'] = df['CloseDate'].dt.year
    df['sold_month'] = df['CloseDate'].dt.month
    df['sold_yrmo'] = df['sold_year'] * 100 + df['sold_month']

    print("Sold date range:", df['CloseDate'].min().date(), "to", df['CloseDate'].max().date())
    return df


def parse_listing_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse ListingContractDate and create year-month features for the listings dataset."""
    df['ListingContractDate'] = pd.to_datetime(df['ListingContractDate'], errors='coerce')
    df['list_year'] = df['ListingContractDate'].dt.year
    df['list_month'] = df['ListingContractDate'].dt.month
    df['list_yrmo'] = df['list_year'] * 100 + df['list_month']

    print("Listings date range:", df['ListingContractDate'].min().date(), "to", df['ListingContractDate'].max().date())
    return df
