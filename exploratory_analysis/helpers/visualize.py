"""
Visualization helper functions for the EDA notebook.

Each function produces one chart or chart group. The notebook calls these
functions so the plotting logic stays out of the narrative cells.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ---------------------------------------------------------------------------
# Missing data
# ---------------------------------------------------------------------------

def plot_missing_values(sold_missing: pd.DataFrame, list_missing: pd.DataFrame,
                        top_n: int = 20):
    """Side-by-side horizontal bar charts of top missing-value columns."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    sold_missing.head(top_n)['Missing %'].plot(kind='barh', ax=axes[0], color='steelblue')
    axes[0].set_title(f'Sold — Top {top_n} Columns by Missing %')
    axes[0].set_xlabel('Missing %')

    list_missing.head(top_n)['Missing %'].plot(kind='barh', ax=axes[1], color='darkorange')
    axes[1].set_title(f'Listings — Top {top_n} Columns by Missing %')
    axes[1].set_xlabel('Missing %')

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Outlier assessment
# ---------------------------------------------------------------------------

def plot_boxplots(df: pd.DataFrame, columns: list, title: str, color: str = 'steelblue'):
    """Row of boxplots for the given numeric columns."""
    available = [c for c in columns if c in df.columns]
    fig, axes = plt.subplots(1, len(available), figsize=(20, 5))
    if len(available) == 1:
        axes = [axes]
    for i, col in enumerate(available):
        sns.boxplot(y=df[col].dropna(), ax=axes[i], color=color)
        axes[i].set_title(col)
    plt.suptitle(title, y=1.02, fontsize=14)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Distributions
# ---------------------------------------------------------------------------

def plot_sold_distributions(sold: pd.DataFrame):
    """Histograms + skewness summary for key sold metrics."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    sns.histplot(sold['ClosePrice'].dropna(), bins=50, kde=True, ax=axes[0, 0], color='steelblue')
    axes[0, 0].set_title('Close Price Distribution')
    axes[0, 0].axvline(sold['ClosePrice'].median(), color='red', linestyle='--',
                       label=f"Median: ${sold['ClosePrice'].median():,.0f}")
    axes[0, 0].legend()

    sns.histplot(sold['priceratio'].dropna(), bins=50, kde=True, ax=axes[0, 1], color='steelblue')
    axes[0, 1].set_title('Price Ratio (Close/List) Distribution')
    axes[0, 1].axvline(1.0, color='red', linestyle='--', label='1.0 (At Ask)')
    axes[0, 1].legend()

    sns.histplot(sold['pricesqft'].dropna(), bins=50, kde=True, ax=axes[0, 2], color='steelblue')
    axes[0, 2].set_title('Price per Sq Ft Distribution')
    axes[0, 2].axvline(sold['pricesqft'].median(), color='red', linestyle='--',
                       label=f"Median: ${sold['pricesqft'].median():,.0f}")
    axes[0, 2].legend()

    sns.histplot(sold['DaysOnMarket'].dropna(), bins=50, kde=True, ax=axes[1, 0], color='steelblue')
    axes[1, 0].set_title('Days on Market Distribution')

    sns.histplot(sold['LivingArea'].dropna(), bins=50, kde=True, ax=axes[1, 1], color='steelblue')
    axes[1, 1].set_title('Living Area (sq ft) Distribution')

    skew_data = sold[['ClosePrice', 'priceratio', 'pricesqft', 'DaysOnMarket', 'LivingArea']].skew()
    axes[1, 2].barh(skew_data.index, skew_data.values, color='steelblue')
    axes[1, 2].set_title('Skewness of Key Sold Metrics')
    axes[1, 2].axvline(0, color='black', linestyle='-', linewidth=0.5)

    plt.suptitle('Sold Transactions — Distribution Analysis', y=1.01, fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_listing_distributions(listings: pd.DataFrame):
    """Histograms for key listing metrics."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    sns.histplot(listings['ListPrice'].dropna(), bins=50, kde=True, ax=axes[0], color='darkorange')
    axes[0].set_title('List Price Distribution')
    axes[0].axvline(listings['ListPrice'].median(), color='red', linestyle='--',
                    label=f"Median: ${listings['ListPrice'].median():,.0f}")
    axes[0].legend()

    sns.histplot(listings['DaysOnMarket'].dropna(), bins=50, kde=True, ax=axes[1], color='darkorange')
    axes[1].set_title('Days on Market Distribution (Listings)')

    sns.histplot(listings['LivingArea'].dropna(), bins=50, kde=True, ax=axes[2], color='darkorange')
    axes[2].set_title('Living Area Distribution (Listings)')

    plt.suptitle('New Listings — Distribution Analysis', y=1.02, fontsize=14)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Market trends
