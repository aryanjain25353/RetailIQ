# RetailIQ – Smart Retail Sales & Profit Intelligence Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557c.svg)](https://matplotlib.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)

RetailIQ is an interactive, enterprise-grade business intelligence dashboard designed for modern retail operators, financial analysts, and store managers. It bridges the gap between raw CSV sales data and strategic profit decisions.

Built entirely with **Python**, **Streamlit**, and **Matplotlib**, RetailIQ delivers instant executive visibility, detects silent profit leaks, flags statistical sales anomalies, models pricing changes with a What-If simulator, and generates data-backed business recommendations.

---

## 🌟 Key Features

### 1. 📊 Executive Overview Dashboard
- **Real-time KPI Metrics**: Total Revenue, Net Profit, Total Orders, Units Sold, Average Order Value (AOV), and Net Profit Margin (%).
- **Top Performer Cards**: Instantly identifies the best-selling product, highest-margin category, and leading geographic territory.
- **Automated Business Insights**: Plain-English, data-driven takeaways summarizing category dominance, month-over-month growth, weekend vs. weekday sales splits, and regional revenue shares.
- **High-Level Progression Charts**: Monthly revenue vs. profit trajectories and category distributions.

### 2. 📈 In-Depth Sales Analytics
- **Monthly Revenue Trend**: Smooth line chart with area fill and point markers.
- **Profit by Category**: Horizontal bar chart clearly distinguishing positive margin categories from loss leaders.
- **Revenue vs. Profit Comparison**: Direct side-by-side grouped bar charts visualizing margin conversion per category.
- **Geographic Analysis**: Regional sales volume and operating margins.
- **Temporal Analysis**: Day-of-week sales footprint (weekday vs. weekend performance).

### 3. 📦 SKU & Product Performance Matrix
- **Top 10 Product Ranking**: Ranked revenue bar chart with exact value annotations.
- **Volume vs. Margin Bubble Matrix**: Visual distribution plotting sales volume against margin percentage with bubble size scaled to revenue.
- **Complete SKU Profitability Table**: Detailed tabular breakdown with sorting and formatting.

### 4. ⚠️ Unique Feature 1: Profit Leak Detector
- **Margin Risk Engine**: Identifies products that drive gross revenue but fail to generate healthy bottom-line profits.
- **Transparent Rule-Based Classification**:
  - `Healthy`: Margin $\ge 20\%$
  - `Low Margin`: $5\% \le \text{Margin} < 20\%$
  - `Profit Warning`: $0\% \le \text{Margin} < 5\%$ (Volume traps)
  - `Loss Making`: $\text{Margin} < 0\%$ (Immediate leak)
- **Visual Profit-Risk Quadrant**: Scatter plot mapping Revenue against Profit Margin with break-even threshold lines.
- **Automated Actionable Diagnosis**: Pinpoints exact root causes (e.g., supplier cost inflation, excessive clearance discounts).

### 5. 🔍 Unique Feature 2: Sales Anomaly Detector
- **Statistical Outlier Surveillance**: Uses a 7-day rolling mean and standard deviation ($\pm 1.96\sigma$ corridor).
- **Outlier Classification**:
  - **Spikes**: Days where sales exceed the upper confidence boundary (promotional surges, holiday peaks, bulk orders).
  - **Drops**: Days where sales plunge below the lower confidence boundary (stockouts, server downtime, payment gateway failures).
- **Interactive Anomaly Visualization**: Matplotlib timeline highlighting normal corridors, spike triangles (green), and drop triangles (red).
- **Contextual Anomaly Log**: Detailed audit log with calculated deviation percentages and business diagnosis.

### 6. 🔮 Sales Forecasting Module
- **Moving-Average Forecast**: Projects sales revenue for the next 3 consecutive months using weighted moving averages and linear momentum.
- **Forecast Chart**: Seamless transition from actual historical data to projected future months with confidence interval bands ($\pm 10\%$).
- **Data Sufficiency Engine**: Validates minimum historical requirements (requires at least 3 months) and displays friendly guidance if data is insufficient.

