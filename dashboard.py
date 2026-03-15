import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# â”€â”€â”€ Page Config â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.set_page_config(
    page_title="Apple Sales Intelligence Dashboard",
    page_icon="ðŸŽ",
    layout="wide",
    initial_sidebar_state="expanded",
)

# â”€â”€â”€ Custom CSS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 40%, #0a0f1a 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #111128 100%);
    border-right: 1px solid rgba(99,102,241,0.2);
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    backdrop-filter: blur(10px);
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.25);
}
.kpi-value {
    font-size: 2.1rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.kpi-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: #94a3b8;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.kpi-delta {
    font-size: 0.85rem;
    color: #34d399;
    margin-top: 4px;
    font-weight: 600;
}

/* Section headers */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid rgba(99,102,241,0.2);
    margin: 24px 0;
}

/* Main title */
.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}
.sub-title {
    font-size: 1rem;
    color: #64748b;
    margin-top: 4px;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(15,15,30,0.6);
    border-radius: 12px;
    padding: 6px;
    border: 1px solid rgba(99,102,241,0.2);
}
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    color: #64748b;
    border-radius: 8px;
    padding: 8px 20px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.4), rgba(139,92,246,0.3)) !important;
    color: #c4b5fd !important;
}

/* Metric containers */
[data-testid="stMetricValue"] { color: #818cf8 !important; font-weight: 700; }
[data-testid="stMetricDelta"] { font-weight: 600; }

/* Plotly charts background */
.js-plotly-plot .plotly .modebar { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


# â”€â”€â”€ Data Loading â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# Use a path relative to this script so it works locally AND on Streamlit Cloud
DATA_PATH = Path(__file__).parent / "eda"

@st.cache_data(show_spinner="Loading datasetsâ€¦")
def load_data():
    dim_economic = pd.read_csv(f"{DATA_PATH}/dim_economic.csv", on_bad_lines="skip")
    dim_product  = pd.read_csv(f"{DATA_PATH}/dim_product.csv",  on_bad_lines="skip")
    dim_store    = pd.read_csv(f"{DATA_PATH}/dim_store.csv",    on_bad_lines="skip")
    fact_sales   = pd.read_csv(f"{DATA_PATH}/fact_sales.csv",   on_bad_lines="skip")

    # Parse dates
    fact_sales["sale_date"]    = pd.to_datetime(fact_sales["sale_date"])
    dim_economic["sale_date"]  = pd.to_datetime(dim_economic["sale_date"])

    # Merge into one analytical table
    df = (fact_sales
          .merge(dim_store,    on="store_id",   how="left", suffixes=("", "_store"))
          .merge(dim_product,  on="product_id", how="left", suffixes=("", "_prod"))
          .merge(dim_economic, on=["sale_date", "country_norm_mapped"], how="left"))

    df["year"]  = df["sale_date"].dt.year
    df["month"] = df["sale_date"].dt.month
    df["month_name"] = df["sale_date"].dt.strftime("%b")
    df["yearmonth"] = df["sale_date"].dt.to_period("M").astype(str)
    df["quarter"] = df["sale_date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
    df["country"] = df["country_norm_mapped"].str.title()

    # ── Memory optimisation (cuts RAM by ~65%) ───────────────────────
    # Convert low-cardinality string/object columns -> category
    for col in df.select_dtypes("object").columns:
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype("category")
    # float64 -> float32  (halves float memory)
    for col in df.select_dtypes("float64").columns:
        df[col] = df[col].astype("float32")
    # int64 -> smallest fitting int type
    for col in df.select_dtypes("int64").columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")
    # Same optimisations on dim_economic (used directly in Tab 5)
    for col in dim_economic.select_dtypes("object").columns:
        if dim_economic[col].nunique() / len(dim_economic) < 0.5:
            dim_economic[col] = dim_economic[col].astype("category")
    for col in dim_economic.select_dtypes("float64").columns:
        dim_economic[col] = dim_economic[col].astype("float32")
    # ─────────────────────────────────────────────────────────────────

    return df, dim_economic, dim_product, dim_store

df, dim_economic, dim_product, dim_store = load_data()

# â”€â”€â”€ Plotly theme helper â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
CHART_BG   = "rgba(10,10,20,0)"
PAPER_BG   = "rgba(10,10,20,0)"
FONT_COLOR = "#cbd5e1"
GRID_COLOR = "rgba(99,102,241,0.12)"
PURPLE_SEQ = px.colors.sequential.Purp
PALETTE    = ["#818cf8","#c084fc","#f472b6","#34d399","#fbbf24","#60a5fa","#fb923c","#a78bfa","#38bdf8","#4ade80"]

def style_fig(fig, height=420):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family="Inter, sans-serif", color=FONT_COLOR, size=12),
        height=height,
        margin=dict(l=16, r=16, t=36, b=16),
        legend=dict(
            bgcolor="rgba(15,15,30,0.7)",
            bordercolor="rgba(99,102,241,0.25)",
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, tickfont=dict(size=11)),
        colorway=PALETTE,
    )
    return fig


# â”€â”€â”€ Sidebar Filters â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
with st.sidebar:
    st.markdown('<div class="main-title" style="font-size:1.6rem;">ðŸŽ Apple EDA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sales Intelligence Dashboard</div>', unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    st.markdown("### ðŸ” Filters")

    years = sorted(df["year"].unique())
    sel_years = st.multiselect("Year(s)", years, default=years, key="yr")

    all_countries = sorted(df["country"].dropna().unique())
    sel_countries = st.multiselect("Country/Market", all_countries, default=all_countries, key="ct")

    all_categories = sorted(df["category_name"].dropna().unique())
    sel_categories = st.multiselect("Product Category", all_categories, default=all_categories, key="cat")

    promo_opt = st.radio("Promotion Filter", ["All", "Promo Only", "No Promo"], horizontal=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#475569;font-size:0.75rem;'>
    Data covers <b style='color:#818cf8'>1,040,200</b> transactions across
    <b style='color:#818cf8'>19 markets</b>, <b style='color:#818cf8'>177 products</b>
    and <b style='color:#818cf8'>75 stores</b>.<br><br>
    Date range: Jan 2020 â€“ Nov 2024
    </div>
    """, unsafe_allow_html=True)

# Apply filters
mask = (
    df["year"].isin(sel_years)
    & df["country"].isin(sel_countries)
    & df["category_name"].isin(sel_categories)
)
if promo_opt == "Promo Only":
    mask &= df["promo_flag"] == 1
elif promo_opt == "No Promo":
    mask &= df["promo_flag"] == 0

fdf = df[mask].copy()


# â”€â”€â”€ Header â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="main-title">Apple Sales Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-market EDA Â· 2020 â€“ 2024 Â· Powered by Streamlit & Plotly</div>', unsafe_allow_html=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# â”€â”€â”€ KPI Row â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
total_revenue   = fdf["sales_amount_realistic"].sum()
total_units     = fdf["quantity"].sum()
total_txns      = len(fdf)
avg_order_value = fdf["sales_amount_realistic"].mean()
promo_rate      = fdf["promo_flag"].mean() * 100
unique_markets  = fdf["country"].nunique()

def fmt_million(v):
    if v >= 1e9:  return f"${v/1e9:.2f}B"
    if v >= 1e6:  return f"${v/1e6:.2f}M"
    return f"${v:,.0f}"

kpis = [
    ("ðŸ’° Total Revenue",      fmt_million(total_revenue),   "Realistic adj. sales"),
    ("ðŸ“¦ Total Units Sold",   f"{total_units:,}",            "Across all products"),
    ("ðŸ§¾ Transactions",       f"{total_txns:,}",             "Filtered records"),
    ("ðŸ›’ Avg Order Value",    f"${avg_order_value:,.0f}",    "Per transaction"),
    ("ðŸŽ¯ Promo Rate",         f"{promo_rate:.1f}%",          "Transactions on promo"),
    ("ðŸŒ Active Markets",     f"{unique_markets}",           "Countries represented"),
]

cols = st.columns(6)
for col, (label, value, sub) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# â”€â”€â”€ Tabs â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "ðŸ“ˆ Sales Trends",
    "ðŸŒ Market Analysis",
    "ðŸ“± Product Insights",
    "ðŸª Store Performance",
    "ðŸ“Š Economic Factors",
])


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 1 â€“ SALES TRENDS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab1:
    st.markdown('<div class="section-header">ðŸ“ˆ Revenue Over Time</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 1])
    with col_b:
        trend_gran = st.selectbox("Granularity", ["Monthly", "Quarterly", "Yearly"], key="tg")

    if trend_gran == "Monthly":
        ts = fdf.groupby("yearmonth")["sales_amount_realistic"].sum().reset_index()
        ts.columns = ["Period", "Revenue"]
    elif trend_gran == "Quarterly":
        ts = fdf.groupby(["year","quarter"])["sales_amount_realistic"].sum().reset_index()
        ts["Period"] = ts["year"].astype(str) + " " + ts["quarter"]
        ts = ts[["Period","sales_amount_realistic"]].rename(columns={"sales_amount_realistic":"Revenue"})
    else:
        ts = fdf.groupby("year")["sales_amount_realistic"].sum().reset_index()
        ts.columns = ["Period", "Revenue"]
        ts["Period"] = ts["Period"].astype(str)

    fig_trend = px.area(
        ts, x="Period", y="Revenue",
        title="Sales Revenue Trend",
        color_discrete_sequence=["#818cf8"],
    )
    fig_trend.update_traces(
        fill="tozeroy",
        fillcolor="rgba(129,140,248,0.15)",
        line=dict(width=2.5, color="#818cf8"),
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    )
    style_fig(fig_trend, 380)
    st.plotly_chart(fig_trend, width='stretch')

    # â”€â”€ Revenue by category over time
    st.markdown('<div class="section-header">ðŸ“± Category Revenue by Year</div>', unsafe_allow_html=True)
    cat_yr = fdf.groupby(["year","category_name"])["sales_amount_realistic"].sum().reset_index()
    cat_yr.columns = ["Year","Category","Revenue"]
    cat_yr["Year"] = cat_yr["Year"].astype(str)

    fig_cat_yr = px.bar(
        cat_yr, x="Year", y="Revenue", color="Category",
        title="Revenue by Category & Year",
        barmode="group",
        color_discrete_sequence=PALETTE,
    )
    fig_cat_yr.update_traces(hovertemplate="<b>%{x}</b><br>%{fullData.name}: $%{y:,.0f}<extra></extra>")
    style_fig(fig_cat_yr, 380)
    st.plotly_chart(fig_cat_yr, width='stretch')

    # â”€â”€ Monthly seasonality
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">ðŸ“… Monthly Seasonality</div>', unsafe_allow_html=True)
        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        seas = fdf.groupby("month_name")["sales_amount_realistic"].mean().reindex(month_order).reset_index()
        seas.columns = ["Month", "Avg Revenue"]
        fig_seas = px.bar(
            seas, x="Month", y="Avg Revenue",
            title="Avg Monthly Revenue (Seasonality)",
            color="Avg Revenue", color_continuous_scale="Purples",
        )
        fig_seas.update_traces(hovertemplate="<b>%{x}</b><br>Avg: $%{y:,.0f}<extra></extra>")
        style_fig(fig_seas, 360)
        st.plotly_chart(fig_seas, width='stretch')

    with col2:
        st.markdown('<div class="section-header">ðŸŽ¯ Promo vs Non-Promo Revenue</div>', unsafe_allow_html=True)
        promo_ts = fdf.groupby(["yearmonth","promo_flag"])["sales_amount_realistic"].sum().reset_index()
        promo_ts["Promo"] = promo_ts["promo_flag"].map({0:"No Promo", 1:"Promo"})
        fig_promo = px.line(
            promo_ts, x="yearmonth", y="sales_amount_realistic", color="Promo",
            title="Promo vs. Non-Promo Revenue Over Time",
            color_discrete_map={"Promo":"#f472b6","No Promo":"#818cf8"},
        )
        fig_promo.update_traces(hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>")
        style_fig(fig_promo, 360)
        st.plotly_chart(fig_promo, width='stretch')


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 2 â€“ MARKET ANALYSIS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">ðŸŒ Revenue by Country</div>', unsafe_allow_html=True)
        country_rev = (fdf.groupby("country")["sales_amount_realistic"]
                       .sum().sort_values(ascending=False).reset_index())
        country_rev.columns = ["Country","Revenue"]
        fig_country = px.bar(
            country_rev, x="Revenue", y="Country", orientation="h",
            title="Total Revenue by Country",
            color="Revenue", color_continuous_scale="Purples",
        )
        fig_country.update_traces(hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>")
        fig_country.update_layout(yaxis=dict(autorange="reversed"))
        style_fig(fig_country, 500)
        st.plotly_chart(fig_country, width='stretch')

    with col2:
        st.markdown('<div class="section-header">ðŸ—ºï¸ Market Share (Treemap)</div>', unsafe_allow_html=True)
        fig_tree = px.treemap(
            country_rev, path=["Country"], values="Revenue",
            title="Market Share by Country",
            color="Revenue", color_continuous_scale="Purples",
        )
        fig_tree.update_traces(hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<extra></extra>")
        style_fig(fig_tree, 500)
        st.plotly_chart(fig_tree, width='stretch')

    # â”€â”€ Country growth YoY
    st.markdown('<div class="section-header">ðŸ“Š Country Revenue â€“ Year-over-Year</div>', unsafe_allow_html=True)
    cty_yr = fdf.groupby(["country","year"])["sales_amount_realistic"].sum().reset_index()
    cty_yr.columns = ["Country","Year","Revenue"]
    cty_yr["Year"] = cty_yr["Year"].astype(str)
    top10_ct = country_rev["Country"].head(10).tolist()
    fig_cty_yr = px.line(
        cty_yr[cty_yr["Country"].isin(top10_ct)],
        x="Year", y="Revenue", color="Country",
        title="Top-10 Country Revenue Trend",
        markers=True,
        color_discrete_sequence=PALETTE,
    )
    fig_cty_yr.update_traces(hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>")
    style_fig(fig_cty_yr, 380)
    st.plotly_chart(fig_cty_yr, width='stretch')

    # â”€â”€ Units sold by country
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">ðŸ“¦ Units Sold by Country</div>', unsafe_allow_html=True)
        units_ct = fdf.groupby("country")["quantity"].sum().sort_values(ascending=False).reset_index()
        units_ct.columns = ["Country","Units"]
        fig_units = px.bar(
            units_ct.head(15), x="Country", y="Units",
            title="Units Sold â€“ Top 15 Countries",
            color="Units", color_continuous_scale="Blues",
        )
        style_fig(fig_units, 360)
        st.plotly_chart(fig_units, width='stretch')

    with col4:
        st.markdown('<div class="section-header">ðŸ’¸ Avg Order Value by Country</div>', unsafe_allow_html=True)
        aov_ct = fdf.groupby("country")["sales_amount_realistic"].mean().sort_values(ascending=False).reset_index()
        aov_ct.columns = ["Country","AOV"]
        fig_aov = px.bar(
            aov_ct.head(15), x="Country", y="AOV",
            title="Avg Order Value â€“ Top 15 Countries",
            color="AOV", color_continuous_scale="Pinkyl",
        )
        fig_aov.update_traces(hovertemplate="<b>%{x}</b><br>AOV: $%{y:,.0f}<extra></extra>")
        style_fig(fig_aov, 360)
        st.plotly_chart(fig_aov, width='stretch')


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 3 â€“ PRODUCT INSIGHTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">ðŸ† Revenue by Category</div>', unsafe_allow_html=True)
        cat_rev = (fdf.groupby("category_name")["sales_amount_realistic"]
                   .sum().sort_values(ascending=False).reset_index())
        cat_rev.columns = ["Category","Revenue"]
        fig_cat = px.pie(
            cat_rev, names="Category", values="Revenue",
            title="Revenue Share by Category",
            color_discrete_sequence=PALETTE,
            hole=0.45,
        )
        fig_cat.update_traces(hovertemplate="<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>")
        style_fig(fig_cat, 400)
        st.plotly_chart(fig_cat, width='stretch')

    with col2:
        st.markdown('<div class="section-header">ðŸ“Š Units Sold by Category</div>', unsafe_allow_html=True)
        cat_units = (fdf.groupby("category_name")["quantity"]
                     .sum().sort_values(ascending=False).reset_index())
        cat_units.columns = ["Category","Units"]
        fig_cu = px.bar(
            cat_units, x="Category", y="Units",
            title="Units Sold by Category",
            color="Units", color_continuous_scale="Purples",
        )
        fig_cu.update_xaxes(tickangle=30)
        style_fig(fig_cu, 400)
        st.plotly_chart(fig_cu, width='stretch')

    # â”€â”€ Top products
    st.markdown('<div class="section-header">ðŸŒŸ Top Products by Revenue</div>', unsafe_allow_html=True)
    n_top = st.slider("Number of top products to show", 5, 30, 15, key="ntp")
    top_prod = (fdf.groupby(["product_name","category_name"])["sales_amount_realistic"]
                .sum().sort_values(ascending=False).head(n_top).reset_index())
    top_prod.columns = ["Product","Category","Revenue"]

    fig_tp = px.bar(
        top_prod, x="Revenue", y="Product", color="Category",
        orientation="h", title=f"Top {n_top} Products by Revenue",
        color_discrete_sequence=PALETTE,
    )
    fig_tp.update_layout(yaxis=dict(autorange="reversed"))
    fig_tp.update_traces(hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>")
    style_fig(fig_tp, max(380, n_top*22))
    st.plotly_chart(fig_tp, width='stretch')

    # â”€â”€ Price distribution
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">ðŸ’² Price Distribution by Category</div>', unsafe_allow_html=True)
        fig_price = px.box(
            fdf.dropna(subset=["category_name","price"]),
            x="category_name", y="price", color="category_name",
            title="Price Distribution per Category",
            color_discrete_sequence=PALETTE,
        )
        fig_price.update_xaxes(tickangle=30)
        fig_price.update_layout(showlegend=False)
        style_fig(fig_price, 400)
        st.plotly_chart(fig_price, width='stretch')

    with col4:
        st.markdown('<div class="section-header">ðŸ“¦ Quantity Distribution</div>', unsafe_allow_html=True)
        fig_qty = px.histogram(
            fdf, x="quantity", nbins=10,
            title="Quantity per Transaction",
            color_discrete_sequence=["#818cf8"],
        )
        fig_qty.update_traces(hovertemplate="Qty: %{x}<br>Count: %{y}<extra></extra>")
        style_fig(fig_qty, 400)
        st.plotly_chart(fig_qty, width='stretch')

    # â”€â”€ Promo effect per category
    st.markdown('<div class="section-header">ðŸŽ¯ Promo Impact by Category</div>', unsafe_allow_html=True)
    promo_cat = (fdf.groupby(["category_name","promo_flag"])["sales_amount_realistic"]
                 .mean().reset_index())
    promo_cat["Promo"] = promo_cat["promo_flag"].map({0:"No Promo", 1:"Promo"})
    fig_pi = px.bar(
        promo_cat, x="category_name", y="sales_amount_realistic", color="Promo",
        barmode="group",
        title="Avg Transaction Value: Promo vs No-Promo",
        color_discrete_map={"Promo":"#f472b6", "No Promo":"#818cf8"},
    )
    fig_pi.update_xaxes(tickangle=30)
    style_fig(fig_pi, 380)
    st.plotly_chart(fig_pi, width='stretch')


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 4 â€“ STORE PERFORMANCE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">ðŸª Top Stores by Revenue</div>', unsafe_allow_html=True)
        store_rev = (fdf.groupby(["store_id","store_name","city","country"])["sales_amount_realistic"]
                     .sum().sort_values(ascending=False).reset_index().head(20))
        store_rev.columns = ["Store ID","Store Name","City","Country","Revenue"]
        fig_st = px.bar(
            store_rev, x="Revenue", y="Store Name",
            orientation="h", color="Country",
            title="Top 20 Stores by Revenue",
            color_discrete_sequence=PALETTE,
        )
        fig_st.update_layout(yaxis=dict(autorange="reversed"), showlegend=False)
        fig_st.update_traces(hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>")
        style_fig(fig_st, 560)
        st.plotly_chart(fig_st, width='stretch')

    with col2:
        st.markdown('<div class="section-header">ðŸ“Š Store Count by Country</div>', unsafe_allow_html=True)
        store_ct = (dim_store.groupby("country_norm_mapped").size()
                    .sort_values(ascending=False).reset_index())
        store_ct.columns = ["Country","Store Count"]
        store_ct["Country"] = store_ct["Country"].str.title()
        fig_sc = px.bar(
            store_ct, x="Country", y="Store Count",
            title="Number of Stores per Country",
            color="Store Count", color_continuous_scale="Purples",
        )
        fig_sc.update_xaxes(tickangle=40)
        style_fig(fig_sc, 380)
        st.plotly_chart(fig_sc, width='stretch')

        st.markdown('<div class="section-header">ðŸ·ï¸ Revenue per Store by Country</div>', unsafe_allow_html=True)
        rev_per_store = (fdf.groupby("country")["sales_amount_realistic"].sum()
                         / fdf.groupby("country")["store_id"].nunique())
        rev_per_store = rev_per_store.sort_values(ascending=False).reset_index()
        rev_per_store.columns = ["Country","Rev per Store"]
        fig_rps = px.bar(
            rev_per_store, x="Country", y="Rev per Store",
            title="Avg Revenue per Store",
            color="Rev per Store", color_continuous_scale="Pinkyl",
        )
        fig_rps.update_xaxes(tickangle=40)
        fig_rps.update_traces(hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>")
        style_fig(fig_rps, 340)
        st.plotly_chart(fig_rps, width='stretch')

    # â”€â”€ Store revenue heatmap (store x year)
    st.markdown('<div class="section-header">ðŸ”¥ Store Revenue Heatmap (Top 20 Stores Ã— Year)</div>', unsafe_allow_html=True)
    top20_stores = (fdf.groupby("store_name")["sales_amount_realistic"]
                    .sum().sort_values(ascending=False).head(20).index.tolist())
    heat_df = (fdf[fdf["store_name"].isin(top20_stores)]
               .groupby(["store_name","year"])["sales_amount_realistic"]
               .sum().reset_index())
    heat_piv = heat_df.pivot(index="store_name", columns="year", values="sales_amount_realistic").fillna(0)
    fig_hm = px.imshow(
        heat_piv,
        color_continuous_scale="Purples",
        title="Revenue Heatmap â€“ Top 20 Stores by Year",
        labels=dict(color="Revenue ($)"),
        aspect="auto",
    )
    fig_hm.update_traces(hovertemplate="Store: <b>%{y}</b><br>Year: %{x}<br>Revenue: $%{z:,.0f}<extra></extra>")
    style_fig(fig_hm, 520)
    st.plotly_chart(fig_hm, width='stretch')


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TAB 5 â€“ ECONOMIC FACTORS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
with tab5:
    st.markdown('<div class="section-header">ðŸŒ Macroeconomic Context by Country</div>', unsafe_allow_html=True)

    econ_agg = (dim_economic.groupby("country_norm_mapped")
                .agg(avg_fx=("exchange_rate","mean"),
                     avg_inflation=("inflation_rate","mean"),
                     avg_gdp=("gdp_per_capita","mean"),
                     avg_season=("season_factor","mean"))
                .reset_index())
    econ_agg["country"] = econ_agg["country_norm_mapped"].str.title()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">ðŸ’¹ GDP per Capita by Country</div>', unsafe_allow_html=True)
        fig_gdp = px.bar(
            econ_agg.sort_values("avg_gdp", ascending=False),
            x="country", y="avg_gdp",
            title="Avg GDP per Capita (USD)",
            color="avg_gdp", color_continuous_scale="Purples",
        )
        fig_gdp.update_xaxes(tickangle=40)
        fig_gdp.update_traces(hovertemplate="<b>%{x}</b><br>GDP: $%{y:,.0f}<extra></extra>")
        style_fig(fig_gdp, 380)
        st.plotly_chart(fig_gdp, width='stretch')

    with col2:
        st.markdown('<div class="section-header">ðŸ“‰ Avg Inflation Rate by Country</div>', unsafe_allow_html=True)
        fig_inf = px.bar(
            econ_agg.sort_values("avg_inflation", ascending=False),
            x="country", y="avg_inflation",
            title="Avg Inflation Rate (%)",
            color="avg_inflation", color_continuous_scale="RdPu",
        )
        fig_inf.update_xaxes(tickangle=40)
        fig_inf.update_traces(hovertemplate="<b>%{x}</b><br>Inflation: %{y:.2f}%<extra></extra>")
        style_fig(fig_inf, 380)
        st.plotly_chart(fig_inf, width='stretch')

    # â”€â”€ GDP vs Revenue scatter
    st.markdown('<div class="section-header">ðŸ”— GDP vs. Sales Revenue Correlation</div>', unsafe_allow_html=True)
    country_rev_econ = (fdf.groupby("country")["sales_amount_realistic"]
                        .sum().reset_index().rename(columns={"sales_amount_realistic": "Revenue"}))
    econ_scatter = econ_agg.merge(country_rev_econ, on="country", how="inner")

    fig_scatter = px.scatter(
        econ_scatter, x="avg_gdp", y="Revenue",
        size="Revenue", color="country",
        hover_name="country",
        title="GDP per Capita vs. Total Revenue by Country",
        labels={"avg_gdp":"Avg GDP per Capita ($)", "Revenue":"Total Revenue ($)"},
        color_discrete_sequence=PALETTE,
    )
    fig_scatter.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>GDP: $%{x:,.0f}<br>Revenue: $%{y:,.0f}<extra></extra>"
    )
    style_fig(fig_scatter, 420)
    st.plotly_chart(fig_scatter, width='stretch')

    # â”€â”€ Exchange rate & Inflation trends
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">ðŸ’± Exchange Rate Over Time (Selected Countries)</div>', unsafe_allow_html=True)
        sel_econ_ct = st.multiselect(
            "Countries for FX chart",
            sorted(dim_economic["country_norm_mapped"].str.title().unique()),
            default=["Japan","United Kingdom","Australia","Canada"],
            key="fx_ct",
        )
        econ_ts = dim_economic.copy()
        econ_ts["country"] = econ_ts["country_norm_mapped"].str.title()
        econ_ts_f = econ_ts[econ_ts["country"].isin(sel_econ_ct)]
        fig_fx = px.line(
            econ_ts_f, x="sale_date", y="exchange_rate", color="country",
            title="Exchange Rate vs USD",
            color_discrete_sequence=PALETTE,
        )
        fig_fx.update_traces(hovertemplate="<b>%{x}</b><br>FX: %{y:.3f}<extra></extra>")
        style_fig(fig_fx, 380)
        st.plotly_chart(fig_fx, width='stretch')

    with col4:
        st.markdown('<div class="section-header">ðŸ“ˆ Inflation Rate Over Time</div>', unsafe_allow_html=True)
        fig_inf_ts = px.line(
            econ_ts_f.dropna(subset=["inflation_rate"]),
            x="sale_date", y="inflation_rate", color="country",
            title="Inflation Rate Over Time",
            color_discrete_sequence=PALETTE,
        )
        fig_inf_ts.update_traces(hovertemplate="<b>%{x}</b><br>Inflation: %{y:.2f}%<extra></extra>")
        style_fig(fig_inf_ts, 380)
        st.plotly_chart(fig_inf_ts, width='stretch')

    # â”€â”€ Season factor
    st.markdown('<div class="section-header">ðŸŒ¤ï¸ Season Factor Distribution</div>', unsafe_allow_html=True)
    fig_sf = px.histogram(
        dim_economic, x="season_factor", nbins=20,
        color_discrete_sequence=["#c084fc"],
        title="Distribution of Season Factor Across All Records",
    )
    fig_sf.update_traces(hovertemplate="Season Factor: %{x:.2f}<br>Count: %{y}<extra></extra>")
    style_fig(fig_sf, 320)
    st.plotly_chart(fig_sf, width='stretch')


# â”€â”€â”€ Footer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center;color:#334155;font-size:0.78rem;padding-bottom:12px;'>
    ðŸŽ Apple Sales EDA Dashboard Â· Built with Streamlit & Plotly Â· Data: 2020â€“2024
</div>
""", unsafe_allow_html=True)