# ---------------------------------------------------------------------------

def plot_monthly_kpi_trends(monthly_sold: pd.DataFrame, monthly_listings: pd.DataFrame):
    """6-panel monthly KPI dashboard: price, PPSF, DOM, ratio, sold count, listing count."""
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))

    axes[0, 0].plot(monthly_sold['sold_yrmo'].astype(str), monthly_sold['median_close_price'],
                    marker='o', color='steelblue', markersize=4)
    axes[0, 0].set_title('Median Close Price')
    axes[0, 0].set_ylabel('Price ($)')
    axes[0, 0].tick_params(axis='x', rotation=90, labelsize=8)

    axes[0, 1].plot(monthly_sold['sold_yrmo'].astype(str), monthly_sold['median_pricesqft'],
                    marker='o', color='teal', markersize=4)
    axes[0, 1].set_title('Median Price per Sq Ft')
    axes[0, 1].set_ylabel('$/sqft')
    axes[0, 1].tick_params(axis='x', rotation=90, labelsize=8)

    axes[0, 2].plot(monthly_sold['sold_yrmo'].astype(str), monthly_sold['avg_dom'],
                    marker='o', color='coral', markersize=4)
    axes[0, 2].set_title('Average Days on Market')
    axes[0, 2].set_ylabel('Days')
    axes[0, 2].tick_params(axis='x', rotation=90, labelsize=8)

    axes[1, 0].plot(monthly_sold['sold_yrmo'].astype(str), monthly_sold['avg_priceratio'],
                    marker='o', color='purple', markersize=4)
    axes[1, 0].axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='At Ask (1.0)')
    axes[1, 0].set_title('Average Sold/List Price Ratio')
    axes[1, 0].set_ylabel('Ratio')
    axes[1, 0].legend()
    axes[1, 0].tick_params(axis='x', rotation=90, labelsize=8)

    axes[1, 1].bar(monthly_sold['sold_yrmo'].astype(str), monthly_sold['homes_sold'],
                   color='steelblue', alpha=0.8)
    axes[1, 1].set_title('Homes Sold per Month')
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].tick_params(axis='x', rotation=90, labelsize=8)

    axes[1, 2].bar(monthly_listings['list_yrmo'].astype(str), monthly_listings['new_listings'],
                   color='darkorange', alpha=0.8)
    axes[1, 2].set_title('New Listings per Month')
    axes[1, 2].set_ylabel('Count')
    axes[1, 2].tick_params(axis='x', rotation=90, labelsize=8)

    plt.suptitle('Monthly Market KPI Trends — California Residential', y=1.01, fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_yoy_comparison(sold: pd.DataFrame):
    """Year-over-year overlay of median price and homes sold by month."""
    sold['close_month_dt'] = sold['CloseDate'].dt.to_period('M')
    yoy = sold.groupby(['sold_year', 'sold_month']).agg(
        median_price=('ClosePrice', 'median'),
        homes_sold=('ClosePrice', 'count')
    ).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for year in sorted(yoy['sold_year'].unique()):
        subset = yoy[yoy['sold_year'] == year]
        axes[0].plot(subset['sold_month'], subset['median_price'], marker='o',
                     label=str(year), markersize=4)
        axes[1].plot(subset['sold_month'], subset['homes_sold'], marker='o',
                     label=str(year), markersize=4)

    axes[0].set_title('Median Close Price — Year over Year')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Median Price ($)')
    axes[0].set_xticks(range(1, 13))
    axes[0].legend()

    axes[1].set_title('Homes Sold — Year over Year')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Count')
    axes[1].set_xticks(range(1, 13))
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_supply_vs_demand(monthly_sold: pd.DataFrame, monthly_listings: pd.DataFrame):
    """Bar chart of new listings vs homes sold with listing-to-sold ratio overlay."""
    supply_demand = monthly_sold[['sold_yrmo', 'homes_sold']].merge(
        monthly_listings, left_on='sold_yrmo', right_on='list_yrmo', how='inner'
    )

    fig, ax1 = plt.subplots(figsize=(16, 6))
    x = range(len(supply_demand))
    width = 0.35
    ax1.bar([i - width / 2 for i in x], supply_demand['new_listings'], width,
            label='New Listings', color='darkorange', alpha=0.8)
    ax1.bar([i + width / 2 for i in x], supply_demand['homes_sold'], width,
            label='Homes Sold', color='steelblue', alpha=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(supply_demand['sold_yrmo'].astype(str), rotation=90, fontsize=8)
    ax1.set_ylabel('Count')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    supply_demand['listing_to_sold_ratio'] = supply_demand['new_listings'] / supply_demand['homes_sold']
    ax2.plot(x, supply_demand['listing_to_sold_ratio'], color='red', marker='o',
             markersize=4, linewidth=2, label='Listing/Sold Ratio')
    ax2.set_ylabel('Listing-to-Sold Ratio', color='red')
    ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.3)
    ax2.legend(loc='upper right')

    plt.title('Supply vs. Demand — New Listings vs. Homes Sold')
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Geographic analysis
# ---------------------------------------------------------------------------

def plot_top_counties(county_stats: pd.DataFrame, top_n: int = 20):
    """Horizontal bar charts for top counties by volume, price, and DOM."""
    top = county_stats.head(top_n)
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))

    top['homes_sold'].plot(kind='barh', ax=axes[0], color='steelblue')
    axes[0].set_title(f'Top {top_n} Counties — Homes Sold')
    axes[0].set_xlabel('Count')

    top['median_price'].plot(kind='barh', ax=axes[1], color='teal')
    axes[1].set_title(f'Top {top_n} Counties — Median Close Price')
    axes[1].set_xlabel('Price ($)')

    top['avg_dom'].plot(kind='barh', ax=axes[2], color='coral')
    axes[2].set_title(f'Top {top_n} Counties — Avg Days on Market')
    axes[2].set_xlabel('Days')

    plt.tight_layout()
    plt.show()


