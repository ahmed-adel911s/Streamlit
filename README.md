# 🍎 Apple Retail Sales Forecasting – EDA Dashboard

An interactive **Streamlit** dashboard for exploratory data analysis of Apple retail sales across 19 global markets (2020–2024).

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📊 Dashboard Features

| Tab | Contents |
|-----|----------|
| 📈 Sales Trends | Revenue over time, seasonality, promo impact |
| 🌍 Market Analysis | Revenue by country, market share treemap, YoY growth |
| 📱 Product Insights | Top products, category breakdown, price distribution |
| 🏪 Store Performance | Top stores, revenue heatmap, stores per country |
| 📊 Economic Factors | GDP, inflation, exchange rates, season factors |

## 🗂️ Dataset Overview

| File | Description |
|------|-------------|
| `eda/fact_sales.csv` | 1,040,200 sales transactions (2020–2024) |
| `eda/dim_product.csv` | 177 products across multiple categories |
| `eda/dim_store.csv` | 75 stores across 19 markets |
| `eda/dim_economic.csv` | Macroeconomic indicators per country/month |

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## ☁️ Deploy on Streamlit Community Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo → `dashboard.py` as the main file
5. Click **Deploy**

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** – Dashboard framework
- **[Plotly](https://plotly.com/python/)** – Interactive visualizations
- **[Pandas](https://pandas.pydata.org/)** – Data manipulation

## 📁 Project Structure

```
.
├── dashboard.py          # Main Streamlit app
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit theme configuration
└── eda/
    ├── fact_sales.csv
    ├── dim_product.csv
    ├── dim_store.csv
    └── dim_economic.csv
```
