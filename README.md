# IDX Exchange — MLS Analytics Internship

I completed a 12-week Data Analyst Internship at IDX Exchange, analyzing real MLS transaction data from the California Regional Multiple Listing Service (CRMLS) to produce housing market intelligence. This repository contains the analytical work I built throughout the program — from raw data exploration through interactive Tableau dashboards published to Tableau Public.

**Live dashboards:** [Tableau Public Profile](https://public.tableau.com/app/profile/abhi.sachdeva/vizzes)

---

## What This Project Is

IDX Exchange runs a data pipeline that pulls monthly listing and sold transaction records from the CoreLogic Trestle API. I took those datasets — spanning **January 2024 through April 2026** (28 months) — and turned them into clean, enriched analytical datasets that power two Tableau workbooks: **market analysis** and **competitive intelligence**.

**Stack:** Python (Pandas, NumPy, Matplotlib, Seaborn), Tableau Desktop Public Edition

**Final Deliverables:**
- Two published Tableau Public workbooks (6 dashboards in market analysis, 5 in competitive analysis)
- 1-page Market Intelligence Report
- 5-minute presentation walking through findings

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
│       ├── outliers.py                # IQR-based outlier flagging and filtering
│       ├── mortgage_rates.py          # FRED mortgage rate loading and merging
│       ├── validation.py              # Invalid numeric value flagging
│       ├── geographic.py              # Coordinate quality checks
│       └── geocoding.py               # Address-to-coordinate recovery via Nominatim API
│
├── feature_engineering/               # Derived market metrics
│   ├── add_new_features.py            # Entry point — engineers all features
│   └── helpers/
│       └── engineer_features.py       # Market condition, price tiers, DOM buckets, etc.
│
├── tableau/                           # Tableau workbooks (.twb XML configs only;
│   ├── market_analysis.twb            # data extracts gitignored)
│   └── competitve_analysis.twb
│
├── reports/                           # Final deliverables
│   └── Market_Intelligence_Report.md  # 1-page summary of California market findings
│
├── data/                              # Pipeline data (gitignored, only .gitkeep tracked)
│   ├── input/                         # Raw inputs: priceratio.csv, newlistings.csv, MORTGAGE30US.csv
│   ├── deliverables/                  # Phase outputs (proof of work for each handbook week)
│   └── tableau/                       # Final datasets that feed the Tableau dashboards
│
├── .gitignore
└── README.md
```

The EDA notebook is the central piece — it imports helper functions from `data_cleaning`, `feature_engineering`, and its own `helpers/` so the narrative stays clean while the logic lives in reusable modules.

> **Running the pipeline:** Place `priceratio.csv`, `newlistings.csv`, and `MORTGAGE30US.csv` in `data/input/`, then open the EDA notebook to run the analysis. CSV data is gitignored — the analytical code is what's public.

---

## What I Built

### Tableau Dashboards — Published on Tableau Public
> [Tableau Public Profile](https://public.tableau.com/app/profile/abhi.sachdeva/vizzes)

**[CRMLS Market Analysis — Jan 2024 to Apr 2026](https://public.tableau.com/app/profile/abhi.sachdeva/viz/CRMLSMarketAnalysisJan2024toApr2026/MonthlyMedianClosePrice)** — 6 dashboards covering statewide market dynamics:
- Monthly Median Close Price
- Average Days on Market
- Average Close-to-List Price Ratio
- New Listings per Month
- Closed Sales per Month
- Mortgage Rate vs Sales Volume (custom dashboard joining FRED MORTGAGE30US data)

**[CRMLS Competitive Analysis — Jan 2024 to Apr 2026](https://public.tableau.com/app/profile/abhi.sachdeva/viz/CRMLSCompetitiveAnalysisJan2024toApr2026/Top100ListingOffices)** — 5 dashboards covering brokerage and agent landscape:
- Top 100 Listing Offices
- Top 100 Listing Agents
- Top 100 Buyer Offices
- ZIP Heat Map — Median Close Prices
- ZIP Heat Map — Homes Sold

All dashboards support filtering by **county, city, ZIP code, and property subtype**, with single-value dropdowns for fast drill-down. The competitive analysis defaults to Single Family Residence to match the dominant market segment.

### Market Intelligence Report
> [`reports/Market_Intelligence_Report.md`](reports/Market_Intelligence_Report.md)

A 1-page summary of the California residential market over the reporting window, covering median price trends, days-on-market evolution, sold-to-list ratio dynamics, top brokerage concentration, and five key takeaways — including the finding that the late-2025 market softness decoupled from mortgage rate movements, suggesting non-rate factors (inventory accumulation, buyer fatigue) became the dominant driver.

### Exploratory Analysis
> [`exploratory_analysis/`](exploratory_analysis/)

My first step was understanding the data. I combined 28 months (Jan 2024 – Apr 2026) of sold and listing CSVs — **414K closed transactions and 566K new listings** — into unified datasets, then ran a full EDA covering:

- Schema inspection, data types, and missing value analysis across 100+ columns
- Distribution analysis of key fields: ClosePrice, LivingArea, DaysOnMarket, price ratios
- Geographic breakdowns by county and city — identifying which markets are most active and competitive
- Supply vs. demand trends — new listings vs. closed sales over time
- Preliminary competitive analysis of top agents and offices by volume
- Correlation analysis between price, size, DOM, and other property attributes
- Price tier segmentation and new construction vs. existing home comparisons

### Data Cleaning
> [`data_cleaning/`](data_cleaning/)

A modular preprocessing pipeline that handles the common data quality issues in MLS data:

- Dropping duplicate columns created by API extraction quirks
- Parsing date fields (`CloseDate`, `ListingContractDate`) and deriving year-month keys for time-series analysis
- Generating missing value reports to identify columns with high null rates
- IQR-based outlier detection that flags extreme values without deleting records, then produces both a flagged (full) and filtered (clean) dataset for downstream analysis
- Merging FRED 30-year fixed mortgage rates (weekly → monthly resampling) onto both datasets for rate-adjusted analysis
- Date consistency validation — flagging records where listing, contract, or close dates violate logical ordering
- Invalid numeric value detection — ClosePrice <= 0, LivingArea <= 0, negative DOM/bedrooms/bathrooms
- Geographic coordinate checks — flagging missing, zero, positive longitude, and out-of-state records
- **Coordinate recovery via geocoding** — rather than imputing missing lat/lon with statistical placeholders (which distorts maps), `geocode_missing.py` recovers real coordinates by looking up the address through the OpenStreetMap Nominatim API. Results are cached locally to avoid repeat lookups.

### Feature Engineering
> [`feature_engineering/`](feature_engineering/)

The market metrics that power the Tableau dashboards:

- **Market condition flags** — classifying each sale as Seller's or Buyer's Market based on price ratio
- **Price reduction tracking** — flagging and measuring listings that were reduced before closing
- **DOM buckets** — segmenting days on market into actionable ranges (0-7, 8-14, 15-30, etc.)
- **Price tiers** — grouping transactions by price segment to compare market dynamics across price points
- **Timeline durations** — listing-to-contract days and contract-to-close days, derived from MLS date fields
- **Segment analysis tables** — market metrics grouped by PropertySubType, CountyOrParish, ListOfficeName, and BuyerOfficeName for competitive intelligence

---

## Key Metrics

| Metric | What It Tells You |
|--------|-------------------|
| **Price Ratio** (`ClosePrice / OriginalListPrice`) | Whether homes are selling above or below ask — a read on market competitiveness |
| **Price Per Sq Ft** (`ClosePrice / LivingArea`) | Apples-to-apples price comparison across different sized homes |
| **Days on Market** | How fast homes are moving — lower means a hotter market |
| **Listing-to-Contract Days** | Time from listing to accepted offer |
| **Contract-to-Close Days** | How long escrow and closing take |

---

*Built during the IDX Exchange Data Analyst Internship — MLS Analytics & Tableau Dashboard Program.*