def plot_top_cities(city_stats: pd.DataFrame, top_n: int = 20):
    """Horizontal bar charts for top cities by volume and price ratio."""
    top = city_stats.head(top_n)
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    top['homes_sold'].plot(kind='barh', ax=axes[0], color='steelblue')
    axes[0].set_title(f'Top {top_n} Cities — Homes Sold')
    axes[0].set_xlabel('Count')

    colors = ['teal' if x >= 1.0 else 'coral' for x in top['avg_priceratio']]
    top['avg_priceratio'].plot(kind='barh', ax=axes[1], color=colors)
    axes[1].axvline(x=1.0, color='red', linestyle='--', alpha=0.7, label='At Ask (1.0)')
    axes[1].set_title(f'Top {top_n} Cities — Avg Price Ratio')
    axes[1].set_xlabel('Ratio (Close/List)')
    axes[1].legend()

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Property characteristics
# ---------------------------------------------------------------------------

def plot_subtype_comparison(sold: pd.DataFrame, top_n: int = 10):
    """Boxplots comparing price, DOM, and price ratio across property subtypes."""
    subtype_order = (sold.groupby('PropertySubType')['ClosePrice']
                     .median().sort_values(ascending=False).index[:top_n])

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    sns.boxplot(data=sold[sold['PropertySubType'].isin(subtype_order)],
                y='PropertySubType', x='ClosePrice', order=subtype_order,
                ax=axes[0], palette='Blues_r')
    axes[0].set_title('Close Price by Property Subtype')
    axes[0].set_xlabel('Close Price ($)')

    sns.boxplot(data=sold[sold['PropertySubType'].isin(subtype_order)],
                y='PropertySubType', x='DaysOnMarket', order=subtype_order,
                ax=axes[1], palette='Oranges_r')
    axes[1].set_title('Days on Market by Property Subtype')
    axes[1].set_xlabel('Days')

    sns.boxplot(data=sold[sold['PropertySubType'].isin(subtype_order)],
                y='PropertySubType', x='priceratio', order=subtype_order,
                ax=axes[2], palette='Greens_r')
    axes[2].axvline(x=1.0, color='red', linestyle='--', alpha=0.7)
    axes[2].set_title('Price Ratio by Property Subtype')
    axes[2].set_xlabel('Ratio')

    plt.tight_layout()
    plt.show()


