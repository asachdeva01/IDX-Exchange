"""
Reusable statistical aggregation helpers for the EDA notebook.

These functions compute grouped summaries that are used both for
visualization and for the final Tableau summary output.
"""
import pandas as pd


def monthly_sold_summary(sold: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sold transactions by year-month into monthly KPIs."""
    return sold.groupby('sold_yrmo').agg(
        median_close_price=('ClosePrice', 'median'),
        median_pricesqft=('pricesqft', 'median'),
        avg_dom=('DaysOnMarket', 'mean'),
        avg_priceratio=('priceratio', 'mean'),
        homes_sold=('ClosePrice', 'count')
    ).reset_index()


def monthly_listing_summary(listings: pd.DataFrame) -> pd.DataFrame:
    """Count new listings by year-month."""
    return listings.groupby('list_yrmo').size().reset_index(name='new_listings')


def geographic_summary(sold: pd.DataFrame, geo_col: str) -> pd.DataFrame:
    """Aggregate sold data by a geographic column (CountyOrParish, City, etc.)."""
    return sold.groupby(geo_col).agg(
        homes_sold=('ClosePrice', 'count'),
        median_price=('ClosePrice', 'median'),
        avg_priceratio=('priceratio', 'mean'),
        median_pricesqft=('pricesqft', 'median'),
        avg_dom=('DaysOnMarket', 'mean')
    ).sort_values('homes_sold', ascending=False)


def dom_bucket_summary(sold: pd.DataFrame) -> pd.DataFrame:
    """Aggregate price ratio and market condition metrics by DOM bucket."""
    return (sold.dropna(subset=['dom_bucket', 'priceratio'])
            .groupby('dom_bucket', observed=True)
            .agg(
                count=('priceratio', 'count'),
                avg_priceratio=('priceratio', 'mean'),
                median_price=('ClosePrice', 'median'),
                pct_above_ask=('market_condition', lambda x: (x == "Seller's Market").mean() * 100)
            ).reset_index())


def competitive_summary(sold: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Aggregate by agent or office name for competitive analysis."""
    return sold.groupby(group_col).agg(
        units_sold=('ClosePrice', 'count'),
        total_volume=('ClosePrice', 'sum'),
        median_price=('ClosePrice', 'median'),
        avg_priceratio=('priceratio', 'mean'),
        avg_dom=('DaysOnMarket', 'mean')
    ).sort_values('units_sold', ascending=False)


def price_tier_summary(sold: pd.DataFrame) -> pd.DataFrame:
    """Aggregate metrics by price tier."""
    stats = (sold.dropna(subset=['price_tier'])
             .groupby('price_tier', observed=True)
             .agg(
                 count=('ClosePrice', 'count'),
                 avg_priceratio=('priceratio', 'mean'),
                 avg_dom=('DaysOnMarket', 'mean'),
                 median_pricesqft=('pricesqft', 'median'),
                 pct_reduced=('was_reduced', 'mean')
             ).reset_index())
    stats['pct_reduced'] = stats['pct_reduced'] * 100
    return stats


def percentile_summary(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Generate a percentile distribution table for the specified numeric columns.

    Returns min, 25th, median, mean, 75th, max, and count for each column.
    This is the formal numeric distribution summary required by the Weeks 2-3 deliverable.
    """
    stats = df[columns].describe(percentiles=[0.25, 0.5, 0.75]).T
    stats = stats[['count', 'min', '25%', '50%', 'mean', '75%', 'max']]
    stats.columns = ['Count', 'Min', '25th', 'Median', 'Mean', '75th', 'Max']
    return stats.round(2)


def market_summary(sold: pd.DataFrame, listings: pd.DataFrame):
    """Print an overall market summary for the Tableau summary section."""
    print("=" * 60)
    print("CALIFORNIA RESIDENTIAL MARKET SUMMARY")
    print(f"Period: {sold['CloseDate'].min().date()} to {sold['CloseDate'].max().date()}")
    print("=" * 60)
    print(f"Total closed transactions:    {len(sold):,}")
    print(f"Total new listings:           {len(listings):,}")
    print(f"Median close price:           ${sold['ClosePrice'].median():,.0f}")
    print(f"Median price per sq ft:       ${sold['pricesqft'].median():,.0f}")
    print(f"Avg days on market:           {sold['DaysOnMarket'].mean():.1f}")
    print(f"Avg sold/list price ratio:    {sold['priceratio'].mean():.4f}")
    print(f"% sold above ask:             {(sold['priceratio'] >= 1.0).mean() * 100:.1f}%")
    print(f"% with price reduction:       {sold['was_reduced'].mean() * 100:.1f}%")
    print(f"Unique cities:                {sold['City'].nunique()}")
    print(f"Unique counties:              {sold['CountyOrParish'].nunique()}")
    print(f"Unique ZIP codes:             {sold['PostalCode'].nunique()}")
    print(f"Unique listing offices:       {sold['ListOfficeName'].nunique()}")
    print(f"Unique listing agents:        {sold['ListAgentFullName'].nunique()}")
    print("=" * 60)
