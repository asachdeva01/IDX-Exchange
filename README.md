# IDX Exchange — MLS Analytics Internship

I'm working as a Data Analyst Intern at IDX Exchange, where I analyze real MLS transaction data from the California Regional Multiple Listing Service (CRMLS) to produce housing market intelligence. This repository contains the analytical work I've built throughout the program — from raw data exploration to interactive Tableau dashboards.

---

## What This Project Is

IDX Exchange runs a data pipeline that pulls monthly listing and sold transaction records from the CoreLogic Trestle API. I take those datasets — spanning January 2024 through the most recent month — and turn them into clean, enriched analytical datasets that power market analysis and competitive intelligence dashboards in Tableau.

**Stack:** Python (Pandas, NumPy, Matplotlib, Seaborn), Tableau Desktop

---

## Repository Structure

```
IDX-Exchange/
├── exploratory_analysis/              # EDA notebook + visualization/stats helpers
│   ├── crmls_residential_eda.ipynb    # Main EDA notebook — imports from all modules below
│   └── helpers/
│       ├── visualize.py               # All plotting functions (distributions, trends, geo, etc.)
│       └── stats.py                   # Reusable aggregations (monthly KPIs, geo summaries, etc.)
│
├── data_cleaning/                     # Data preprocessing pipeline
│   ├── preprocess.py                  # Entry point — runs all cleaning steps
│   ├── geocode_missing.py             # Standalone script to recover missing coordinates
│   └── helpers/
│       ├── duplicates.py              # Drop duplicate columns from API extraction
│       ├── dates.py                   # Parse date fields, create year-month features
│       ├── missing.py                 # Missing value analysis and reporting
│       ├── outliers.py               # IQR-based outlier flagging and filtering
│       ├── mortgage_rates.py         # FRED mortgage rate loading and merging
│       ├── validation.py             # Invalid numeric value flagging
│       ├── geographic.py             # Coordinate quality checks
│       └── geocoding.py              # Address-to-coordinate recovery via Nominatim API
│
├── feature_engineering/               # Derived market metrics
│   ├── add_new_features.py            # Entry point — engineers all features
│   └── helpers/
│       └── engineer_features.py       # Market condition, price tiers, DOM buckets, etc.
│
├── data/                              # Pipeline data (gitignored, only .gitkeep tracked)
│   ├── input/                         # Raw inputs: priceratio.csv, newlistings.csv, MORTGAGE30US.csv
│   ├── deliverables/                  # Phase outputs (proof of work for each handbook week)
│   └── tableau/                       # Final datasets that feed the Tableau dashboards
│
├── tableau/                           # Tableau workbooks (coming weeks 8-10)
├── .gitignore
└── README.md
```

The EDA notebook is the central piece — it imports helper functions from `data_cleaning`, `feature_engineering`, and its own `helpers/` so the narrative stays clean while the logic lives in reusable modules.

> **Getting started:** Place your `priceratio.csv`, `newlistings.csv`, and `MORTGAGE30US.csv` files in `data/input/`, then open the EDA notebook to run the analysis.

---

## What I've Done

### Exploratory Analysis
> [`exploratory_analysis/`](exploratory_analysis/)

My first step was understanding the data I'd be working with. I combined 28 months (Jan 2024 – Apr 2026) of sold and listing CSVs — **414K closed transactions and 566K new listings** — into unified datasets, then ran a full EDA covering:

- Schema inspection, data types, and missing value analysis across 100+ columns
- Distribution analysis of key fields: ClosePrice, LivingArea, DaysOnMarket, price ratios
- Geographic breakdowns by county and city — identifying which markets are most active and competitive
- Supply vs. demand trends — new listings vs. closed sales over time
- Preliminary competitive analysis of top agents and offices by volume
- Correlation analysis between price, size, DOM, and other property attributes
- Price tier segmentation and new construction vs. existing home comparisons

### Data Cleaning
> [`data_cleaning/`](data_cleaning/)

I built a modular preprocessing pipeline that handles the common data quality issues in MLS data:

- Dropping duplicate columns created by API extraction quirks
- Parsing date fields (`CloseDate`, `ListingContractDate`) and deriving year-month keys for time-series analysis
- Generating missing value reports to identify columns with high null rates
- IQR-based outlier detection that flags extreme values without deleting records, then produces both a flagged (full) and filtered (clean) dataset for downstream analysis
- Merging FRED 30-year fixed mortgage rates (weekly → monthly resampling) onto both datasets for rate-adjusted analysis
- Date consistency validation — flagging records where listing, contract, or close dates violate logical ordering
- Invalid numeric value detection — ClosePrice <= 0, LivingArea <= 0, negative DOM/bedrooms/bathrooms
- Geographic coordinate checks — flagging missing, zero, positive longitude, and out-of-state records
- **Coordinate recovery via geocoding** — rather than imputing missing lat/lon with statistical placeholders (which distorts maps), the `geocode_missing.py` script recovers real coordinates by looking up the address through the OpenStreetMap Nominatim API. Results are cached locally to avoid repeat lookups.

### Feature Engineering
> [`feature_engineering/`](feature_engineering/)

I engineered the market metrics that power the Tableau dashboards:

- **Market condition flags** — classifying each sale as Seller's or Buyer's Market based on price ratio
- **Price reduction tracking** — flagging and measuring listings that were reduced before closing
- **DOM buckets** — segmenting days on market into actionable ranges (0-7, 8-14, 15-30, etc.)
- **Price tiers** — grouping transactions by price segment to compare market dynamics across price points
- **Timeline durations** — listing-to-contract days and contract-to-close days, derived from MLS date fields
- **Segment analysis tables** — market metrics grouped by PropertySubType, CountyOrParish, ListOfficeName, and BuyerOfficeName for competitive intelligence

<!-- Sections below will be added as work progresses -->

<!--
### Tableau Dashboards
> `tableau/`

### Market Intelligence Report
> `reports/`
-->

---

## Key Metrics I Work With

| Metric | What It Tells You |
|--------|-------------------|
| **Price Ratio** (`ClosePrice / OriginalListPrice`) | Whether homes are selling above or below ask — a read on market competitiveness |
| **Price Per Sq Ft** (`ClosePrice / LivingArea`) | Apples-to-apples price comparison across different sized homes |
| **Days on Market** | How fast homes are moving — lower means a hotter market |
| **Listing-to-Contract Days** | Time from listing to accepted offer |
| **Contract-to-Close Days** | How long escrow and closing take |

---

## What's Coming

This is an active 12-week program. As I progress, I'll be adding:

- **Tableau dashboards** — interactive market analysis and competitive intelligence workbooks
- **Market intelligence report** — a 1-page data-driven summary of a chosen California market

---

*Built during the IDX Exchange Data Analyst Internship Program.*
