import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="ShopEase Analytics", page_icon="🛒", layout="wide")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fc; }
    .block-container { padding-top: 1.5rem; }
    h1 { color: #1F4E79; }
    h2, h3 { color: #2E75B6; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        text-align: center;
    }
    .metric-label { font-size: 13px; color: #888; margin-bottom: 4px; }
    .metric-value { font-size: 26px; font-weight: 700; color: #1F4E79; }
    .insight-box {
        background: #EBF5FB;
        border-left: 4px solid #2E75B6;
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 8px;
        font-size: 14px;
        color: #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("shopease_ecommerce_data.csv")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)
    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/shopping-cart.png", width=60)
st.sidebar.title("ShopEase Analytics")
st.sidebar.markdown("---")

categories = st.sidebar.multiselect("Category", df["Category"].unique(), default=list(df["Category"].unique()))
quarters   = st.sidebar.multiselect("Quarter", ["Q1","Q2","Q3","Q4"], default=["Q1","Q2","Q3","Q4"])
statuses   = st.sidebar.multiselect("Order Status", df["Order_Status"].unique(), default=list(df["Order_Status"].unique()))

fdf = df[df["Category"].isin(categories) & df["Quarter"].isin(quarters) & df["Order_Status"].isin(statuses)]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(fdf):,}** of **{len(df):,}** orders")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛒 ShopEase E-Commerce Analytics Dashboard")
st.markdown("**Individual Assignment — Data Analytics (MGB) | Year: 2024**")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_rev   = fdf["Revenue_INR"].sum()
total_prof  = fdf["Profit_INR"].sum()
margin      = (total_prof / total_rev * 100) if total_rev else 0
aov         = fdf["Revenue_INR"].mean()
delivered   = fdf[fdf["Order_Status"] == "Delivered"]
avg_rating  = delivered["Customer_Rating"].mean()
repeat_pct  = fdf["Is_Repeat_Customer"].mean() * 100

c1, c2, c3, c4, c5, c6 = st.columns(6)
def kpi(col, label, value):
    col.markdown(f"""<div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>""", unsafe_allow_html=True)

kpi(c1, "Total Revenue",   f"₹{total_rev/1e6:.2f}M")
kpi(c2, "Total Profit",    f"₹{total_prof/1e6:.2f}M")
kpi(c3, "Profit Margin",   f"{margin:.1f}%")
kpi(c4, "Avg Order Value", f"₹{aov:,.0f}")
kpi(c5, "Avg Rating",      f"⭐ {avg_rating:.2f}" if not np.isnan(avg_rating) else "N/A")
kpi(c6, "Repeat Customers",f"{repeat_pct:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ── Helper ────────────────────────────────────────────────────────────────────
BLUE_PALETTE = ["#1F4E79","#2E75B6","#4A90C4","#6BAED6","#9ECAE1","#C6DBEF"]

def insight(text):
    st.markdown(f'<div class="insight-box">💡 <b>Insight:</b> {text}</div>', unsafe_allow_html=True)

# ── Row 1: Category Revenue + Monthly Trend ───────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Revenue & Profit by Category")
    cat_df = fdf.groupby("Category")[["Revenue_INR","Profit_INR"]].sum().sort_values("Revenue_INR", ascending=True)
    fig, ax = plt.subplots(figsize=(6, 3.8))
    y = np.arange(len(cat_df))
    ax.barh(y - 0.2, cat_df["Revenue_INR"]/1e5, 0.38, label="Revenue", color="#2E75B6")
    ax.barh(y + 0.2, cat_df["Profit_INR"]/1e5,  0.38, label="Profit",  color="#4A90C4")
    ax.set_yticks(y); ax.set_yticklabels(cat_df.index, fontsize=9)
    ax.set_xlabel("Amount (₹ Lakhs)", fontsize=9)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
    ax.legend(fontsize=8); ax.grid(axis="x", alpha=0.3); ax.set_facecolor("#f8f9fc")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("Home & Kitchen and Electronics together drive ~68% of total revenue with ~46% margins each.")

with col2:
    st.subheader("📈 Monthly Revenue Trend")
    mon_df = fdf.groupby("Month", observed=True)["Revenue_INR"].sum()
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(mon_df.index, mon_df.values/1e5, marker="o", color="#1F4E79", linewidth=2.5, markersize=6)
    ax.fill_between(range(len(mon_df)), mon_df.values/1e5, alpha=0.12, color="#2E75B6")
    ax.set_xticks(range(len(mon_df)))
    ax.set_xticklabels([m[:3] for m in mon_df.index], rotation=45, fontsize=8)
    ax.set_ylabel("Revenue (₹ Lakhs)", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
    ax.grid(alpha=0.3); ax.set_facecolor("#f8f9fc")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("January peaks at ₹13.7L; revenue stabilises from Q2–Q4, showing consistent demand with no extreme seasonality.")

st.markdown("---")

# ── Row 2: Order Status Pie + Acquisition Channel ────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("🔄 Order Status Distribution")
    status_cnt = fdf["Order_Status"].value_counts()
    colors_pie = ["#2E75B6","#E74C3C","#F39C12","#95A5A6"]
    fig, ax = plt.subplots(figsize=(5, 3.8))
    wedges, texts, autotexts = ax.pie(
        status_cnt.values, labels=status_cnt.index, autopct="%1.1f%%",
        colors=colors_pie[:len(status_cnt)], startangle=140,
        textprops={"fontsize": 9}, pctdistance=0.78
    )
    for at in autotexts: at.set_color("white"); at.set_fontweight("bold")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("75.5% delivery rate is solid; ~19% combined cancellations + returns represent key revenue leakage to address.")

with col4:
    st.subheader("📣 Acquisition Channel Performance")
    ch_df = fdf.groupby("Acquisition_Channel").agg(
        Revenue=("Revenue_INR","sum"),
        AOV=("Revenue_INR","mean")
    ).sort_values("Revenue", ascending=True)
    fig, ax = plt.subplots(figsize=(6, 3.8))
    bars = ax.barh(ch_df.index, ch_df["Revenue"]/1e5, color=BLUE_PALETTE[:len(ch_df)], edgecolor="white")
    for bar, aov_val in zip(bars, ch_df["AOV"]):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"AOV ₹{aov_val:,.0f}", va="center", fontsize=8, color="#444")
    ax.set_xlabel("Revenue (₹ Lakhs)", fontsize=9)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
    ax.grid(axis="x", alpha=0.3); ax.set_facecolor("#f8f9fc")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("Email Campaigns drive the most revenue; Referral has the highest AOV (₹2,606) — best for high-value customer targeting.")

st.markdown("---")

# ── Row 3: Discount vs Revenue Scatter + Rating Distribution ─────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("💸 Discount % vs Revenue (Correlation)")
    sample = fdf.sample(min(1000, len(fdf)), random_state=42)
    corr = fdf["Discount_Pct"].corr(fdf["Revenue_INR"])
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.scatter(sample["Discount_Pct"], sample["Revenue_INR"]/1000,
               alpha=0.3, s=15, color="#2E75B6")
    m, b = np.polyfit(fdf["Discount_Pct"], fdf["Revenue_INR"]/1000, 1)
    x_line = np.linspace(0, 25, 100)
    ax.plot(x_line, m*x_line + b, color="#E74C3C", linewidth=2, label=f"Trend (r={corr:.3f})")
    ax.set_xlabel("Discount %", fontsize=9); ax.set_ylabel("Revenue (₹ '000s)", fontsize=9)
    ax.legend(fontsize=8); ax.grid(alpha=0.3); ax.set_facecolor("#f8f9fc")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight(f"Pearson r = {corr:.4f} — near-zero correlation. Discounting does NOT drive higher revenue. Avoid blanket discounts.")

with col6:
    st.subheader("⭐ Customer Rating Distribution")
    rated = fdf[(fdf["Order_Status"] == "Delivered") & (fdf["Customer_Rating"].notna())]
    rating_cnt = rated["Customer_Rating"].value_counts().sort_index()
    colors_r = ["#E74C3C","#E67E22","#F1C40F","#2ECC71","#27AE60"]
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    bars = ax.bar(rating_cnt.index.astype(int), rating_cnt.values,
                  color=colors_r, edgecolor="white", width=0.6)
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
                str(int(bar.get_height())), ha="center", fontsize=9, fontweight="bold")
    ax.set_xlabel("Star Rating", fontsize=9); ax.set_ylabel("Number of Orders", fontsize=9)
    ax.set_xticks([1,2,3,4,5])
    ax.set_xticklabels(["1★","2★","3★","4★","5★"])
    ax.grid(axis="y", alpha=0.3); ax.set_facecolor("#f8f9fc")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("80.2% of customers rate 4–5 stars (avg 4.10/5). Strong satisfaction signals early product-market fit.")

st.markdown("---")

# ── Row 4: Quarterly Performance + City Revenue ───────────────────────────────
col7, col8 = st.columns(2)

with col7:
    st.subheader("📊 Quarterly Revenue vs Profit")
    q_df = fdf.groupby("Quarter")[["Revenue_INR","Profit_INR"]].sum().reindex(["Q1","Q2","Q3","Q4"])
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.bar(x - 0.2, q_df["Revenue_INR"]/1e5, 0.38, label="Revenue", color="#1F4E79")
    ax.bar(x + 0.2, q_df["Profit_INR"]/1e5,  0.38, label="Profit",  color="#4A90C4")
    ax.set_xticks(x); ax.set_xticklabels(["Q1","Q2","Q3","Q4"])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:.0f}L"))
    ax.set_ylabel("Amount (₹ Lakhs)", fontsize=9)
    ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3); ax.set_facecolor("#f8f9fc")
    for i, (rev, prof) in enumerate(zip(q_df["Revenue_INR"]/1e5, q_df["Profit_INR"]/1e5)):
        margin_q = prof/rev*100 if rev else 0
        ax.text(i, rev + 0.5, f"{margin_q:.1f}%", ha="center", fontsize=8, color="#1F4E79", fontweight="bold")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("Margins stay stable at 45.6–46.1% across all quarters. Q2 dips -12.5% QoQ — plan a mid-year promotion.")

