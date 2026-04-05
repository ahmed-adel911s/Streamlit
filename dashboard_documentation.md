# 🍎 Apple Sales Intelligence Dashboard — Full Documentation

## Table of Contents

1. [Overview](#overview)
2. [Bugs Found & Fixed](#bugs-found--fixed)
3. [Data Sources & Schema](#data-sources--schema)
4. [KPI Cards (Top Row)](#kpi-cards-top-row)
5. [Tab 1 — Sales Trends](#tab-1--sales-trends)
6. [Tab 2 — Market Analysis](#tab-2--market-analysis)
7. [Tab 3 — Product Insights](#tab-3--product-insights)
8. [Tab 4 — Store Performance](#tab-4--store-performance)
9. [Tab 5 — Economic Factors](#tab-5--economic-factors)
10. [Sidebar Filters](#sidebar-filters)

---

## Overview

The dashboard is built with **Streamlit + Plotly** and provides multi-market exploratory data analysis for Apple product sales from **January 2020 to November 2024** across **19 international markets**, **89 unique products**, and **75 stores**.

**File**: [dashboard.py](file:///c:/Users/Amira%20Roshdy/Downloads/Test/dashboard.py)

---

## Bugs Found & Fixed

> [!CAUTION]
> Three significant issues were found and corrected in the dashboard code.

### Bug 1 — Product Merge Duplication (CRITICAL) ⚠️

| Aspect | Detail |
|---|---|
| **Root Cause** | `dim_product.csv` has 177 rows but only 89 unique `product_id` values. Each product appears twice with different `launch_date` values. |
| **Impact** | The `merge(dim_product, on="product_id")` created a ~1.98x row fan-out: 1,040,200 → 2,068,642 rows |
| **KPIs Affected** | Total Revenue inflated by ~$6.79B, Total Units inflated by ~5.66M, Transaction count inflated by ~1.03M |
| **Fix** | Added `dim_product.drop_duplicates(subset="product_id", keep="first")` before the merge |

```diff
+    # Deduplicate dim_product (each product_id appears twice with different launch_dates)
+    dim_product_dedup = dim_product.drop_duplicates(subset="product_id", keep="first")
+
     # Merge into one analytical table
     df = (fact_sales
           .merge(dim_store,    on="store_id",   how="left", suffixes=("", "_store"))
-          .merge(dim_product,  on="product_id", how="left", suffixes=("", "_prod"))
+          .merge(dim_product_dedup,  on="product_id", how="left", suffixes=("", "_prod"))
           .merge(dim_economic, on=["sale_date", "country_norm_mapped"], how="left"))
```

| KPI | Before Fix (Wrong) | After Fix (Correct) |
|---|---|---|
| Total Revenue | ~$13.73B | **$6.94B** |
| Total Units | ~11,377,482 | **5,721,344** |
| Transactions | ~2,068,642 | **1,040,200** |
| Avg Order Value | ~$6,636 | **$6,669** |
| Promo Rate | 10.0% | **10.0%** (unchanged — ratio) |

### Bug 2 — Hardcoded Sidebar Product Count

| Aspect | Detail |
|---|---|
| **Root Cause** | Sidebar text was hardcoded with `177 products` (total dim_product rows) instead of 89 (unique products) |
| **Fix** | Made all sidebar statistics dynamic, computed from the actual data |

### Bug 3 — Misleading Seasonality Chart

| Aspect | Detail |
|---|---|
| **Root Cause** | Chart titled "Avg Monthly Revenue" was computing `groupby("month_name").mean()` — the mean of individual transaction amounts per month, NOT average monthly revenue |
| **Impact** | Showed values in the ~$5K-$10K range instead of ~$93M-$138M |
| **Fix** | Changed to `groupby("month_name").sum() / n_years` to correctly show the average total monthly revenue across years |

---

## Data Sources & Schema

### fact_sales.csv (1,040,200 rows)

| Column | Type | Description |
|---|---|---|
| `sale_id` | string | Unique transaction identifier |
| `sale_date` | date | Date of the sale (2020-01-01 to 2024-11-12) |
| `store_id` | string | Foreign key → dim_store |
| `product_id` | string | Foreign key → dim_product |
| `quantity` | int | Units sold (1–10) |
| `price` | int | Unit price in USD (231–1965) |
| `sales_amount` | float | Raw sales total (quantity × price) |
| `promo_flag` | int | 0 = no promotion, 1 = promotion |
| `sales_amount_realistic` | float | Adjusted/realistic sales amount |
| `country_norm_mapped` | string | Normalized country name (lowercase) |

### dim_product.csv (177 rows → 89 unique products)

| Column | Type | Description |
|---|---|---|
| `product_id` | string | Primary key (P-1 through P-89) |
| `product_name` | string | Apple product name |
| `launch_date` | date | Product launch date (causes duplicates) |
| `category_id` | string | Category foreign key |
| `category_name` | string | One of 10 categories |

**Categories**: Subscription Service, Smartphone, Audio, Desktop, Accessories, Wearable, Laptop, Tablet, Smart Speaker, Streaming Device

### dim_store.csv (75 rows)

| Column | Type | Description |
|---|---|---|
| `store_id` | string | Primary key |
| `store_name` | string | Apple store name |
| `city` | string | City location |
| `country_norm_mapped` | string | Normalized country name |

### dim_economic.csv (33,774 rows)

| Column | Type | Description |
|---|---|---|
| `sale_date` | date | Date (daily granularity) |
| `country_norm_mapped` | string | Normalized country name |
| `exchange_rate` | float | Exchange rate vs USD |
| `inflation_rate` | float | Country inflation rate (%) |
| `gdp_per_capita` | float | GDP per capita in USD |
| `season_factor` | float | Seasonal demand multiplier |

---

## KPI Cards (Top Row)

Six KPI cards displayed in a single row at the top of the dashboard. All are **dynamic** and respond to sidebar filters.

| # | KPI | Formula | Description |
|---|---|---|---|
| 1 | 💰 **Total Revenue** | `SUM(sales_amount_realistic)` | Total adjusted sales amount across all filtered transactions. Formatted in M/B. |
| 2 | 📦 **Total Units Sold** | `SUM(quantity)` | Total quantity of items sold across all filtered transactions. |
| 3 | 🧾 **Transactions** | `COUNT(rows)` | Total number of transaction records matching current filters. |
| 4 | 🛒 **Avg Order Value** | `MEAN(sales_amount_realistic)` | Average revenue per transaction. This is the mean of the realistic sales amount column. |
| 5 | 🎯 **Promo Rate** | `MEAN(promo_flag) × 100` | Percentage of transactions that had a promotion applied. |
| 6 | 🌍 **Active Markets** | `NUNIQUE(country)` | Count of distinct countries/markets represented in filtered data. |

> [!IMPORTANT]
> Correct unfiltered values: Revenue = **$6.94B**, Units = **5,721,344**, Transactions = **1,040,200**, AOV = **$6,669**, Promo Rate = **10.0%**, Markets = **19**

---

## Tab 1 — Sales Trends

### 1.1 Revenue Over Time (Area Chart)
- **Granularity**: Monthly / Quarterly / Yearly (user selectable)
- **Metric**: `SUM(sales_amount_realistic)` grouped by selected time period
- **Chart type**: Plotly Area chart with gradient fill
- **Purpose**: Track overall revenue trajectory and identify growth/decline periods

### 1.2 Category Revenue by Year (Grouped Bar)
- **Metric**: `SUM(sales_amount_realistic)` grouped by `(year, category_name)`
- **Chart type**: Grouped bar chart, one bar group per year
- **Purpose**: Compare category performance across years, identify which product lines are growing

### 1.3 Monthly Seasonality (Bar Chart)
- **Metric**: `SUM(sales_amount_realistic) per month_name / COUNT(distinct years)`
- **Chart type**: Bar chart with Purples color scale proportional to value
- **Purpose**: Reveal seasonal demand patterns — e.g., November and December show peak revenue (holiday season)

> [!NOTE]
> **Fixed**: Previously used per-transaction mean which was misleading. Now correctly shows average monthly total revenue across all years.

### 1.4 Promo vs Non-Promo Revenue Over Time (Line Chart)
- **Metric**: `SUM(sales_amount_realistic)` grouped by `(yearmonth, promo_flag)`
- **Chart type**: Dual-line chart (pink = Promo, indigo = No Promo)
- **Purpose**: Visualize promotion impact on monthly revenue over time

---

## Tab 2 — Market Analysis

### 2.1 Revenue by Country (Horizontal Bar)
- **Metric**: `SUM(sales_amount_realistic)` grouped by `country`
- **Chart type**: Horizontal bar, sorted descending, with Purples color scale
- **Purpose**: Rank countries by total revenue contribution

### 2.2 Market Share Treemap
- **Metric**: Same data as 2.1 — `SUM(sales_amount_realistic)` by country
- **Chart type**: Treemap with area proportional to revenue
- **Purpose**: Visual representation of market share — quickly see dominant vs. minor markets

### 2.3 Top-10 Country Revenue Trend (Line Chart)
- **Metric**: `SUM(sales_amount_realistic)` grouped by `(country, year)`, filtered to top-10 countries
- **Chart type**: Multi-line with markers
- **Purpose**: Track year-over-year revenue trends for the most important markets

### 2.4 Units Sold by Country (Bar)
- **Metric**: `SUM(quantity)` grouped by `country`, top 15
- **Chart type**: Vertical bar with Blues color scale
- **Purpose**: Volume analysis — which markets drive the most unit sales

### 2.5 Avg Order Value by Country (Bar)
- **Metric**: `MEAN(sales_amount_realistic)` grouped by `country`, top 15
- **Chart type**: Vertical bar with Pinkyl color scale
- **Purpose**: Identify high-value vs. low-value markets — higher AOV may indicate premium product mix or pricing differences

---

## Tab 3 — Product Insights

### 3.1 Revenue Share by Category (Donut Chart)
- **Metric**: `SUM(sales_amount_realistic)` grouped by `category_name`
- **Chart type**: Pie/donut chart (hole=0.45)
- **Purpose**: Show which product categories drive the most revenue

### 3.2 Units Sold by Category (Bar)
- **Metric**: `SUM(quantity)` grouped by `category_name`
- **Chart type**: Vertical bar with Purples color scale
- **Purpose**: Compare volume across product categories

### 3.3 Top Products by Revenue (Horizontal Bar)
- **Metric**: `SUM(sales_amount_realistic)` grouped by `(product_name, category_name)`, top N
- **N**: User-configurable via slider (5–30, default 15)
- **Chart type**: Horizontal bar, color-coded by category
- **Purpose**: Identify the highest-grossing individual products

### 3.4 Price Distribution by Category (Box Plot)
- **Metric**: Distribution of `price` per `category_name`
- **Chart type**: Box plot showing median, IQR, and outliers
- **Purpose**: Understand price range and spread within each product category

### 3.5 Quantity Distribution (Histogram)
- **Metric**: Distribution of `quantity` per transaction
- **Chart type**: Histogram with 10 bins
- **Purpose**: Understand typical order sizes (1–10 units range)

### 3.6 Promo Impact by Category (Grouped Bar)
- **Metric**: `MEAN(sales_amount_realistic)` grouped by `(category_name, promo_flag)`
- **Chart type**: Grouped bar (pink = Promo, indigo = No Promo)
- **Purpose**: Assess whether promotions increase or decrease average transaction value per category

---

## Tab 4 — Store Performance

### 4.1 Top 20 Stores by Revenue (Horizontal Bar)
- **Metric**: `SUM(sales_amount_realistic)` grouped by `(store_id, store_name, city, country)`, top 20
- **Chart type**: Horizontal bar, color-coded by country
- **Purpose**: Identify the highest-performing stores globally

### 4.2 Store Count by Country (Bar)
- **Metric**: `COUNT(stores)` from `dim_store` grouped by `country_norm_mapped`
- **Data source**: `dim_store` directly (not filtered)
- **Chart type**: Vertical bar with Purples color scale
- **Purpose**: Show store distribution across markets

### 4.3 Revenue per Store by Country (Bar)
- **Metric**: `SUM(sales_amount_realistic) / NUNIQUE(store_id)` per country
- **Chart type**: Vertical bar with Pinkyl color scale
- **Purpose**: Normalize revenue by store count to identify the most efficient markets

### 4.4 Store Revenue Heatmap (Heatmap)
- **Metric**: `SUM(sales_amount_realistic)` for top 20 stores × year
- **Chart type**: 2D heatmap (stores as rows, years as columns)
- **Purpose**: Visualize store performance patterns over time, identify growing vs. declining stores

---

## Tab 5 — Economic Factors

### 5.1 GDP per Capita by Country (Bar)
- **Metric**: `MEAN(gdp_per_capita)` from `dim_economic`, grouped by country
- **Chart type**: Vertical bar with Purples color scale
- **Purpose**: Contextualize sales data with economic wealth indicators

### 5.2 Avg Inflation Rate by Country (Bar)
- **Metric**: `MEAN(inflation_rate)` from `dim_economic`, grouped by country
- **Chart type**: Vertical bar with RdPu color scale
- **Purpose**: Understand inflationary pressures across markets

### 5.3 GDP vs. Sales Revenue Correlation (Scatter)
- **Metric**: X = `MEAN(gdp_per_capita)`, Y = `SUM(sales_amount_realistic)`, Size = Revenue
- **Chart type**: Bubble scatter plot, color-coded by country
- **Purpose**: Explore whether wealthier countries generate more Apple revenue

### 5.4 Exchange Rate Over Time (Line Chart)
- **Metric**: `exchange_rate` from `dim_economic` over time
- **Countries**: User-selectable (default: Japan, UK, Australia, Canada)
- **Purpose**: Track currency fluctuations that may impact regional pricing and revenue

### 5.5 Inflation Rate Over Time (Line Chart)
- **Metric**: `inflation_rate` from `dim_economic` over time
- **Countries**: Same selection as 5.4
- **Purpose**: Track inflation trends that may impact consumer purchasing power

### 5.6 Season Factor Distribution (Histogram)
- **Metric**: Distribution of `season_factor` across all economic records
- **Chart type**: Histogram with 20 bins
- **Purpose**: Show the spread of seasonal demand multipliers used in the data

---

## Sidebar Filters

| Filter | Type | Default | Effect |
|---|---|---|---|
| **Year(s)** | Multi-select | All (2020–2024) | Filters by `sale_date.year` |
| **Country/Market** | Multi-select | All 19 countries | Filters by `country` |
| **Product Category** | Multi-select | All 10 categories | Filters by `category_name` |
| **Promotion Filter** | Radio | "All" | Options: All / Promo Only / No Promo |

> [!NOTE]
> All KPI cards and charts in all tabs are responsive to these filters. The "Store Count by Country" chart in Tab 4 uses `dim_store` directly and is the only visual not affected by filters.

---

## Summary of Changes Made

render_diffs(file:///c:/Users/Amira%20Roshdy/Downloads/Test/dashboard.py)
