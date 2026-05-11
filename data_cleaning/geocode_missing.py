"""
Standalone Geocoding Script

Recovers missing latitude/longitude in priceratio.csv (the sold dataset) by
geocoding the UnparsedAddress field via OpenStreetMap Nominatim (free, no API
key required). Run this once after pulling new data — it's slow due to the
1 req/sec rate limit, so plan on ~70 minutes for ~4K records.

Listings are skipped by default because the dashboards aggregate by ZIP code
(which is already populated), and the ~80K listings missing coordinates would
take >20 hours to geocode at Nominatim's rate limit.

Usage:
    # Dry run — see how many records need geocoding, no API calls
    python3 data_cleaning/geocode_missing.py --dry-run

    # Actually geocode (saves to data/input/priceratio_geocoded.csv)
    python3 data_cleaning/geocode_missing.py

    # Include listings (slow — ~22 hours for ~80K records)
    python3 data_cleaning/geocode_missing.py --include-listings
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_cleaning.helpers.geocoding import geocode_missing_coordinates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true',
                        help='Count records without making API calls')
    parser.add_argument('--data-dir', default='data/input',
                        help='Directory containing input CSVs')
    parser.add_argument('--include-listings', action='store_true',
                        help='Also geocode the listings dataset (slow)')
    parser.add_argument('--rate-limit', type=float, default=1.0,
                        help='Seconds between API calls (Nominatim requires >=1.0)')
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    csvs = ['priceratio.csv']
    if args.include_listings:
        csvs.append('newlistings.csv')

    for csv_name in csvs:
        csv_path = data_dir / csv_name
        if not csv_path.exists():
            print(f"Skipping {csv_name} — not found in {data_dir}")
            continue

        print(f"\n{'=' * 60}")
        print(f"Processing {csv_name}")
        print('=' * 60)
        df = pd.read_csv(csv_path, encoding='ISO-8859-1', low_memory=False)

        df = geocode_missing_coordinates(
            df,
            cache_path=data_dir.parent / 'geocode_cache.json',
            rate_limit_sec=args.rate_limit,
            dry_run=args.dry_run,
        )

        if not args.dry_run:
            output_name = csv_name.replace('.csv', '_geocoded.csv')
            output_path = data_dir / output_name
            df.to_csv(output_path, index=False)
            print(f"Saved {output_name}: {len(df):,} rows")


if __name__ == '__main__':
    main()
