# 🛒 ShopEase E-Commerce Analytics Dashboard

A Streamlit dashboard for the **Data Analytics (MGB) Individual Assignment**.  
Performs end-to-end descriptive analytics on ShopEase's synthetic e-commerce dataset (5,000 orders, Jan–Dec 2024).

---

## 📁 Project Structure

```
shopease_streamlit/
├── app.py                        # Main Streamlit application
├── shopease_ecommerce_data.csv   # Synthetic dataset (5,000 rows, 21 features)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 How to Deploy on Streamlit Cloud

1. **Push this folder to GitHub**
   - Create a new GitHub repository (e.g., `shopease-analytics`)
   - Upload all files in this folder to the root of the repo

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click **"New app"**
   - Select your GitHub repo and branch (`main`)
   - Set **Main file path** to `app.py`
   - Click **Deploy** ✅

---

## 💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Dashboard Features

| Section | Chart Type | Insight Covered |
|---|---|---|
| KPI Cards | Metric tiles | Revenue, Profit, Margin, AOV, Rating, Repeat % |
| Category Performance | Horizontal Bar | Revenue & profit by category |
| Monthly Trend | Line Chart | Revenue across Jan–Dec 2024 |
| Order Status | Pie Chart | Delivery, Cancellation, Return rates |
| Acquisition Channels | Bar + AOV | Channel revenue and avg order value |
| Discount vs Revenue | Scatter + Trendline | Pearson correlation analysis |
| Customer Ratings | Bar Chart | 1–5 star distribution |
| Quarterly Performance | Grouped Bar | Q1–Q4 revenue, profit, margin |
| City Revenue | Horizontal Bar | Top 8 metro-wise revenue |
| Payment Methods | Bar Chart | UPI, Cards, COD distribution |
| Device Types | Pie Chart | Mobile vs Desktop vs Tablet |
| Descriptive Stats | Table | Mean, Median, Std Dev, Min, Max |

---

## 🎓 Assignment Details

- **Course**: Data Analytics – MGB  
- **Task**: Individual Submission (50 Marks)  
- **Business Domain**: E-Commerce / Retail (ShopEase D2C Startup)  
- **Techniques**: Synthetic Data Generation · Data Cleaning · Descriptive Analytics · EDA  
