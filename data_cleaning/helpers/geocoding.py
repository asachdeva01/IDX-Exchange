"""
Geocoding helper for recovering missing latitude/longitude values.

Rather than imputing missing coordinates with a median (which distorts spatial
analysis), this module recovers actual locations by geocoding the address
through the OpenStreetMap Nominatim service.

Nominatim is free, requires no API key, and is rate-limited to 1 request per
second. Results are cached locally so re-running won't re-geocode addresses
already looked up.
"""
import json
import time
from pathlib import Path
from typing import Optional, Tuple, Dict

import pandas as pd
import requests


# ---------------------------------------------------------------------------
# Nominatim API call
# ---------------------------------------------------------------------------

def _geocode_nominatim(address: str, timeout: int = 10) -> Tuple[Optional[float], Optional[float]]:
    """Geocode a single address using OpenStreetMap Nominatim.

    Returns (lat, lon) on success, (None, None) on any failure.
    """
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'IDX-Exchange-Internship/1.0'}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        results = response.json()
        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
    except (requests.RequestException, ValueError, KeyError):
        pass
    return None, None


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------

def _load_cache(path: Path) -> Dict[str, Tuple[float, float]]:
    if path.exists():
        with open(path) as f:
            return {k: tuple(v) for k, v in json.load(f).items()}
    return {}


def _save_cache(cache: Dict[str, Tuple[float, float]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump({k: list(v) for k, v in cache.items()}, f)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def geocode_missing_coordinates(
    df: pd.DataFrame,
    address_col: str = 'UnparsedAddress',
    lat_col: str = 'Latitude',
    lon_col: str = 'Longitude',
    cache_path='data/geocode_cache.json',
    rate_limit_sec: float = 1.0,
    progress_every: int = 100,
    dry_run: bool = False,
) -> pd.DataFrame:
    """Recover missing latitude/longitude by geocoding the address field.

    Only rows where lat OR lon is null (or zero) are geocoded. Results are
    cached so re-running on the same data won't re-geocode.

    Args:
        df:             DataFrame to enrich.
        address_col:    Column containing the address string (e.g. 'UnparsedAddress').
        lat_col, lon_col: Coordinate columns to fill.
        cache_path:     JSON file path for caching results across runs.
        rate_limit_sec: Sleep between API calls (Nominatim requires >=1.0).
        progress_every: Print progress every N records.
        dry_run:        Count how many records would be geocoded without making calls.

    Returns:
        DataFrame with missing coordinates filled where geocoding succeeded.
    """
    # Identify rows needing geocoding: null OR zero coordinates
    needs_geo = (
        df[lat_col].isna() | df[lon_col].isna() |
        (df[lat_col] == 0) | (df[lon_col] == 0)
    )
    to_geocode = df[needs_geo & df[address_col].notna()].copy()

    print(f"Total rows missing coords: {needs_geo.sum():,}")
    print(f"  with an address to geocode: {len(to_geocode):,}")
    print(f"  without address (cannot recover): {needs_geo.sum() - len(to_geocode):,}")

    if dry_run:
        print(f"\nDry run — no API calls made. Would geocode {len(to_geocode):,} addresses.")
        print(f"Estimated runtime at {rate_limit_sec}s/req: "
              f"~{len(to_geocode) * rate_limit_sec / 60:.0f} minutes")
        return df

    cache_path = Path(cache_path)
    cache = _load_cache(cache_path)
    print(f"Cache loaded: {len(cache):,} addresses previously geocoded")

    # Geocode each missing row
    geocoded = 0
    skipped = 0
    failed = 0
    for i, (idx, row) in enumerate(to_geocode.iterrows(), start=1):
        address = str(row[address_col]).strip()
        if not address:
            skipped += 1
            continue

        if address in cache:
            lat, lon = cache[address]
        else:
            lat, lon = _geocode_nominatim(address)
            time.sleep(rate_limit_sec)

            if lat is not None and lon is not None:
                cache[address] = (lat, lon)
            else:
                failed += 1
                continue

        df.at[idx, lat_col] = lat
        df.at[idx, lon_col] = lon
        geocoded += 1

        if i % progress_every == 0:
            print(f"  Progress: {i:,}/{len(to_geocode):,} processed "
                  f"({geocoded:,} geocoded, {failed:,} failed)")
            _save_cache(cache, cache_path)

    _save_cache(cache, cache_path)

    print(f"\n=== Geocoding Complete ===")
    print(f"  Geocoded:  {geocoded:,}")
    print(f"  Failed:    {failed:,}")
    print(f"  Skipped:   {skipped:,}")
    print(f"  Cache now has: {len(cache):,} addresses")
    return df
