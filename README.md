---
title: ShopEase India E-Commerce EDA Dashboard
emoji: 🛒
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
license: mit
---

# 🛒 ShopEase India — E-Commerce EDA Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

> **MBA Data Analytics · Individual Assignment**  
> Task 1: Synthetic Data (10M) | Task 2: Data Cleaning (10M) | Task 3: EDA & Charts (30M)

---

## 🚀 Live Demo

| Platform | Link |
|----------|------|
| **Streamlit Cloud** | [Deploy instructions below](#deploy-on-streamlit-cloud) |
| **HuggingFace Spaces** | [Deploy instructions below](#deploy-on-huggingface-spaces) |

---

## 📋 Project Overview

**ShopEase India** is a synthetic D2C e-commerce start-up dataset built to validate a real business idea:  
_Can a Direct-to-Consumer platform across Indian metros generate profitable unit economics within Year 1 of operations?_

### Dataset
- **5,000 orders** generated → **4,850 after cleaning** (duplicates removed)
- **27 variables**: 21 raw + 7 derived features
- **8 Indian cities**: Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad
- **5 product categories**: Electronics, Fashion, Home & Kitchen, Sports & Fitness, Books
- **5 acquisition channels**: Organic Search, Paid Ads, Social Media, Email Campaign, Referral

> **Note:** The dataset is fully generated inside `app.py` using Python's `random` module with a fixed seed (`random.seed(42)`), so **no CSV file is needed**. The app is fully self-contained.

---

## 📊 Dashboard Features

| Tab | Content |
|-----|---------|
| **Overview & KPIs** | 9 live KPI cards, city & category distribution charts |
| **Data Cleaning** | Missing values viz, outlier detection, cleaning log, feature engineering |
| **Descriptive Stats** | Full summary statistics table + frequency distributions |
| **EDA Charts** | 12 analytical charts with business insights |
| **Correlation** | Pearson correlation heatmap (10×10) + key findings |
| **Dataset** | Searchable explorer with CSV download (raw & cleaned) |

### Charts Included
1. Avg Revenue & Profit by Category (Grouped Horizontal Bar)
2. Monthly Revenue Trend (Line Chart with avg reference line)
3. Revenue Distribution (Histogram)
4. Avg Profit by Region (Bar Chart)
5. Order Status Distribution (Pie Chart)
6. Acquisition Channel: Orders vs AOV (Dual-axis Bar + Line)
7. Avg Customer Rating by Category (Bar Chart)
8. Profit Margin % by Category (Box Plot)
9. Discount % vs Revenue (Scatter + Trendline + Pearson r)
10. Revenue vs Quantity by Category (Multi-colour Scatter)
11. Quarterly Revenue & Profit (Grouped Bar Chart)
12. Profitable vs Loss-Making Orders (Donut Chart)
+ Pearson Correlation Heatmap (10×10)

---

## 🛠️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/shopease-eda.git
cd shopease-eda

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 🌐 Deploy on Streamlit Cloud

> Free deployment in 3 steps — no credit card needed

**Step 1:** Push this repo to GitHub (public repo)
```bash
git init
git add .
git commit -m "Initial commit: ShopEase India EDA Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/shopease-eda.git
git push -u origin main
```

**Step 2:** Go to [share.streamlit.io](https://share.streamlit.io)
- Click **"New app"**
- Select your GitHub repo: `YOUR_USERNAME/shopease-eda`
- Branch: `main`
- Main file path: `app.py`
- Click **"Deploy"**

**Step 3:** Your app is live at:  
`https://YOUR_USERNAME-shopease-eda-app-XXXXX.streamlit.app`

---

## 🤗 Deploy on HuggingFace Spaces

> The `README.md` front-matter is already configured for HuggingFace Spaces

**Step 1:** Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
- Name: `shopease-eda`
- SDK: **Streamlit**
- Visibility: Public

**Step 2:** Upload files via the web UI or Git:
```bash
# Using HuggingFace CLI
pip install huggingface_hub

huggingface-cli login
# Paste your HF token from huggingface.co/settings/tokens

# Clone your space
git clone https://huggingface.co/spaces/YOUR_HF_USERNAME/shopease-eda
cd shopease-eda

# Copy app files
cp /path/to/app.py .
cp /path/to/requirements.txt .
cp /path/to/README.md .

# Push
git add .
git commit -m "Deploy ShopEase India EDA Dashboard"
git push
```

**Step 3:** Your app is live at:  
`https://YOUR_HF_USERNAME-shopease-eda.hf.space`

---

## 📁 File Structure

```
shopease-eda/
├── app.py              ← Main Streamlit app (self-contained, no CSV needed)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file (also HuggingFace Spaces config)
```

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| Streamlit | Web app framework |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Chart rendering |
| Seaborn | Heatmap & statistical plots |

---

## 📚 Assignment Tasks Covered

| Task | Marks | Description |
|------|-------|-------------|
| **Task 1** | 10M | Synthetic data generation for D2C e-commerce business validation |
| **Task 2** | 10M | Data cleaning (missing values, outliers, duplicates) + transformation (7 derived features) |
| **Task 3** | 30M | Descriptive analytics + 12 EDA charts + correlation matrix with business insights |
| **Total** | **50M** | Individual submission |

---

## 📄 License

MIT License — free to use, modify, and distribute.