def plot_price_vs_size(sold: pd.DataFrame, sample_n: int = 10000):
    """Scatter plots: Living Area vs Close Price and Year Built vs PPSF."""
    sample = (sold.dropna(subset=['LivingArea', 'ClosePrice'])
              .sample(n=min(sample_n, len(sold)), random_state=42))

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    axes[0].scatter(sample['LivingArea'], sample['ClosePrice'], alpha=0.2, s=10, color='steelblue')
    axes[0].set_title('Living Area vs. Close Price')
    axes[0].set_xlabel('Living Area (sq ft)')
    axes[0].set_ylabel('Close Price ($)')
    axes[0].set_xlim(0, 6000)
    axes[0].set_ylim(0, 3000000)

    year_price = sold.dropna(subset=['YearBuilt', 'pricesqft'])
    year_price = year_price[year_price['YearBuilt'] >= 1900]
    year_agg = year_price.groupby('YearBuilt')['pricesqft'].median().reset_index()

    axes[1].scatter(year_agg['YearBuilt'], year_agg['pricesqft'], alpha=0.5, s=15, color='teal')
    axes[1].set_title('Year Built vs. Median Price per Sq Ft')
    axes[1].set_xlabel('Year Built')
    axes[1].set_ylabel('Median $/sqft')

    plt.tight_layout()
    plt.show()


