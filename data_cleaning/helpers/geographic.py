"""
Geographic data quality checks.

Flags records with missing, zero, or implausible coordinates.
California coordinates should have Latitude ~32-42 and Longitude ~(-124)-(-114).
"""
import pandas as pd


def flag_invalid_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Flag records with geographic coordinate issues.

    Creates boolean flag columns:
        - missing_coords_flag:    Latitude or Longitude is null
        - zero_coords_flag:       Latitude = 0 or Longitude = 0 (sentinel nulls)
        - positive_lon_flag:      Longitude > 0 (should be negative in California)
        - out_of_state_flag:      coordinates outside California bounding box
        - any_geo_flag:           any of the above is True

    Columns that don't exist are silently skipped.
    """
    if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        print("Latitude/Longitude columns not found — skipping geographic checks.")
        return df

    lat = df['Latitude']
    lon = df['Longitude']

    # Missing coordinates
    df['missing_coords_flag'] = lat.isnull() | lon.isnull()

    # Zero coordinates (sentinel null values from the API)
    df['zero_coords_flag'] = (lat == 0) | (lon == 0)

    # Positive longitude (California should be negative)
    df['positive_lon_flag'] = lon > 0

    # Out-of-state: outside California bounding box
    # CA roughly: Lat 32.5-42.0, Lon -124.5 to -114.0
    ca_lat_min, ca_lat_max = 32.5, 42.0
    ca_lon_min, ca_lon_max = -124.5, -114.0
    has_coords = lat.notna() & lon.notna() & (lat != 0) & (lon != 0)
    df['out_of_state_flag'] = has_coords & (
        (lat < ca_lat_min) | (lat > ca_lat_max) |
        (lon < ca_lon_min) | (lon > ca_lon_max)
    )

    geo_flags: list[str] = [
        'missing_coords_flag', 'zero_coords_flag',
        'positive_lon_flag', 'out_of_state_flag',
    ]
    df['any_geo_flag'] = df[geo_flags].any(axis=1)
    geo_flags.append('any_geo_flag')

    print("=== Geographic Data Quality Flags ===")
    for flag in geo_flags:
        count = df[flag].sum()
        print(f"  {flag}: {count:,} records ({count / len(df) * 100:.2f}%)")

    return df
