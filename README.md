# 📊 Enterprise Sales Analytics & Intelligence Dashboard
> **Final Year BCA Capstone / Resume Project**  
> *Built with Python, Streamlit, Pandas, Plotly, Scikit-Learn, and OpenPyXL*

---

## 🎯 Project Overview

The **Enterprise Sales Analytics & Intelligence Dashboard** is an enterprise-grade Business Intelligence (BI) and predictive analytics application. Developed specifically to serve as a standout project for a Bachelor of Computer Applications (BCA) final-year capstone and job resume, it bridges the gap between raw database transactional records and strategic decision-making.

The system processes **2,500+ multi-year enterprise transactions**, evaluates core financial KPIs with delta growth metrics, performs behavioral customer segmentation (RFM Analysis), provides machine-learning-based sales forecasting, and allows seamless data export to CSV and Excel.

---

## 🚀 Key Features

### 1. 📊 Executive KPI Command Center
- **Total Net Sales**: Calculated after promotional discounts and return adjustments.
- **Net Profit & Profit Margin %**: Real-time margin health evaluation.
- **Order Volume & Average Order Value (AOV)**: Velocity and customer basket size tracking.
- **Period-over-Period Delta Indicators**: Automated comparisons against prior matching time intervals with positive/negative growth markers.

### 2. 🎛️ Multidimensional Filtering & Dynamic Drilldowns
- **Preset Time Horizons**: All-time, Last 12 Months, Last 6 Months, Yearly presets, or granular custom Date Pickers.
- **Multi-select Dimensions**: Filter by Region (North, South, East, West, Central), Product Category (Technology, Furniture, Office Supplies), Customer Segment, and Order Status.
- **Instant Reactive UI**: Streamlit's state cache automatically re-aggregates metrics and charts on filter changes.

### 3. 📈 Predictive Revenue Forecasting (Machine Learning)
- **Linear Trend Regression**: Leverages Scikit-Learn to model monthly revenue patterns and extrapolate future 6-month trajectories.
- **Statistical Confidence Intervals**: Generates 80% upper and lower prediction bounds based on historical residual variance.
- **Seasonality Profiling**: Aggregates average sales by Day of Week and Month of Year to identify high-volume demand periods.

### 4. 👥 Customer Intelligence & RFM Segmentation
- **Recency, Frequency, Monetary (RFM) Matrix**: Quantile-based algorithmic scoring (1–4 per dimension) classifying customers into 5 strategic tiers:
  - 🏆 *Champions / High Value*
  - 💎 *Loyal Customers*
  - 🌟 *Potential Loyalists*
  - ⚠️ *Needs Attention*
  - 🚨 *At Risk / Inactive*
- **Interactive Scatter Plot**: Visualize customer spend vs. order frequency and days since last purchase.

### 5. 🔍 Transaction Explorer & Dual Export Engine
- **In-memory Search**: Instant substring search across Order IDs, Customer Names, and Cities.
- **1-Click CSV Export**: Download filtered data directly as UTF-8 `.csv`.
- **1-Click Excel Export**: Generates styled `.xlsx` spreadsheets via `openpyxl`.

### 6. 🎓 Built-In Viva Defense & Resume Module
- Dedicated dashboard tab with 10 detailed viva/technical interview questions and answers, explaining algorithmic choices, architecture, and business impact.

---

## 🏗️ System Architecture & Directory Structure

```
Sales dashboard project/
│
├── app.py                      # Main Streamlit Dashboard Application & Controller
├── config.py                   # CSS design system, typography, color palettes & badges
├── data_generator.py           # Enterprise dataset generator (2,500+ realistic orders)
├── data/
│   └── enterprise_sales.csv    # Rich multi-year transaction dataset
├── utils/
│   ├── __init__.py             # Package initializer
│   ├── analytics.py            # Data loading, KPI calculations, RFM logic, ML forecast
│   └── visualizations.py       # Custom interactive Plotly chart generators
├── requirements.txt            # Python dependencies
├── run_dashboard.bat           # 1-Click launcher script for Windows
└── README.md                   # Complete documentation, Viva Guide & Resume points
```

---

## 💻 Tech Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Standard language for data analytics and ML |
| **UI Framework** | Streamlit | Rapid, reactive data application framework |
| **Data Engine** | Pandas & NumPy | High-performance vectorized data manipulation |
| **Visualization** | Plotly Express & Graph Objects | Fully interactive, zoomable, hardware-accelerated charts |
| **Machine Learning**| Scikit-Learn | Linear trend regression and residual variance modeling |
| **Spreadsheets** | OpenPyXL | Formatted Excel workbook generation |

---

## 🛠️ Installation & Setup Guide

### Step 1: Verify Python Installation
Open PowerShell or Command Prompt and run:
```bash
py --version
```
*(Any Python version 3.10 through 3.14 is supported).*

### Step 2: Install Dependencies
Navigate to the project directory and install the required libraries:
```bash
py -m pip install -r requirements.txt
```

### Step 3: Launch the Dashboard

**Option A (1-Click Batch File on Windows):**
Simply double-click `run_dashboard.bat` in the project folder.

**Option B (Command Line):**
```bash
py -m streamlit run app.py
```

Your default web browser will automatically open:
```
Local URL: http://localhost:8501
```

---

## 📝 How to Showcase This on Your BCA Resume

Add this section directly into your Resume under **Projects**:

```markdown
### Enterprise Sales Intelligence & Predictive Analytics Dashboard
**Technologies:** Python, Streamlit, Pandas, Plotly, Scikit-Learn, OpenPyXL
- Engineered an interactive Business Intelligence application analyzing 2,500+ enterprise transactions with sub-second filter execution via `@st.cache_data`.
- Formulated real-time KPI engines (Net Sales, Profit Margins, AOV) with period-over-period delta comparisons.
- Implemented an RFM (Recency, Frequency, Monetary) segmentation model categorizing accounts into 5 behavioral retention tiers.
- Integrated a Linear Regression predictive pipeline to forecast forward 6-month revenues with an 80% confidence interval envelope.
- Built a dual-format export engine allowing users to download filtered subsets into CSV and formatted Microsoft Excel (.xlsx) workbooks.
```

---

## 📜 License
This project is open-source and free to use for academic submissions and personal portfolios.
