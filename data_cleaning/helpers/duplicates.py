import pandas as pd


def drop_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicate columns created by API extraction (e.g., PropertyType.1, DaysOnMarket.1).

    Pandas appends .1, .2, etc. to duplicate column names on read. This function
    identifies and removes those suffixed duplicates.

    Returns the cleaned DataFrame and prints the columns dropped.
    """
    dup_cols = [col for col in df.columns if '.' in col and col.rsplit('.', 1)[-1].isdigit()]
    print(f"Duplicate columns to drop ({len(dup_cols)}):")
    print(dup_cols)

    df = df.drop(columns=dup_cols)
    print(f"\nShape after dropping duplicates: {df.shape}")
    return df