with col8:
    st.subheader("🏙️ City-wise Revenue Distribution")
    city_df = fdf.groupby("City")["Revenue_INR"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    colors_c = plt.cm.Blues(np.linspace(0.4, 0.85, len(city_df)))
    bars = ax.barh(city_df.index, city_df.values/1e5, color=colors_c, edgecolor="white")
    for bar in bars:
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f"₹{bar.get_width():.1f}L", va="center", fontsize=8)
    ax.set_xlabel("Revenue (₹ Lakhs)", fontsize=9)
    ax.grid(axis="x", alpha=0.3); ax.set_facecolor("#f8f9fc")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("Revenue is evenly spread across metros (11.5–13.7%). Expanding to Tier-2 cities is the next growth lever.")

st.markdown("---")

# ── Row 5: Payment Method + Device Type ──────────────────────────────────────
col9, col10 = st.columns(2)

with col9:
    st.subheader("💳 Payment Method Distribution")
    pay_df = fdf["Payment_Method"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3.4))
    ax.barh(pay_df.index, pay_df.values, color=BLUE_PALETTE[:len(pay_df)], edgecolor="white")
    for i, v in enumerate(pay_df.values):
        ax.text(v + 5, i, f"{v:,} ({v/len(fdf)*100:.1f}%)", va="center", fontsize=8)
    ax.set_xlabel("Orders", fontsize=9)
    ax.grid(axis="x", alpha=0.3); ax.set_facecolor("#f8f9fc")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("Payment methods are evenly distributed (~20% each). UPI is growing — ensure seamless UPI integration.")