def plot_dom_bucket_analysis(dom_analysis: pd.DataFrame):
    """Bar charts for DOM bucket breakdown: volume, price ratio, % above ask."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    axes[0].bar(dom_analysis['dom_bucket'].astype(str), dom_analysis['count'], color='steelblue')
    axes[0].set_title('Transaction Volume by DOM Bucket')
    axes[0].set_xlabel('Days on Market')
    axes[0].set_ylabel('Count')

    axes[1].bar(dom_analysis['dom_bucket'].astype(str), dom_analysis['avg_priceratio'], color='teal')
    axes[1].axhline(y=1.0, color='red', linestyle='--')
    axes[1].set_title('Avg Price Ratio by DOM Bucket')
    axes[1].set_xlabel('Days on Market')
    axes[1].set_ylabel('Ratio')

    axes[2].bar(dom_analysis['dom_bucket'].astype(str), dom_analysis['pct_above_ask'], color='purple')
    axes[2].set_title('% Sold Above Ask by DOM Bucket')
    axes[2].set_xlabel('Days on Market')
    axes[2].set_ylabel('%')

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Price reductions
# ---------------------------------------------------------------------------

def plot_price_reductions(sold: pd.DataFrame):
    """Monthly price reduction rate trend and city-level breakdown."""
    monthly_reductions = sold.groupby('sold_yrmo').agg(
        total=('was_reduced', 'count'),
        reduced=('was_reduced', 'sum')
    ).reset_index()
    monthly_reductions['reduction_rate'] = monthly_reductions['reduced'] / monthly_reductions['total'] * 100

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    axes[0].plot(monthly_reductions['sold_yrmo'].astype(str), monthly_reductions['reduction_rate'],
                 marker='o', color='coral', markersize=4)
    axes[0].set_title('Monthly Price Reduction Rate (Sold Transactions)')
    axes[0].set_ylabel('% of Sales with Price Reduction')
    axes[0].tick_params(axis='x', rotation=90, labelsize=8)

    top_20_cities = sold['City'].value_counts().head(20).index
    city_reductions = (sold[sold['City'].isin(top_20_cities)]
                       .groupby('City')
                       .agg(reduction_rate=('was_reduced', 'mean'))
                       .sort_values('reduction_rate', ascending=True) * 100)

    city_reductions['reduction_rate'].plot(kind='barh', ax=axes[1], color='coral')
    axes[1].set_title('Price Reduction Rate — Top 20 Cities by Volume')
    axes[1].set_xlabel('% Reduced')

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Competitive analysis
# ---------------------------------------------------------------------------

def plot_top_offices(office_stats: pd.DataFrame, top_n: int = 20):
    """Top offices by units sold, volume, and DOM."""
    top = office_stats.head(top_n)
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))

    top['units_sold'].plot(kind='barh', ax=axes[0], color='steelblue')
    axes[0].set_title(f'Top {top_n} Offices — Units Sold')
    axes[0].set_xlabel('Units')

    (top['total_volume'] / 1e6).plot(kind='barh', ax=axes[1], color='teal')
    axes[1].set_title(f'Top {top_n} Offices — Total Volume ($M)')
    axes[1].set_xlabel('Volume (Millions)')

    top['avg_dom'].plot(kind='barh', ax=axes[2], color='coral')
    axes[2].set_title(f'Top {top_n} Offices — Avg DOM')
    axes[2].set_xlabel('Days')

    plt.tight_layout()
    plt.show()


def plot_top_agents(agent_stats: pd.DataFrame, top_n: int = 20):
    """Top agents by units sold, volume, and price ratio."""
    top = agent_stats.head(top_n)
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))

    top['units_sold'].plot(kind='barh', ax=axes[0], color='steelblue')
    axes[0].set_title(f'Top {top_n} Agents — Units Sold')
    axes[0].set_xlabel('Units')

    (top['total_volume'] / 1e6).plot(kind='barh', ax=axes[1], color='teal')
    axes[1].set_title(f'Top {top_n} Agents — Total Volume ($M)')
    axes[1].set_xlabel('Volume (Millions)')

    top['avg_priceratio'].plot(kind='barh', ax=axes[2], color='purple')
    axes[2].axvline(x=1.0, color='red', linestyle='--', alpha=0.7)
    axes[2].set_title(f'Top {top_n} Agents — Avg Price Ratio')
    axes[2].set_xlabel('Ratio')

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Correlation
# ---------------------------------------------------------------------------

def plot_correlation_heatmap(sold: pd.DataFrame):
    """Correlation heatmap for key sold transaction metrics."""
    corr_cols = ['ClosePrice', 'OriginalListPrice', 'ListPrice', 'LivingArea',
                 'DaysOnMarket', 'priceratio', 'pricesqft', 'BedroomsTotal',
                 'BathroomsTotalInteger', 'YearBuilt', 'GarageSpaces', 'LotSizeSquareFeet']
    available = [c for c in corr_cols if c in sold.columns]

    corr_matrix = sold[available].corr()

    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', fmt='.2f',
                center=0, square=True, linewidths=0.5)
    plt.title('Correlation Matrix — Sold Transaction Metrics')
    plt.tight_layout()
    plt.show()


def plot_close_vs_list(sold: pd.DataFrame, sample_n: int = 15000):
    """Scatter plot of close price vs list price with 45-degree reference line."""
    sample = (sold.dropna(subset=['ListPrice', 'ClosePrice'])
              .sample(n=min(sample_n, len(sold)), random_state=42))

    plt.figure(figsize=(10, 10))
    plt.scatter(sample['ListPrice'], sample['ClosePrice'], alpha=0.15, s=8, color='steelblue')

    max_val = max(sample['ListPrice'].quantile(0.99), sample['ClosePrice'].quantile(0.99))
    plt.plot([0, max_val], [0, max_val], color='red', linestyle='--', linewidth=1.5,
             label='Close = List')

    plt.xlabel('List Price ($)')
    plt.ylabel('Close Price ($)')
    plt.title('Close Price vs. List Price — Points Above Line = Sold Over Ask')
    plt.legend()
    plt.xlim(0, max_val)
    plt.ylim(0, max_val)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Price tiers
# ---------------------------------------------------------------------------

def plot_price_tiers(tier_stats: pd.DataFrame):
    """4-panel view of market dynamics by price tier."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    axes[0, 0].bar(tier_stats['price_tier'].astype(str), tier_stats['count'], color='steelblue')
    axes[0, 0].set_title('Transaction Volume by Price Tier')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].tick_params(axis='x', rotation=30)

    axes[0, 1].bar(tier_stats['price_tier'].astype(str), tier_stats['avg_priceratio'], color='teal')
    axes[0, 1].axhline(y=1.0, color='red', linestyle='--')
    axes[0, 1].set_title('Avg Price Ratio by Price Tier')
    axes[0, 1].set_ylabel('Ratio')
    axes[0, 1].tick_params(axis='x', rotation=30)

    axes[1, 0].bar(tier_stats['price_tier'].astype(str), tier_stats['avg_dom'], color='coral')
    axes[1, 0].set_title('Avg Days on Market by Price Tier')
    axes[1, 0].set_ylabel('Days')
    axes[1, 0].tick_params(axis='x', rotation=30)

    axes[1, 1].bar(tier_stats['price_tier'].astype(str), tier_stats['pct_reduced'], color='purple')
    axes[1, 1].set_title('% Price Reduced by Price Tier')
    axes[1, 1].set_ylabel('%')
    axes[1, 1].tick_params(axis='x', rotation=30)

    plt.suptitle('Market Dynamics by Price Tier', y=1.01, fontsize=14)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# New construction