### 7. 🎛️ Unique Feature 3: What-If Profit Simulator
- **Dynamic Scenario Modeler**: Interactive sliders allow users to simulate adjustments to:
  - Retail Selling Price ($-30\%$ to $+50\%$)
  - Supplier Unit Cost ($-30\%$ to $+50\%$)
  - Promotional Discount Rate ($0\%$ to $50\%$)
- **Side-by-Side Financial Impact**: Compares baseline vs. simulated Revenue, Profit, Margin, and Percentage Change in Profit.
- **Comparative Chart**: Instant visual comparison of Revenue, Cost, and Profit before and after strategic adjustments.
- **Automated Strategic Narrative**: Explains the exact dollar impact and strategic desirability of the scenario.

### 8. 📑 Executive Reports & Export Center
- **Filtered Dataset Export**: Download raw filtered transactions as a clean CSV.
- **SKU Profitability Audit**: Export aggregated product-level metrics (units sold, cost, revenue, profit, margin).
- **Executive Briefing**: Instant download of a comprehensive formatted text briefing summarizing KPIs, category contributions, and anomalies.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Frontend UI** | Streamlit |
| **Data Engine** | Pandas, NumPy |
| **Visualizations** | Matplotlib, Seaborn |
| **Styling** | Custom SaaS Dark Navy Theme (CSS) |

---

## 📂 Project Structure

```
RetailIQ/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python package dependencies
├── sample_sales.csv       # Realistic 160+ row sample dataset
├── generate_sample.py     # Script to regenerate sample data
└── README.md              # Project documentation
```

---

## 🚀 Installation & Getting Started

### 1. Clone or Navigate to the Workspace
```bash
cd "C:\Users\Aryan jain\.gemini\antigravity\scratch\RetailIQ"
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 📊 CSV File Requirements & Column Mapping

RetailIQ supports standard retail datasets. The engine automatically handles common column aliases:

| Standard Name | Accepted Aliases | Description |
|---|---|---|
| **Date** | `Order Date`, `Transaction Date`, `order_date` | Date of transaction |
| **Product** | `Item`, `Product Name`, `Product Title` | SKU or item name |
| **Category** | `Category Name`, `Cat` | Product category |
| **Quantity** | `Qty`, `Units`, `Volume` | Number of units purchased |
| **Unit Price** | `Price`, `unit_price` | List price per unit |
| **Unit Cost** | `Cost`, `unit_cost`, `Cost Price` | Wholesale cost per unit |
| **Discount** | `Discount Amount`, `Disc` | Discount applied |
| **Sales** | `Revenue`, `Total Sales`, `Net Sales` | Final gross sales amount |
| **Profit** | `Net Profit`, `Margin` | Net earnings |
| **Region** | `Location`, `Territory`, `Zone` | Store or geographic region |

### Automatic Calculations:
- If **Sales** is missing: $\text{Sales} = (\text{Quantity} \times \text{Unit Price}) - \text{Discount}$
- If **Profit** is missing: $\text{Profit} = \text{Sales} - (\text{Quantity} \times \text{Unit Cost})$
- If **Discount** is missing: Defaulted to `0.0`
- Safe division handling prevents application crashes from zero sales or missing inputs.
- Users can download a pre-formatted template CSV directly from the sidebar.

---

## 🧪 Testing Verification

The application has been verified against the 12 core test requirements:
- [x] Application launches cleanly on Streamlit.
- [x] Sample CSV loads with full data integrity.
- [x] Custom CSV upload and dynamic column mapping functional.
- [x] Financial formulas (Sales, Profit, Margin, AOV) verified.
- [x] Dynamic multi-filters update all metrics and charts in real-time.
- [x] Matplotlib charts render with dark-navy SaaS theme styling.
- [x] Profit Leak Detector classifies risk statuses and highlights volume traps.
- [x] Sales Anomaly Detector isolates spikes and drops using rolling statistics.
- [x] What-If Simulator calculates dynamic pricing and discount sensitivity.
- [x] Sales forecasting projects moving averages with uncertainty corridors.
- [x] Report exports generate valid CSV and TXT files.
- [x] Graceful error handling for missing fields and empty filter results.

---

## 📄 License
RetailIQ is an open-source analytics project developed for commercial retail intelligence.
