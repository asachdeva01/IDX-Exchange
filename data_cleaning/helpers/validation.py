"""
Numeric value validation helpers.

Flags records with invalid or implausible values in key numeric fields.
"""
import pandas as pd


def flag_invalid_numerics(df: pd.DataFrame) -> pd.DataFrame:
    """Flag records with invalid values in core numeric fields.

    Rules applied:
        - ClosePrice  <= 0
        - LivingArea  <= 0
        - DaysOnMarket < 0
        - BedroomsTotal < 0
        - BathroomsTotalInteger < 0

    Each rule creates a boolean flag column. A summary 'any_invalid_flag'
    column is True when any individual flag fires. Columns that don't
    exist in the DataFrame are silently skipped.
    """
    rules: list[tuple[str, str]] = [
        ('ClosePrice',             'invalid_close_price'),
        ('LivingArea',             'invalid_living_area'),
        ('DaysOnMarket',           'invalid_dom'),
        ('BedroomsTotal',          'invalid_bedrooms'),
        ('BathroomsTotalInteger',  'invalid_bathrooms'),
    ]

    flags_added: list[str] = []
    for col, flag_name in rules:
        if col not in df.columns:
            continue
        if col == 'DaysOnMarket' or col == 'BedroomsTotal' or col == 'BathroomsTotalInteger':
            df[flag_name] = df[col] < 0
        else:
            df[flag_name] = df[col] <= 0
        flags_added.append(flag_name)

    if flags_added:
        df['any_invalid_flag'] = df[flags_added].any(axis=1)
        flags_added.append('any_invalid_flag')

    print("=== Invalid Numeric Value Flags ===")
    for flag in flags_added:
        count = df[flag].sum()
        print(f"  {flag}: {count:,} records ({count / len(df) * 100:.2f}%)")

    return df