# ---------------------------------------------------------------------------

def plot_new_construction(sold: pd.DataFrame):
    """Compare new construction vs existing homes on price, PPSF, and DOM."""
    if 'NewConstructionYN' not in sold.columns:
        print("NewConstructionYN column not found — skipping.")
        return

    new_const = sold.dropna(subset=['NewConstructionYN']).copy()
    new_const['NewConstructionYN'] = new_const['NewConstructionYN'].astype(str)

    nc_stats = new_const.groupby('NewConstructionYN').agg(
        count=('ClosePrice', 'count'),
        median_price=('ClosePrice', 'median'),
        median_pricesqft=('pricesqft', 'median'),
        avg_dom=('DaysOnMarket', 'mean'),
        avg_priceratio=('priceratio', 'mean')
    )

    print("New Construction vs. Existing Homes:")
    print(nc_stats.to_string())

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    nc_stats['median_price'].plot(kind='bar', ax=axes[0], color=['steelblue', 'darkorange'])
    axes[0].set_title('Median Close Price')
    axes[0].set_ylabel('Price ($)')
    axes[0].tick_params(axis='x', rotation=0)

    nc_stats['median_pricesqft'].plot(kind='bar', ax=axes[1], color=['steelblue', 'darkorange'])
    axes[1].set_title('Median Price per Sq Ft')
    axes[1].set_ylabel('$/sqft')
    axes[1].tick_params(axis='x', rotation=0)

    nc_stats['avg_dom'].plot(kind='bar', ax=axes[2], color=['steelblue', 'darkorange'])
    axes[2].set_title('Avg Days on Market')
    axes[2].set_ylabel('Days')
    axes[2].tick_params(axis='x', rotation=0)

    plt.suptitle('New Construction (True) vs. Existing (False)', y=1.02, fontsize=13)
    plt.tight_layout()
    plt.show()