with col10:
    st.subheader("📱 Device Type Usage")
    dev_df = fdf["Device_Type"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3.4))
    colors_d = ["#1F4E79","#2E75B6","#6BAED6"]
    wedges, texts, autotexts = ax.pie(
        dev_df.values, labels=dev_df.index, autopct="%1.1f%%",
        colors=colors_d, startangle=140, textprops={"fontsize":10}, pctdistance=0.78
    )
    for at in autotexts: at.set_color("white"); at.set_fontweight("bold")
    fig.patch.set_facecolor("#f8f9fc"); fig.tight_layout()
    st.pyplot(fig)
    insight("Desktop (34.8%) leads slightly, but Mobile (33.7%) is nearly equal — ensure a mobile-first responsive design.")

st.markdown("---")

# ── Descriptive Stats Table ───────────────────────────────────────────────────
st.subheader("📋 Descriptive Statistics Summary")
numeric_cols = ["Revenue_INR","Profit_INR","COGS_INR","Quantity","Discount_Pct","Unit_Price_INR"]
desc = fdf[numeric_cols].describe().T.round(2)
desc.index = ["Revenue (₹)","Profit (₹)","COGS (₹)","Quantity","Discount %","Unit Price (₹)"]
st.dataframe(desc.style.format("{:.2f}").background_gradient(cmap="Blues", subset=["mean","50%"]), use_container_width=True)

st.markdown("---")

# ── Raw Data Preview ──────────────────────────────────────────────────────────
with st.expander("🗂️ View Raw Dataset (first 100 rows)"):
    st.dataframe(fdf.head(100), use_container_width=True)

st.caption("ShopEase E-Commerce Analytics | Data Analytics (MGB) Individual Assignment | 2024")
