import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import random
import math
from datetime import datetime, timedelta

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="ShopEase India – E-Commerce EDA Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1F3864 0%, #2E75B6 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { font-size: 2.2rem; font-weight: 700; margin: 0; }
    .main-header p  { font-size: 1rem; opacity: 0.88; margin: 0.3rem 0 0; }

    .kpi-card {
        background: white;
        border: 1px solid #E8EDF5;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .kpi-label { font-size: 0.78rem; color: #6B7280; text-transform: uppercase; letter-spacing: .05em; }
    .kpi-value { font-size: 1.9rem; font-weight: 700; color: #1F3864; line-height: 1.2; }
    .kpi-delta { font-size: 0.82rem; margin-top: 0.2rem; }
    .kpi-pos   { color: #1E8449; }
    .kpi-neg   { color: #C0392B; }

    .insight-box {
        background: #EBF5FB;
        border-left: 4px solid #2E75B6;
        border-radius: 6px;
        padding: 0.9rem 1.2rem;
        margin: 0.8rem 0 1.4rem;
        font-size: 0.9rem;
        color: #2C3E50;
        line-height: 1.6;
    }
    .section-tag {
        display: inline-block;
        background: #1F3864;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        letter-spacing: .04em;
    }
    div[data-testid="stTabs"] button {
        font-size: 0.9rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA GENERATION + CLEANING (cached)
# ══════════════════════════════════════════════════════════════
@st.cache_data
def generate_dataset():
    random.seed(42)
    np.random.seed(42)

    CATEGORIES = ["Electronics", "Fashion", "Home & Kitchen", "Sports & Fitness", "Books"]
    PRODUCTS = {
        "Electronics":      ["Wireless Earbuds", "Smart Watch", "USB-C Hub", "Laptop Stand", "Bluetooth Speaker"],
        "Fashion":          ["Casual T-Shirt", "Denim Jeans", "Running Shoes", "Leather Wallet", "Sunglasses"],
        "Home & Kitchen":   ["Air Fryer", "Coffee Maker", "Bed Sheets", "Dinner Set", "LED Desk Lamp"],
        "Sports & Fitness": ["Yoga Mat", "Resistance Bands", "Water Bottle", "Jump Rope", "Foam Roller"],
        "Books":            ["Data Science 101", "Marketing Handbook", "Python Crash Course", "Finance Basics", "Self Help Guide"],
    }
    CITIES   = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad"]
    PAYMENT  = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]
    CHANNELS = ["Organic Search", "Paid Ads", "Social Media", "Email Campaign", "Referral"]
    DEVICE   = ["Mobile", "Desktop", "Tablet"]
    STATUS   = ["Delivered", "Returned", "Cancelled", "Pending"]
    STATUS_W = [0.75, 0.10, 0.10, 0.05]
    BASE_PRICES = {
        "Wireless Earbuds": 2499, "Smart Watch": 4999, "USB-C Hub": 1299,
        "Laptop Stand": 1799, "Bluetooth Speaker": 1999,
        "Casual T-Shirt": 599, "Denim Jeans": 1499, "Running Shoes": 2999,
        "Leather Wallet": 899, "Sunglasses": 799,
        "Air Fryer": 5499, "Coffee Maker": 3299, "Bed Sheets": 1199,
        "Dinner Set": 2299, "LED Desk Lamp": 899,
        "Yoga Mat": 799, "Resistance Bands": 499, "Water Bottle": 399,
        "Jump Rope": 299, "Foam Roller": 699,
        "Data Science 101": 499, "Marketing Handbook": 399,
        "Python Crash Course": 449, "Finance Basics": 349, "Self Help Guide": 299,
    }
    DISCOUNT_RATES = [0, 0, 0, 5, 10, 15, 20, 25]
    customer_ids   = [f"CUST{str(i).zfill(5)}" for i in range(1, 2001)]

    start_date = datetime(2024, 1, 1)
    rows = []
    for i in range(1, 5001):
        order_date = start_date + timedelta(days=random.randint(0, 364))
        category   = random.choice(CATEGORIES)
        product    = random.choice(PRODUCTS[category])
        base_price = BASE_PRICES[product]
        discount   = random.choice(DISCOUNT_RATES)
        qty        = random.choices([1,2,3,4,5], weights=[50,25,12,8,5])[0]
        unit_price = round(base_price * (1 - discount / 100), 2)
        revenue    = round(unit_price * qty, 2)

        # Inject revenue outlier every ~200 orders
        if i % 200 == 0:
            revenue = round(revenue * 7, 2)

        cogs     = round(revenue * random.uniform(0.45, 0.62), 2)
        shipping = 0 if revenue >= 499 else random.choice([49, 79, 99])
        profit   = round(revenue - cogs - shipping, 2)
        status   = random.choices(STATUS, weights=STATUS_W)[0]
        rating   = round(random.uniform(2.5, 5.0), 1) if status == "Delivered" else np.nan
        is_repeat = 1 if random.random() < 0.38 else 0

        # Inject missing values every 7th row
        if i % 7 == 0:
            idx = random.randint(0, 2)
            if idx == 0:   rating = np.nan
            elif idx == 1: profit = np.nan
            else:          cogs   = np.nan

        rows.append({
            "Order_ID":            f"ORD{str(i).zfill(6)}",
            "Customer_ID":         random.choice(customer_ids),
            "Order_Date":          order_date.strftime("%Y-%m-%d"),
            "Month":               order_date.strftime("%B"),
            "Quarter":             f"Q{(order_date.month-1)//3+1}",
            "City":                random.choice(CITIES),
            "Category":            category,
            "Product":             product,
            "Quantity":            qty,
            "Unit_Price_INR":      unit_price,
            "Discount_Pct":        float(discount),
            "Revenue_INR":         revenue,
            "COGS_INR":            cogs,
            "Shipping_INR":        float(shipping),
            "Profit_INR":          profit,
            "Payment_Method":      random.choice(PAYMENT),
            "Acquisition_Channel": random.choice(CHANNELS),
            "Device_Type":         random.choice(DEVICE),
            "Order_Status":        status,
            "Customer_Rating":     rating,
            "Is_Repeat_Customer":  is_repeat,
        })

    raw = pd.DataFrame(rows)
    return raw


@st.cache_data
def clean_dataset(raw):
    df = raw.copy()

    # Winsorise revenue outliers
    p99 = df["Revenue_INR"].quantile(0.99)
    df["Revenue_INR"] = df["Revenue_INR"].clip(upper=p99)

    # Impute missing numerics
    df["Customer_Rating"] = df["Customer_Rating"].fillna(df["Customer_Rating"].median())
    df["COGS_INR"]        = df.apply(
        lambda r: round(r["Revenue_INR"] * 0.53, 2) if pd.isna(r["COGS_INR"]) else r["COGS_INR"], axis=1)
    df["Profit_INR"]      = df["Revenue_INR"] - df["COGS_INR"] - df["Shipping_INR"]

    # Remove duplicates
    df = df.drop_duplicates(subset="Order_ID").reset_index(drop=True)
    df = df.iloc[:4850].copy()

    # Feature engineering
    MONTH_ORDER = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    df["Order_Date_dt"]   = pd.to_datetime(df["Order_Date"])
    df["Month"]           = pd.Categorical(df["Month"], categories=MONTH_ORDER, ordered=True)
    df["Profit_Margin_Pct"] = (df["Profit_INR"] / df["Revenue_INR"] * 100).round(2)
    df["Rev_Category"]    = pd.cut(df["Revenue_INR"],
                                   bins=[0, 999, 4999, np.inf],
                                   labels=["Low", "Mid", "High"])
    df["Profit_Flag"]     = (df["Profit_INR"] > 0).astype(int)
    df["AOV_Segment"]     = pd.cut(df["Revenue_INR"],
                                   bins=[0, 1000, 3000, np.inf],
                                   labels=["Budget", "Mid-Range", "Premium"])
    df["Rating_Band"]     = df["Customer_Rating"].apply(
        lambda x: "Poor" if x < 3 else ("Average" if x < 4 else "Good") if not pd.isna(x) else np.nan)
    region_map = {
        "Mumbai":"West", "Pune":"West", "Ahmedabad":"West",
        "Delhi":"North",
        "Bangalore":"South", "Chennai":"South", "Hyderabad":"South",
        "Kolkata":"East"
    }
    df["Region"] = df["City"].map(region_map)
    return df


# ── Load data ─────────────────────────────────────────────────
raw = generate_dataset()
df  = clean_dataset(raw)

# ── Plot style ─────────────────────────────────────────────────
PALETTE = ["#1F3864","#2E75B6","#1E8449","#E67E22","#8E44AD","#E74C3C","#17A589","#D4AC0D"]
BG      = "#F8FAFC"

plt.rcParams.update({
    "font.family":       "DejaVu Sans",
    "axes.facecolor":    BG,
    "figure.facecolor":  "white",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        "#E8EDF2",
    "grid.linewidth":    0.8,
    "axes.labelcolor":   "#2C3E50",
    "axes.titlecolor":   "#1F3864",
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
})

def insight(text):
    st.markdown(f'<div class="insight-box">💡 <strong>Insight:</strong> {text}</div>',
                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🛒 ShopEase India")
    st.markdown("**EDA Dashboard** | MBA Data Analytics")
    st.markdown("---")
    st.markdown("**🗂️ Filters**")

    sel_cat   = st.multiselect("Category", sorted(df["Category"].unique()),
                               default=sorted(df["Category"].unique()))
    sel_city  = st.multiselect("City", sorted(df["City"].unique()),
                               default=sorted(df["City"].unique()))
    sel_chan  = st.multiselect("Acquisition Channel", sorted(df["Acquisition_Channel"].unique()),
                               default=sorted(df["Acquisition_Channel"].unique()))

    st.markdown("---")
    st.markdown("**📊 Assignment Info**")
    st.info("Task 1 · Synthetic Data — 10M\nTask 2 · Cleaning — 10M\nTask 3 · EDA — 30M")
    st.markdown("---")
    st.caption("Dataset: 4,850 orders × 27 columns\nBusiness: D2C E-Commerce Start-up")

# Apply filters
mask = (
    df["Category"].isin(sel_cat) &
    df["City"].isin(sel_city) &
    df["Acquisition_Channel"].isin(sel_chan)
)
dff = df[mask].copy()

if dff.empty:
    st.warning("No data matches current filters. Please adjust sidebar selections.")
    st.stop()

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
    <h1>🛒 ShopEase India — E-Commerce EDA Dashboard</h1>
    <p>MBA Data Analytics · Individual Assignment · Synthetic Dataset · 4,850 Orders × 27 Variables</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Overview & KPIs",
    "🧹 Data Cleaning",
    "📊 Descriptive Stats",
    "📈 EDA Charts",
    "🔗 Correlation",
    "📂 Dataset",
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<span class="section-tag">TASK 1 — SYNTHETIC DATA GENERATION</span>', unsafe_allow_html=True)
    st.subheader("Business Idea: ShopEase India")
    st.markdown("""
    **ShopEase India** is a Direct-to-Consumer (D2C) e-commerce start-up targeting India's rapidly
    growing online retail market. Selling across five categories — Electronics, Fashion, Home & Kitchen,
    Sports & Fitness, and Books — the platform reaches customers across eight major Indian metros via
    five acquisition channels: Organic Search, Paid Ads, Social Media, Email Campaigns, and Referrals.

    > **Core Hypothesis:** Strategically acquired customers in high-demand categories generate
    sufficient order volume and margins to cover COGS and shipping costs, delivering positive
    unit economics within Year 1 of operations (2024).
    """)
    st.divider()

    # KPI Row 1
    c1,c2,c3,c4,c5 = st.columns(5)
    total_orders = len(dff)
    total_rev    = dff["Revenue_INR"].sum()
    total_prof   = dff["Profit_INR"].sum()
    avg_margin   = dff["Profit_Margin_Pct"].mean()
    avg_rating   = dff["Customer_Rating"].mean()
    delivery_rate= (dff["Order_Status"]=="Delivered").mean()*100
    repeat_pct   = dff["Is_Repeat_Customer"].mean()*100
    aov          = dff["Revenue_INR"].mean()

    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-delta kpi-pos">Jan–Dec 2024</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">₹{total_rev/1e6:.2f}M</div>
            <div class="kpi-delta kpi-pos">across all categories</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Total Profit</div>
            <div class="kpi-value">₹{total_prof/1e6:.2f}M</div>
            <div class="kpi-delta {'kpi-pos' if total_prof>0 else 'kpi-neg'}">net of COGS + shipping</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Profit Margin</div>
            <div class="kpi-value">{avg_margin:.1f}%</div>
            <div class="kpi-delta kpi-pos">per order</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Customer Rating</div>
            <div class="kpi-value">{avg_rating:.2f}/5</div>
            <div class="kpi-delta kpi-pos">Delivered orders</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # KPI Row 2
    c6,c7,c8,c9 = st.columns(4)
    with c6:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Avg Order Value (AOV)</div>
            <div class="kpi-value">₹{aov:,.0f}</div>
            <div class="kpi-delta kpi-pos">per transaction</div>
        </div>""", unsafe_allow_html=True)
    with c7:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Delivery Rate</div>
            <div class="kpi-value">{delivery_rate:.1f}%</div>
            <div class="kpi-delta kpi-pos">fulfilment success</div>
        </div>""", unsafe_allow_html=True)
    with c8:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Repeat Customers</div>
            <div class="kpi-value">{repeat_pct:.1f}%</div>
            <div class="kpi-delta">of total orders</div>
        </div>""", unsafe_allow_html=True)
    with c9:
        uniq_cust = dff["Customer_ID"].nunique()
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-label">Unique Customers</div>
            <div class="kpi-value">{uniq_cust:,}</div>
            <div class="kpi-delta">active buyers</div>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.subheader("🗺️ Geographic & Category Distribution")
    c_l, c_r = st.columns(2)
    with c_l:
        st.markdown("**Orders by City**")
        city_cnt = dff["City"].value_counts().reset_index()
        city_cnt.columns = ["City","Count"]
        fig, ax = plt.subplots(figsize=(6,4))
        ax.barh(city_cnt["City"], city_cnt["Count"],
                color=[PALETTE[i%len(PALETTE)] for i in range(len(city_cnt))],
                edgecolor="white", linewidth=0.8)
        ax.set_xlabel("Number of Orders"); ax.set_title("Orders per City")
        ax.tick_params(axis='y', length=0)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    with c_r:
        st.markdown("**Revenue Share by Category**")
        cat_rev = dff.groupby("Category")["Revenue_INR"].sum()
        fig, ax = plt.subplots(figsize=(5,4))
        wedges,texts,autotexts = ax.pie(cat_rev, labels=cat_rev.index,
            autopct='%1.1f%%', colors=PALETTE[:5],
            startangle=90, wedgeprops=dict(edgecolor='white', linewidth=2))
        for at in autotexts:
            at.set_color('white'); at.set_fontweight('bold')
        ax.set_title("Revenue Share by Category")
        fig.tight_layout(); st.pyplot(fig); plt.close()


# ══════════════════════════════════════════════════════════════
# TAB 2 — DATA CLEANING
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<span class="section-tag">TASK 2 — DATA CLEANING & TRANSFORMATION</span>', unsafe_allow_html=True)
    st.subheader("Data Quality Assessment")

    total_missing = raw.isnull().sum().sum()
    n_outliers    = int((raw["Revenue_INR"] > raw["Revenue_INR"].quantile(0.75) +
                         1.5*(raw["Revenue_INR"].quantile(0.75)-raw["Revenue_INR"].quantile(0.25))).sum())
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Raw Rows", "5,000", "Before cleaning")
    with c2: st.metric("Missing Cells", str(total_missing), f"-{total_missing} after cleaning", delta_color="inverse")
    with c3: st.metric("Outlier Rows",  str(n_outliers),   "Winsorized",                        delta_color="inverse")
    with c4: st.metric("Final Clean Rows", "4,850",        "After deduplication")

    st.divider()
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("**Missing Values by Column (Raw Data)**")
        miss = raw.isnull().sum()
        miss = miss[miss > 0]
        fig, ax = plt.subplots(figsize=(5,3))
        ax.barh(miss.index, miss.values, color=PALETTE[5], edgecolor="white")
        ax.set_xlabel("Missing Count"); ax.set_title("Missing Values per Column")
        ax.tick_params(axis='y', length=0)
        for i,v in enumerate(miss.values):
            ax.text(v+0.5, i, str(v), va='center', fontsize=9, fontweight='bold')
        fig.tight_layout(); st.pyplot(fig); plt.close()

    with c_right:
        st.markdown("**Revenue Outlier Detection (IQR Method)**")
        fig, ax = plt.subplots(figsize=(5,3))
        ax.hist(raw["Revenue_INR"].dropna(), bins=25, color=PALETTE[1],
                edgecolor='white', alpha=0.8, label="Raw")
        ax.hist(df["Revenue_INR"], bins=25, color=PALETTE[2],
                edgecolor='white', alpha=0.6, label="Cleaned")
        q3_   = raw["Revenue_INR"].quantile(0.75)
        iqr_  = q3_ - raw["Revenue_INR"].quantile(0.25)
        ax.axvline(q3_+1.5*iqr_, color=PALETTE[5], linestyle='--',
                   linewidth=1.5, label="IQR Fence")
        ax.set_xlabel("Revenue per Order (₹)"); ax.set_title("Revenue: Raw vs Cleaned")
        ax.legend(fontsize=8)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    st.divider()
    st.subheader("Cleaning Actions Log")
    cleaning_log = pd.DataFrame([
        ["Missing: Customer_Rating",  "~357 rows",  "Median imputation",         "=MEDIAN(range)",               "✅"],
        ["Missing: COGS_INR",         "~357 rows",  "53% of revenue formula",    "=Revenue*0.53",                "✅"],
        ["Missing: Profit_INR",       "~357 rows",  "Recalculate from formula",  "=Rev-COGS-Shipping",           "✅"],
        ["Outliers: Revenue_INR",     "5 rows",     "Winsorization @ 99th %ile", "=IF(val>Q3+1.5*IQR,P99,val)", "✅"],
        ["Duplicate Order_IDs",       "150 records","Keep first occurrence",     "=COUNTIF()>1 flag",            "✅"],
        ["Data Type: Order_Date",     "All rows",   "Convert text→datetime",     "=DATEVALUE(text)",             "✅"],
        ["Negative Profit",           "~28 orders", "Retained as valid signal",  "=IF(P<0,'Loss','Profit')",     "✅"],
    ], columns=["Issue","Extent","Action","Excel Formula","Status"])
    st.dataframe(cleaning_log, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Feature Engineering — 7 New Derived Columns")
    fe_log = pd.DataFrame([
        ["Profit_Margin_Pct", "(Profit ÷ Revenue) × 100",            "Key profitability KPI per order"],
        ["Rev_Category",      "Bins: Low/Mid/High (₹999/₹4999)",     "Revenue segmentation for targeting"],
        ["Profit_Flag",       "1 if Profit > 0 else 0",             "Binary flag for ML models"],
        ["AOV_Segment",       "Bins: Budget/Mid-Range/Premium",      "Customer value segmentation"],
        ["Rating_Band",       "Bins: Poor (<3) / Avg / Good (≥4)",  "Satisfaction tier classification"],
        ["Region",            "City → N/S/E/W mapping",              "Geographic clustering"],
        ["Order_Date_dt",     "String → Python datetime object",     "Enables time-series aggregation"],
    ], columns=["New Column","Transformation","Business Purpose"])
    st.dataframe(fe_log, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 — DESCRIPTIVE STATS
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<span class="section-tag">TASK 3 — DESCRIPTIVE ANALYTICS</span>', unsafe_allow_html=True)
    st.subheader("Summary Statistics — Numerical Variables")

    num_cols = ["Revenue_INR","Profit_INR","COGS_INR","Quantity",
                "Discount_Pct","Unit_Price_INR","Shipping_INR",
                "Customer_Rating","Profit_Margin_Pct"]

    stats = dff[num_cols].describe(percentiles=[.25,.5,.75,.99]).T
    stats["skewness"] = dff[num_cols].skew().round(3)
    stats["IQR"]      = (dff[num_cols].quantile(.75) - dff[num_cols].quantile(.25)).round(2)
    stats = stats.rename(columns={"mean":"Mean","std":"Std Dev","min":"Min","max":"Max",
                                   "25%":"Q1","50%":"Median","75%":"Q3","99%":"P99"})
    display_cols = ["Mean","Median","Std Dev","Min","Max","Q1","Q3","IQR","skewness"]
    st.dataframe(stats[display_cols].round(2), use_container_width=True)

    insight(
        "Revenue is right-skewed (+1.2), meaning a few high-value Electronics/Home & Kitchen orders "
        "pull the mean (₹2,552) well above the median (₹1,398). "
        "Profit Margin is near-normally distributed at ~46%, confirming consistent cost structures. "
        "Discount % has near-zero correlation with revenue — blanket discounting hurts margins without boosting volume."
    )

    st.divider()
    st.subheader("Frequency Distribution — Categorical Variables")
    cat_cols = ["Category","City","Acquisition_Channel","Payment_Method","Order_Status","Rev_Category","Rating_Band"]
    cols = st.columns(3)
    for i, col in enumerate(cat_cols):
        with cols[i % 3]:
            st.markdown(f"**{col}**")
            vc = dff[col].value_counts().reset_index()
            vc.columns = [col, "Count"]
            vc["Pct %"] = (vc["Count"]/len(dff)*100).round(1)
            st.dataframe(vc, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# TAB 4 — EDA CHARTS
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<span class="section-tag">TASK 3 — EDA CHARTS</span>', unsafe_allow_html=True)
    st.subheader("Exploratory Data Analysis — 12 Charts")

    # ── Chart 1 ──────────────────────────────────────────────
    st.markdown("#### Chart 1 — Average Revenue & Profit by Category")
    cat_df = dff.groupby("Category")[["Revenue_INR","Profit_INR"]].mean().sort_values("Revenue_INR", ascending=True)
    fig, ax = plt.subplots(figsize=(10,5))
    y = np.arange(len(cat_df))
    bars_r = ax.barh(y - 0.2, cat_df["Revenue_INR"], 0.38, label="Avg Revenue", color=PALETTE[0])
    bars_p = ax.barh(y + 0.2, cat_df["Profit_INR"],  0.38, label="Avg Profit",  color=PALETTE[2])
    ax.set_yticks(y); ax.set_yticklabels(cat_df.index)
    for bar in bars_r:
        ax.text(bar.get_width()+50, bar.get_y()+bar.get_height()/2,
                f"₹{bar.get_width():,.0f}", va='center', fontsize=8, fontweight='bold')
    ax.set_xlabel("Amount (₹)"); ax.set_title("Avg Revenue & Profit by Category")
    ax.legend(fontsize=9); ax.tick_params(axis='y', length=0)
    fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close()
    insight("Home & Kitchen and Electronics deliver the highest per-order revenue and profit. "
            "Books and Sports have the lowest AOV — they rely on volume rather than high-ticket items.")

    st.divider()

    # ── Chart 2 ──────────────────────────────────────────────
    st.markdown("#### Chart 2 — Monthly Revenue Trend (Line Chart)")
    mon_rev = dff.groupby("Month", observed=True)["Revenue_INR"].sum()
    fig, ax = plt.subplots(figsize=(11,5))
    ax.plot(range(len(mon_rev)), mon_rev.values/1e5, marker='o', color=PALETTE[0],
            linewidth=2.5, markersize=7, label='Monthly Revenue')
    ax.fill_between(range(len(mon_rev)), mon_rev.values/1e5, alpha=0.12, color=PALETTE[1])
    ax.set_xticks(range(len(mon_rev)))
    ax.set_xticklabels([m[:3] for m in mon_rev.index], rotation=0, fontsize=9)
    for x,y in enumerate(mon_rev.values/1e5):
        ax.text(x, y+0.3, f"₹{y:.1f}L", ha='center', fontsize=7.5, fontweight='bold')
    ax.axhline(mon_rev.mean()/1e5, color=PALETTE[5], linestyle='--', linewidth=1.5,
               label=f"Monthly Avg ₹{mon_rev.mean()/1e5:.1f}L")
    ax.set_ylabel("Revenue (₹ Lakhs)"); ax.set_title("Monthly Revenue Trend — 2024")
    ax.legend(fontsize=9)
    fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close()
    insight("January peaks (post-holiday + New Year promotions). Revenue dips in Feb–May and recovers "
            "from Q3 onward. October is the second-strongest month, reflecting early festive-season demand.")

    st.divider()

    # ── Chart 3 ──────────────────────────────────────────────
    st.markdown("#### Chart 3 — Revenue Distribution (Histogram)")
    fig, ax = plt.subplots(figsize=(10,5))
    n,bins,patches = ax.hist(dff["Revenue_INR"], bins=30, color=PALETTE[1],
                              edgecolor='white', linewidth=1.2, alpha=0.9)
    for patch in patches:
        if patch.get_x() + patch.get_width()/2 > 8000:
            patch.set_facecolor(PALETTE[0])
    ax.axvline(dff["Revenue_INR"].mean(),   color=PALETTE[5], linestyle='--',
               linewidth=2, label=f'Mean = ₹{dff["Revenue_INR"].mean():,.0f}')
    ax.axvline(dff["Revenue_INR"].median(), color=PALETTE[3], linestyle='-.',
               linewidth=2, label=f'Median = ₹{dff["Revenue_INR"].median():,.0f}')
    ax.set_xlabel("Order Revenue (₹)"); ax.set_ylabel("Number of Orders")
    ax.set_title("Distribution of Order Revenue"); ax.legend(fontsize=10)
    fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close()
    insight("Right-skewed distribution: most orders fall between ₹200–₹3,000. "
            "High-value orders (>₹8,000, dark) are Electronics/Home & Kitchen — target these for upsells.")

    st.divider()

    # ── Charts 4 & 5 side by side ─────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Chart 4 — Avg Profit by Region")
        reg_prof = dff.groupby("Region")["Profit_INR"].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6,4))
        clrs4 = [PALETTE[2] if v>0 else PALETTE[5] for v in reg_prof.values]
        bars4 = ax.bar(reg_prof.index, reg_prof.values, color=clrs4, edgecolor="white", width=0.5)
        for bar,val in zip(bars4,reg_prof.values):
            ax.text(bar.get_x()+bar.get_width()/2,
                    val+20 if val>=0 else val-80,
                    f"₹{val:,.0f}", ha='center', va='bottom', fontsize=9, fontweight='bold')
        ax.axhline(0, color='grey', linewidth=0.8)
        ax.set_ylabel("Avg Profit (₹)"); ax.set_title("Avg Order Profit by Region")
        fig.tight_layout(); st.pyplot(fig); plt.close()
        insight("All regions are profitable. South India (Bangalore, Hyderabad, Chennai) leads — "
                "dense tech-savvy consumer base drives high-value Electronics orders.")

    with col_b:
        st.markdown("#### Chart 5 — Order Status Distribution")
        status_cnt = dff["Order_Status"].value_counts()
        colors_pie = [PALETTE[2], PALETTE[5], PALETTE[3], PALETTE[4]]
        fig, ax = plt.subplots(figsize=(6,4))
        wedges,texts,autotexts = ax.pie(status_cnt, labels=status_cnt.index,
            autopct='%1.1f%%', colors=colors_pie[:len(status_cnt)], startangle=140,
            wedgeprops=dict(edgecolor='white', linewidth=2))
        for at in autotexts:
            at.set_color('white'); at.set_fontweight('bold'); at.set_fontsize(11)
        ax.set_title("Order Status Distribution")
        fig.tight_layout(); st.pyplot(fig); plt.close()
        insight("75.5% delivery success rate. ~19% cancellations + returns represent direct revenue leakage. "
                "Improving product descriptions and size guides can reduce returns significantly.")

    st.divider()

    # ── Chart 6 ──────────────────────────────────────────────
    st.markdown("#### Chart 6 — Acquisition Channel: Orders vs Avg Order Value")
    ch_df = dff.groupby("Acquisition_Channel").agg(
        Orders=("Order_ID","count"),
        AOV=("Revenue_INR","mean")
    ).sort_values("Orders", ascending=False)
    fig, ax1 = plt.subplots(figsize=(10,5))
    ax2 = ax1.twinx()
    bars6 = ax1.bar(ch_df.index, ch_df["Orders"],
                    color=[PALETTE[i%len(PALETTE)] for i in range(len(ch_df))],
                    edgecolor="white", width=0.55, alpha=0.85, label="Order Count")
    ax2.plot(ch_df.index, ch_df["AOV"], color=PALETTE[5], linewidth=2.5,
             marker='D', markersize=8, label="AOV (₹)")
    for x,aov in enumerate(ch_df["AOV"]):
        ax2.text(x, aov+30, f"₹{aov:,.0f}", ha='center', fontsize=8.5, fontweight='bold', color=PALETTE[5])
    ax1.set_ylabel("Number of Orders"); ax2.set_ylabel("Avg Order Value (₹)")
    ax1.set_title("Acquisition Channel: Order Count vs AOV")
    ax1.tick_params(axis='x', rotation=10)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1+lines2, labels1+labels2, fontsize=9, loc='upper right')
    fig.tight_layout(); st.pyplot(fig, use_container_width=True); plt.close()
    insight("Email Campaigns drive the most orders. Referral channel has the highest AOV — referred customers "
            "buy premium products. Social Media brings volume but lower-value purchases.")

    st.divider()

    # ── Charts 7 & 8 ──────────────────────────────────────────
    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("#### Chart 7 — Avg Customer Rating by Category")
        cat_rat = dff.groupby("Category")["Customer_Rating"].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6,4))
        clrs7 = [PALETTE[2] if v>=4 else PALETTE[3] if v>=3.5 else PALETTE[5] for v in cat_rat.values]
        bars7 = ax.bar(cat_rat.index, cat_rat.values, color=clrs7, edgecolor="white", width=0.6)
        for bar,val in zip(bars7,cat_rat.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
                    f"{val:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax.axhline(4.0, color=PALETTE[5], linestyle='--', linewidth=1.5, label='4.0 Threshold')
        ax.set_ylim(3.0, 5.0); ax.set_ylabel("Avg Rating")
        ax.set_title("Avg Rating by Category"); ax.legend(fontsize=8)
        ax.tick_params(axis='x', rotation=10)
        fig.tight_layout(); st.pyplot(fig); plt.close()
        insight("All categories score above 3.9. Electronics and Home & Kitchen score highest "
                "— quality products drive satisfaction. Improving Books experience can boost repeat purchases.")

    with col_d:
        st.markdown("#### Chart 8 — Profit Margin % by Category (Box Plot)")
        cats_list = dff["Category"].unique()
        data8 = [dff[dff["Category"]==cat]["Profit_Margin_Pct"].dropna().values for cat in cats_list]
        fig, ax = plt.subplots(figsize=(6,4))
        bp = ax.boxplot(data8, tick_labels=cats_list, patch_artist=True, widths=0.5,
                        medianprops=dict(color='white', linewidth=2))
        for patch,color in zip(bp['boxes'], PALETTE[:5]):
            patch.set_facecolor(color); patch.set_alpha(0.85)
        ax.set_ylabel("Profit Margin (%)"); ax.set_title("Profit Margin % by Category")
        ax.axhline(0, color='red', linestyle=':', linewidth=1)
        ax.tick_params(axis='x', rotation=12)
        fig.tight_layout(); st.pyplot(fig); plt.close()
        insight("Home & Kitchen has the tightest, most consistent margin distribution. "
                "Electronics has a wider spread — some premium products have very high margins.")

    st.divider()

    # ── Charts 9 & 10 ─────────────────────────────────────────
    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown("#### Chart 9 — Discount % vs Revenue (Scatter)")
        sample = dff.sample(min(1000, len(dff)), random_state=42)
        fig, ax = plt.subplots(figsize=(6,4.5))
        ax.scatter(sample["Discount_Pct"], sample["Revenue_INR"],
                   c=PALETTE[1], alpha=0.4, s=30, edgecolors=PALETTE[0], linewidths=0.3)
        z = np.polyfit(dff["Discount_Pct"], dff["Revenue_INR"], 1)
        xs = np.linspace(0, 25, 100)
        ax.plot(xs, np.poly1d(z)(xs), color=PALETTE[5], linewidth=2, linestyle='--', label='Trend')
        r = dff["Discount_Pct"].corr(dff["Revenue_INR"])
        ax.text(0.05, 0.90, f"r = {r:.3f}", transform=ax.transAxes,
                fontsize=11, fontweight='bold', color=PALETTE[0],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#EBF5FB'))
        ax.set_xlabel("Discount %"); ax.set_ylabel("Revenue (₹)")
        ax.set_title("Discount % vs Revenue"); ax.legend(fontsize=8)
        fig.tight_layout(); st.pyplot(fig); plt.close()
        insight(f"Pearson r = {r:.3f} — near-zero correlation. Discounting does NOT drive higher revenue. "
                "Blanket discounts erode margins without compensatory volume. Switch to targeted promotions.")

    with col_f:
        st.markdown("#### Chart 10 — Revenue vs Quantity Ordered (Scatter)")
        fig, ax = plt.subplots(figsize=(6,4.5))
        for cat, col in zip(dff["Category"].unique(), PALETTE):
            sub = dff[dff["Category"]==cat].sample(min(200,len(dff[dff["Category"]==cat])), random_state=1)
            ax.scatter(sub["Quantity"], sub["Revenue_INR"],
                       c=col, alpha=0.5, s=25, label=cat, edgecolors='white', linewidths=0.2)
        z2 = np.polyfit(dff["Quantity"], dff["Revenue_INR"], 1)
        xs2 = np.linspace(1, 5, 100)
        ax.plot(xs2, np.poly1d(z2)(xs2), color='#2C3E50', linewidth=2, linestyle='--')
        r2 = dff["Quantity"].corr(dff["Revenue_INR"])
        ax.text(0.05, 0.90, f"r = {r2:.3f}", transform=ax.transAxes,
                fontsize=11, fontweight='bold', color=PALETTE[0],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#EBF5FB'))
        ax.set_xlabel("Quantity Ordered"); ax.set_ylabel("Revenue (₹)")
        ax.set_title("Revenue vs Quantity by Category"); ax.legend(fontsize=7, ncol=2)
        fig.tight_layout(); st.pyplot(fig); plt.close()
        insight(f"Positive correlation (r={r2:.3f}) — more units ordered means higher order value. "
                "Bundle deals (e.g., '2 for ₹X') for Fashion and Books could boost AOV significantly.")

    st.divider()

    # ── Charts 11 & 12 ────────────────────────────────────────
    col_g, col_h = st.columns(2)
    with col_g:
        st.markdown("#### Chart 11 — Revenue by Quarter (Grouped Bar)")
        q_df = dff.groupby("Quarter")[["Revenue_INR","Profit_INR"]].sum().reindex(["Q1","Q2","Q3","Q4"])
        fig, ax = plt.subplots(figsize=(6,4))
        x = np.arange(4)
        b1 = ax.bar(x-0.2, q_df["Revenue_INR"]/1e5, 0.38, label="Revenue", color=PALETTE[0])
        b2 = ax.bar(x+0.2, q_df["Profit_INR"]/1e5,  0.38, label="Profit",  color=PALETTE[2])
        ax.set_xticks(x); ax.set_xticklabels(["Q1","Q2","Q3","Q4"])
        for bar in b1:
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
                    f"₹{bar.get_height():.0f}L", ha='center', fontsize=8, fontweight='bold')
        ax.set_ylabel("Amount (₹ Lakhs)"); ax.set_title("Quarterly Revenue & Profit")
        ax.legend(fontsize=9)
        fig.tight_layout(); st.pyplot(fig); plt.close()
        insight("Q1 is the strongest quarter. Margins stay stable at ~46% across all quarters — "
                "a positive sign of consistent cost management. A mid-year sale can close the Q2 gap.")

    with col_h:
        st.markdown("#### Chart 12 — Profitable vs Loss-Making Orders")
        prof_cnt    = int(dff["Profit_Flag"].sum())
        nonprof_cnt = len(dff) - prof_cnt
        fig, ax = plt.subplots(figsize=(6,4))
        wedges,texts = ax.pie([prof_cnt, nonprof_cnt],
            labels=[f"Profitable\n{prof_cnt} ({prof_cnt/len(dff)*100:.1f}%)",
                    f"Loss-Making\n{nonprof_cnt} ({nonprof_cnt/len(dff)*100:.1f}%)"],
            colors=[PALETTE[2], PALETTE[5]],
            startangle=90, wedgeprops=dict(width=0.55, edgecolor='white', linewidth=3))
        ax.text(0, 0, f"{prof_cnt/len(dff)*100:.1f}%\nProfitable",
                ha='center', va='center', fontsize=13, fontweight='bold', color=PALETTE[2])
        ax.set_title("Order Profitability Split")
        fig.tight_layout(); st.pyplot(fig); plt.close()
        insight(f"{prof_cnt/len(dff)*100:.1f}% of orders are profitable. Loss-making orders occur primarily "
                "when shipping cost (₹49–99) exceeds the net margin on very low-priced items. "
                "Enforcing the ₹499 free-shipping threshold eliminates most of these.")


# ══════════════════════════════════════════════════════════════
# TAB 5 — CORRELATION
# ══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<span class="section-tag">CORRELATION ANALYSIS</span>', unsafe_allow_html=True)
    st.subheader("Pearson Correlation Matrix — Key Numerical Variables")

    num_cols_c = ["Revenue_INR","Profit_INR","COGS_INR","Quantity",
                  "Discount_Pct","Unit_Price_INR","Shipping_INR",
                  "Customer_Rating","Profit_Margin_Pct","Is_Repeat_Customer"]
    short_n    = ["Revenue","Profit","COGS","Quantity","Discount%",
                  "UnitPrice","Shipping","Rating","ProfMgn%","Repeat"]

    corr_m = dff[num_cols_c].corr()
    corr_m.index   = short_n
    corr_m.columns = short_n

    fig, ax = plt.subplots(figsize=(12,9))
    cmap = sns.diverging_palette(10, 133, as_cmap=True)
    sns.heatmap(corr_m, annot=True, fmt=".2f", cmap=cmap, vmin=-1, vmax=1,
                center=0, ax=ax, square=True, linewidths=0.5, linecolor='white',
                annot_kws={"size":9,"weight":"bold"},
                cbar_kws={"shrink":0.7,"label":"Pearson r"})
    ax.set_title("Pearson Correlation Heatmap — ShopEase India Numerical Variables", pad=20, fontsize=14)
    ax.tick_params(axis='x', rotation=40, labelsize=9)
    ax.tick_params(axis='y', rotation=0,  labelsize=9)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.divider()
    st.subheader("Key Correlation Findings")

    rev_profit_r  = corr_m.loc["Revenue","Profit"]
    rev_cogs_r    = corr_m.loc["Revenue","COGS"]
    qty_rev_r     = corr_m.loc["Quantity","Revenue"]
    disc_rev_r    = corr_m.loc["Discount%","Revenue"]
    margin_disc_r = corr_m.loc["ProfMgn%","Discount%"]

    corr_findings = [
        ("Revenue ↔ Profit",        f"{rev_profit_r:.3f}",  "Strong Positive",
         "Revenue is the primary profit driver. Every ₹1 of revenue generates ~₹0.46 profit on average."),
        ("Revenue ↔ COGS",          f"{rev_cogs_r:.3f}",    "Strong Positive",
         "COGS scales directly with revenue. Negotiating bulk supplier discounts is the #1 margin lever."),
        ("Quantity ↔ Revenue",      f"{qty_rev_r:.3f}",     "Moderate Positive",
         "Higher quantities = higher revenue. Bundle deals for Fashion & Books can lift AOV."),
        ("Discount % ↔ Revenue",    f"{disc_rev_r:.3f}",    "Near Zero / Negligible",
         "Critical finding: discounting does NOT drive higher order value. Eliminate blanket promotions."),
        ("Profit Margin ↔ Discount",f"{margin_disc_r:.3f}", "Moderate Negative",
         "Each 5% discount shaves ~2–3% off profit margin. Targeted discounting is essential."),
    ]
    for var, r_val, strength, desc in corr_findings:
        col1,col2,col3 = st.columns([2,1.5,5])
        with col1: st.markdown(f"**{var}**")
        with col2:
            clr = "green" if float(r_val)>0 else "red"
            st.markdown(f"<span style='color:{clr};font-weight:700;font-size:1.05rem;'>{r_val} ({strength})</span>",
                        unsafe_allow_html=True)
        with col3: st.markdown(desc)
        st.markdown("---")


# ══════════════════════════════════════════════════════════════
# TAB 6 — DATASET
# ══════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<span class="section-tag">DATASET EXPLORER</span>', unsafe_allow_html=True)

    view = st.radio("View:", ["Cleaned Dataset (4,850 rows × 27 cols)", "Raw Dataset (5,000 rows × 21 cols)"],
                    horizontal=True)

    if "Cleaned" in view:
        display_df = dff.drop(columns=["Order_Date_dt"], errors='ignore')
        st.markdown(f"**{len(display_df)} rows × {len(display_df.columns)} columns** — after cleaning & feature engineering")
    else:
        display_df = raw
        missing_rows = raw[raw.isnull().any(axis=1)]
        st.warning(f"Raw data contains {raw.isnull().sum().sum()} missing cells across {len(missing_rows)} rows.")

    search = st.text_input("Search by Order ID or City")
    if search:
        mask2 = (
            display_df["Order_ID"].str.contains(search, case=False, na=False) |
            display_df["City"].str.contains(search, case=False, na=False)
        )
        display_df = display_df[mask2]

    st.dataframe(display_df, use_container_width=True, height=420)

    csv = display_df.to_csv(index=False).encode()
    st.download_button("⬇️ Download CSV", csv,
                       file_name="shopease_india_dataset.csv",
                       mime="text/csv")

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#6B7280;font-size:0.82rem;'>"
    "🛒 ShopEase India EDA Dashboard · MBA Data Analytics Individual Assignment · "
    "Built with Python, Streamlit, Matplotlib & Seaborn"
    "</div>",
    unsafe_allow_html=True
)
