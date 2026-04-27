"""
Date parsing and consistency validation helpers.
"""
import pandas as pd


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------

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


def parse_all_date_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all transaction date fields to datetime.

    Handles: CloseDate, PurchaseContractDate, ListingContractDate,
    ContractStatusChangeDate. Silently skips columns that don't exist.
    """
    date_cols: list[str] = [
        'CloseDate', 'PurchaseContractDate',
        'ListingContractDate', 'ContractStatusChangeDate',
    ]
    parsed: list[str] = []
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            parsed.append(col)

    print(f"Parsed {len(parsed)} date columns: {parsed}")
    return df


# ---------------------------------------------------------------------------
# Date consistency flags
# ---------------------------------------------------------------------------

def add_date_consistency_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Flag records where date fields violate logical ordering.

    Expected order: ListingContractDate < PurchaseContractDate < CloseDate.

    Creates boolean flag columns:
        - listing_after_close_flag:  ListingContractDate > CloseDate
        - purchase_after_close_flag: PurchaseContractDate > CloseDate
        - negative_timeline_flag:    any of the above is True
    """
    flags_added: list[str] = []

    if 'ListingContractDate' in df.columns and 'CloseDate' in df.columns:
        df['listing_after_close_flag'] = df['ListingContractDate'] > df['CloseDate']
        flags_added.append('listing_after_close_flag')

    if 'PurchaseContractDate' in df.columns and 'CloseDate' in df.columns:
        df['purchase_after_close_flag'] = df['PurchaseContractDate'] > df['CloseDate']
        flags_added.append('purchase_after_close_flag')

    if flags_added:
        df['negative_timeline_flag'] = df[flags_added].any(axis=1)
        flags_added.append('negative_timeline_flag')

    print("=== Date Consistency Flags ===")
    for flag in flags_added:
        count = df[flag].sum()
        print(f"  {flag}: {count:,} records ({count / len(df) * 100:.2f}%)")

    return df
