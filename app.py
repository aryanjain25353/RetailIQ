"""
RetailIQ – Smart Retail Sales & Profit Intelligence Dashboard
A commercial-grade retail analytics and business intelligence application
built with Python, Streamlit, Pandas, NumPy, and Matplotlib.
"""

import io
import os
import math
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import streamlit as st

# ==============================================================================
# 1. APPLICATION CONSTANTS & STYLING
# ==============================================================================

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    .header-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #312e81;
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    .header-box h1 {
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .header-box p {
        color: #94a3b8;
        font-size: 1.05rem;
        margin: 6px 0 0 0;
    }
    
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    .kpi-revenue::before { background: #3b82f6; }
    .kpi-profit::before { background: #10b981; }
    .kpi-orders::before { background: #6366f1; }
    .kpi-units::before { background: #8b5cf6; }
    .kpi-aov::before { background: #06b6d4; }
    .kpi-margin::before { background: #f59e0b; }
    
    .kpi-label {
        color: #94a3b8;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-subtext {
        font-size: 0.78rem;
        color: #64748b;
        margin-top: 6px;
    }
    
    .highlight-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .highlight-title {
        color: #64748b;
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 600;
    }
    .highlight-val {
        color: #e2e8f0;
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 2px;
    }
    
    .insight-card {
        background: #1e293b;
        border-left: 4px solid #6366f1;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin-bottom: 12px;
        color: #e2e8f0;
        font-size: 0.93rem;
    }
    .insight-card strong {
        color: #818cf8;
    }
    
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 16px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
"""

STANDARD_COLUMNS = {
    'date': 'Date',
    'product': 'Product',
    'category': 'Category',
    'quantity': 'Quantity',
    'unit price': 'Unit Price',
    'unit cost': 'Unit Cost',
    'discount': 'Discount',
    'sales': 'Sales',
    'profit': 'Profit',
    'region': 'Region'
}

ALIAS_MAP = {
    'order date': 'Date',
    'transaction date': 'Date',
    'order_date': 'Date',
    'item': 'Product',
    'product name': 'Product',
    'product_name': 'Product',
    'product title': 'Product',
    'category name': 'Category',
    'cat': 'Category',
    'qty': 'Quantity',
    'units': 'Quantity',
    'volume': 'Quantity',
    'price': 'Unit Price',
    'unit_price': 'Unit Price',
    'cost': 'Unit Cost',
    'unit_cost': 'Unit Cost',
    'cost price': 'Unit Cost',
    'discount amount': 'Discount',
    'disc': 'Discount',
    'revenue': 'Sales',
    'total amount': 'Sales',
    'total sales': 'Sales',
    'total_sales': 'Sales',
    'net sales': 'Sales',
    'net profit': 'Profit',
    'total profit': 'Profit',
    'margin': 'Profit',
    'location': 'Region',
    'territory': 'Region',
    'zone': 'Region'
}


def apply_chart_style(ax, fig=None):
    """Applies consistent dark-navy theme to Matplotlib axes and figures."""
    if fig:
        fig.patch.set_facecolor('#1e293b')
    ax.set_facecolor('#1e293b')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#334155')
        spine.set_linewidth(0.8)
    ax.xaxis.label.set_color('#cbd5e1')
    ax.yaxis.label.set_color('#cbd5e1')
    ax.title.set_color('#f8fafc')
    ax.grid(True, linestyle='--', alpha=0.15, color='#cbd5e1')


# ==============================================================================
# 2. DATA PROCESSING & VALIDATION ENGINE
# ==============================================================================

def clean_and_validate_data(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Validates, standardizes, and computes missing financial metrics.
    Returns cleaned DataFrame and list of system diagnostic notes.
    """
    notes = []
    if df.empty:
        raise ValueError("The provided CSV file contains no records.")

    # Standardize column headers: strip whitespace & case-insensitive match
    col_rename = {}
    for col in df.columns:
        norm = str(col).strip().lower()
        if norm in STANDARD_COLUMNS:
            col_rename[col] = STANDARD_COLUMNS[norm]
        elif norm in ALIAS_MAP:
            col_rename[col] = ALIAS_MAP[norm]
            notes.append(f"Auto-mapped column '{col}' to standard '{ALIAS_MAP[norm]}'.")

    df = df.rename(columns=col_rename)

    # Check for minimal required columns
    required_cols = ['Product', 'Quantity']
    for req in required_cols:
        if req not in df.columns:
            raise ValueError(f"Missing essential column '{req}'. Please map or include this column.")

    # Date Handling
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        invalid_dates = df['Date'].isna().sum()
        if invalid_dates > 0:
            notes.append(f"Found {invalid_dates} invalid or missing dates; replaced with current date.")
            df['Date'] = df['Date'].fillna(pd.Timestamp.today())
    else:
        notes.append("No 'Date' column found. Defaulted to generated daily sequential dates.")
        df['Date'] = pd.date_range(end=pd.Timestamp.today(), periods=len(df), freq='D')

    # Category & Region fallbacks
    if 'Category' not in df.columns:
        df['Category'] = 'General'
        notes.append("No 'Category' column found. Defaulted all rows to 'General'.")
    else:
        df['Category'] = df['Category'].fillna('Uncategorized').astype(str)

    if 'Region' not in df.columns:
        df['Region'] = 'National'
        notes.append("No 'Region' column found. Defaulted all rows to 'National'.")
    else:
        df['Region'] = df['Region'].fillna('General').astype(str)

    df['Product'] = df['Product'].fillna('Unnamed Item').astype(str)

    # Numeric columns cleaning
    num_cols = ['Quantity', 'Unit Price', 'Unit Cost', 'Discount', 'Sales', 'Profit']
    for col in num_cols:
        if col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.replace(r'[\$,₹,€,£,]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    # Handle Quantities <= 0
    if (df['Quantity'] <= 0).any():
        zero_cnt = (df['Quantity'] <= 0).sum()
        notes.append(f"Adjusted {zero_cnt} non-positive quantity records to 1.")
        df['Quantity'] = df['Quantity'].apply(lambda q: 1 if q <= 0 else q)

    # Defaults for financial fields if missing
    if 'Discount' not in df.columns:
        df['Discount'] = 0.0

    if 'Unit Price' not in df.columns and 'Sales' in df.columns:
        df['Unit Price'] = (df['Sales'] + df['Discount']) / df['Quantity']
        notes.append("Calculated 'Unit Price' from Sales and Quantity.")
    elif 'Unit Price' not in df.columns:
        df['Unit Price'] = 10.0
        notes.append("Defaulted missing 'Unit Price' to $10.00.")

    if 'Unit Cost' not in df.columns and 'Profit' in df.columns and 'Sales' in df.columns:
        df['Unit Cost'] = np.maximum(0, (df['Sales'] - df['Profit']) / df['Quantity'])
        notes.append("Calculated 'Unit Cost' from Sales and Profit.")
    elif 'Unit Cost' not in df.columns:
        df['Unit Cost'] = df['Unit Price'] * 0.60
        notes.append("Defaulted missing 'Unit Cost' to 60% of Unit Price.")

    # Calculate missing Sales: Sales = Quantity * Unit Price - Discount
    if 'Sales' not in df.columns or (df['Sales'] == 0).all():
        df['Sales'] = (df['Quantity'] * df['Unit Price']) - df['Discount']
        notes.append("Computed 'Sales' as (Quantity × Unit Price − Discount).")

    # Calculate missing Profit: Profit = Sales - (Quantity * Unit Cost)
    if 'Profit' not in df.columns or (df['Profit'] == 0).all():
        df['Profit'] = df['Sales'] - (df['Quantity'] * df['Unit Cost'])
        notes.append("Computed 'Profit' as (Sales − Quantity × Unit Cost).")

    # Round numerical fields
    df['Sales'] = df['Sales'].round(2)
    df['Profit'] = df['Profit'].round(2)
    df['Unit Price'] = df['Unit Price'].round(2)
    df['Unit Cost'] = df['Unit Cost'].round(2)
    df['Discount'] = df['Discount'].round(2)

    # Sort chronological
    df = df.sort_values('Date').reset_index(drop=True)
    return df, notes


# ==============================================================================
# 3. SAMPLE DATA & TEMPLATE ENGINE
# ==============================================================================

@st.cache_data
def get_sample_data() -> pd.DataFrame:
    """Loads sample CSV from workspace directory or builds in-memory fallback."""
    sample_path = os.path.join(os.path.dirname(__file__), "sample_sales.csv")
    if os.path.exists(sample_path):
        return pd.read_csv(sample_path)
    
    # In-memory generator fallback
    np.random.seed(42)
    records = []
    base_date = datetime.now() - timedelta(days=180)
    products = [
        ("Ultra HD Smart TV 55\"", "Electronics", 480.0, 420.0),
        ("Wireless Headphones", "Electronics", 120.0, 55.0),
        ("Fast USB-C Charger Hub", "Electronics", 25.0, 24.5),
        ("Cotton Crewneck T-Shirt", "Apparel", 28.0, 10.0),
        ("Slim-Fit Denim Jeans", "Apparel", 55.0, 24.0),
        ("Ergonomic Office Chair", "Home & Kitchen", 195.0, 110.0),
        ("Ceramic Coffee Mug", "Home & Kitchen", 14.0, 13.5),
        ("Executive Notebook", "Office Supplies", 16.0, 5.0)
    ]
    regions = ["North", "South", "East", "West", "Central"]
    for i in range(120):
        dt = base_date + timedelta(days=int(np.random.randint(0, 180)))
        p_name, p_cat, price, cost = products[np.random.randint(0, len(products))]
        qty = int(np.random.choice([1, 2, 3, 4, 6], p=[0.4, 0.3, 0.15, 0.1, 0.05]))
        disc_rate = np.random.choice([0.0, 0.05, 0.10, 0.20], p=[0.5, 0.3, 0.15, 0.05])
        gross = qty * price
        disc = round(gross * disc_rate, 2)
        sales = round(gross - disc, 2)
        profit = round(sales - (qty * cost), 2)
        records.append({
            "Date": dt.strftime("%Y-%m-%d"),
            "Product": p_name,
            "Category": p_cat,
            "Quantity": qty,
            "Unit Price": price,
            "Unit Cost": cost,
            "Discount": disc,
            "Sales": sales,
            "Profit": profit,
            "Region": np.random.choice(regions)
        })
    return pd.DataFrame(records)

def generate_csv_template() -> str:
    """Provides a downloadable clean template CSV."""
    template_df = pd.DataFrame({
        "Date": ["2025-01-15", "2025-01-16", "2025-01-17"],
        "Product": ["Wireless Noise-Canceling Headphones", "Ergonomic Office Chair", "Premium Cotton T-Shirt"],
        "Category": ["Electronics", "Home & Kitchen", "Apparel"],
        "Quantity": [2, 1, 4],
        "Unit Price": [120.00, 195.00, 28.00],
        "Unit Cost": [55.00, 110.00, 10.00],
        "Discount": [12.00, 0.00, 5.60],
        "Sales": [228.00, 195.00, 106.40],
        "Profit": [118.00, 85.00, 66.40],
        "Region": ["North", "West", "South"]
    })
    return template_df.to_csv(index=False)


# ==============================================================================
# 4. MAIN STREAMLIT APPLICATION
# ==============================================================================

def main():
    st.set_page_config(
        page_title="RetailIQ – Retail Intelligence Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Sidebar Header
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 12px 0 16px 0;'>
        <h2 style='color: #6366f1; margin:0; font-size:1.8rem; font-weight:800; letter-spacing:-0.03em;'>RetailIQ</h2>
        <span style='color: #94a3b8; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;'>Sales & Profit Intelligence</span>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    page = st.sidebar.radio(
        "Navigation Menu",
        [
            "📊 Executive Dashboard",
            "📈 Sales Analysis",
            "📦 Product Performance",
            "⚠️ Profit Leak Detector",
            "🔍 Anomaly Detection",
            "🔮 Sales Forecast",
            "🎛️ What-If Simulator",
            "📑 Export Reports"
        ],
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Data Source")

    data_source = st.sidebar.radio(
        "Choose Dataset Mode:",
        ["Use Sample Dataset", "Upload Custom CSV"],
        index=0
    )

    raw_df = None
    if data_source == "Upload Custom CSV":
        uploaded_file = st.sidebar.file_uploader("Upload Retail CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                raw_df = pd.read_csv(uploaded_file)
                st.sidebar.success(f"Loaded {len(raw_df)} rows")
            except Exception as e:
                st.sidebar.error(f"Error parsing CSV: {str(e)}")
        else:
            st.sidebar.info("Upload a CSV file or switch to Sample Dataset.")
    else:
        raw_df = get_sample_data()

    # Download Template Button
    st.sidebar.download_button(
        label="📥 Download CSV Template",
        data=generate_csv_template(),
        file_name="retailiq_sample_template.csv",
        mime="text/csv",
        use_container_width=True
    )

    if raw_df is None:
        st.info("Please select or upload a dataset to begin.")
        st.stop()

    # Clean & Validate
    try:
        df_clean, validation_notes = clean_and_validate_data(raw_df)
    except Exception as e:
        st.error(f"Dataset Processing Error: {str(e)}")
        st.stop()

    # Column Mapping Expander
    with st.sidebar.expander("🛠️ Column Mapping Status", expanded=False):
        st.caption("Active Column Mappings:")
        cols_present = {c: ("✅ Present" if c in df_clean.columns else "❌ Missing") for c in STANDARD_COLUMNS.values()}
        st.json(cols_present)
        if validation_notes:
            st.caption("System Notes:")
            for n in validation_notes[:4]:
                st.caption(f"• {n}")

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Dynamic Filters")

    # Date Filter
    min_dt = df_clean['Date'].min().date()
    max_dt = df_clean['Date'].max().date()

    if min_dt < max_dt:
        selected_dates = st.sidebar.date_input(
            "Date Range",
            value=(min_dt, max_dt),
            min_value=min_dt,
            max_value=max_dt
        )
    else:
        selected_dates = (min_dt, max_dt)
        st.sidebar.caption(f"Date: {min_dt}")

    # Category Filter
    all_categories = sorted(df_clean['Category'].unique().tolist())
    selected_categories = st.sidebar.multiselect("Category", options=all_categories, default=all_categories)

    # Region Filter
    all_regions = sorted(df_clean['Region'].unique().tolist())
    selected_regions = st.sidebar.multiselect("Region", options=all_regions, default=all_regions)

    # Reset Filters Button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    # Apply Filters
    filtered_df = df_clean.copy()

    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
        start_d, end_d = selected_dates
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= start_d) & 
            (filtered_df['Date'].dt.date <= end_d)
        ]

    if selected_categories:
        filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]

    st.sidebar.markdown(f"**Filtered Records:** `{len(filtered_df):,}` of `{len(df_clean):,}`")

    if filtered_df.empty:
        st.warning("⚠️ No records match the current filter selection. Please expand your filter criteria.")
        st.stop()

    # KPI Computations
    total_revenue = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = len(filtered_df)
    total_units = int(filtered_df['Quantity'].sum())
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0.0

    # Best performers
    top_prod = filtered_df.groupby('Product')['Sales'].sum().idxmax() if not filtered_df.empty else "N/A"
    top_cat = filtered_df.groupby('Category')['Profit'].sum().idxmax() if not filtered_df.empty else "N/A"
    top_reg = filtered_df.groupby('Region')['Sales'].sum().idxmax() if not filtered_df.empty else "N/A"

    # Header Box
    st.markdown("""
    <div class="header-box">
        <h1>RetailIQ – Retail Intelligence Dashboard</h1>
        <p>Turn raw sales data into smarter business decisions.</p>
    </div>
    """, unsafe_allow_html=True)

    # PAGE ROUTING
    if page == "📊 Executive Dashboard":
        render_dashboard(filtered_df, total_revenue, total_profit, total_orders, total_units, avg_order_value, profit_margin, top_prod, top_cat, top_reg)
    elif page == "📈 Sales Analysis":
        render_sales_analysis(filtered_df)
    elif page == "📦 Product Performance":
        render_product_performance(filtered_df)
    elif page == "⚠️ Profit Leak Detector":
        render_profit_leak_detector(filtered_df)
    elif page == "🔍 Anomaly Detection":
        render_anomaly_detection(filtered_df)
    elif page == "🔮 Sales Forecast":
        render_sales_forecast(filtered_df)
    elif page == "🎛️ What-If Simulator":
        render_what_if_simulator(filtered_df)
    elif page == "📑 Export Reports":
        render_export_reports(filtered_df, total_revenue, total_profit, total_orders, total_units, avg_order_value, profit_margin, top_prod, top_cat, top_reg)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #64748b; font-size: 0.85rem; padding: 12px 0;'>"
        "RetailIQ – Smart Retail Sales & Profit Intelligence Dashboard &copy; 2026. Built with Streamlit & Matplotlib."
        "</div>",
        unsafe_allow_html=True
    )


# ==============================================================================
# 5. SUB-PAGE RENDERING MODULES
# ==============================================================================

def render_dashboard(filtered_df, total_revenue, total_profit, total_orders, total_units, avg_order_value, profit_margin, top_prod, top_cat, top_reg):
    st.markdown('<div class="section-header">📌 Executive Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-revenue">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">${total_revenue:,.2f}</div>
            <div class="kpi-subtext">Gross sales realized</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        profit_color = "#34d399" if total_profit >= 0 else "#f87171"
        st.markdown(f"""
        <div class="kpi-card kpi-profit">
            <div class="kpi-label">Total Profit</div>
            <div class="kpi-value" style="color: {profit_color};">${total_profit:,.2f}</div>
            <div class="kpi-subtext">Net earnings</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-orders">
            <div class="kpi-label">Transactions</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-subtext">Orders recorded</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card kpi-units">
            <div class="kpi-label">Units Sold</div>
            <div class="kpi-value">{total_units:,}</div>
            <div class="kpi-subtext">Items shipped</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="kpi-card kpi-aov">
            <div class="kpi-label">Avg Order Value</div>
            <div class="kpi-value">${avg_order_value:,.2f}</div>
            <div class="kpi-subtext">Per transaction</div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        margin_color = "#34d399" if profit_margin >= 20 else ("#fbbf24" if profit_margin >= 10 else "#f87171")
        st.markdown(f"""
        <div class="kpi-card kpi-margin">
            <div class="kpi-label">Profit Margin</div>
            <div class="kpi-value" style="color: {margin_color};">{profit_margin:.1f}%</div>
            <div class="kpi-subtext">Return on sales</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hcol1, hcol2, hcol3, hcol4 = st.columns(4)
    with hcol1:
        st.markdown(f"""
        <div class="highlight-card">
            <div class="highlight-title">Top Selling Product</div>
            <div class="highlight-val">{top_prod}</div>
        </div>
        """, unsafe_allow_html=True)
    with hcol2:
        st.markdown(f"""
        <div class="highlight-card">
            <div class="highlight-title">Most Profitable Category</div>
            <div class="highlight-val">{top_cat}</div>
        </div>
        """, unsafe_allow_html=True)
    with hcol3:
        st.markdown(f"""
        <div class="highlight-card">
            <div class="highlight-title">Leading Region</div>
            <div class="highlight-val">{top_reg}</div>
        </div>
        """, unsafe_allow_html=True)
    with hcol4:
        date_str = f"{filtered_df['Date'].min().strftime('%b %d, %Y')} – {filtered_df['Date'].max().strftime('%b %d, %Y')}"
        st.markdown(f"""
        <div class="highlight-card">
            <div class="highlight-title">Active Date Window</div>
            <div class="highlight-val" style="font-size:0.92rem;">{date_str}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">💡 Automated Business Insights</div>', unsafe_allow_html=True)
    insights = []
    cat_sales = filtered_df.groupby('Category')['Sales'].sum()
    top_cat_share = (cat_sales.max() / total_revenue * 100) if total_revenue > 0 else 0
    insights.append(f"**{cat_sales.idxmax()}** dominates category performance, contributing **{top_cat_share:.1f}%** (${cat_sales.max():,.2f}) of total revenue.")
    
    monthly_df = filtered_df.set_index('Date').resample('ME')['Sales'].sum()
    if len(monthly_df) >= 2:
        last_m = monthly_df.iloc[-1]
        prev_m = monthly_df.iloc[-2]
        mom_change = ((last_m - prev_m) / prev_m * 100) if prev_m > 0 else 0
        direction = "increased" if mom_change >= 0 else "decreased"
        insights.append(f"Latest monthly sales **{direction} by {abs(mom_change):.1f}%** compared to the preceding month (${last_m:,.2f} vs ${prev_m:,.2f}).")
    
    prod_profit = filtered_df.groupby('Product')[['Sales', 'Profit']].sum()
    prod_profit['Margin'] = (prod_profit['Profit'] / prod_profit['Sales'] * 100).fillna(0)
    best_margin_prod = prod_profit['Margin'].idxmax()
    insights.append(f"**{best_margin_prod}** yields the strongest profit margin at **{prod_profit.loc[best_margin_prod, 'Margin']:.1f}%**.")

    filtered_df['IsWeekend'] = filtered_df['Date'].dt.dayofweek >= 5
    weekend_rev = filtered_df[filtered_df['IsWeekend']]['Sales'].sum()
    weekend_share = (weekend_rev / total_revenue * 100) if total_revenue > 0 else 0
    insights.append(f"Weekend orders account for **{weekend_share:.1f}%** of total sales revenue.")
    
    reg_sales = filtered_df.groupby('Region')['Sales'].sum()
    top_reg_share = (reg_sales.max() / total_revenue * 100) if total_revenue > 0 else 0
    insights.append(f"The **{reg_sales.idxmax()} Region** represents the highest regional sales concentration (**{top_reg_share:.1f}%** share).")

    icol1, icol2 = st.columns(2)
    for i, ins in enumerate(insights):
        target_col = icol1 if i % 2 == 0 else icol2
        with target_col:
            st.markdown(f'<div class="insight-card">{ins}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📈 Performance Summary Charts</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Monthly Revenue & Profit Progression")
        m_agg = filtered_df.set_index('Date').resample('ME')[['Sales', 'Profit']].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4.2), dpi=100)
        apply_chart_style(ax, fig)
        
        if not m_agg.empty:
            x_labels = m_agg['Date'].dt.strftime('%b %Y')
            ax.plot(x_labels, m_agg['Sales'], marker='o', linewidth=2.5, color='#38bdf8', label='Revenue')
            ax.plot(x_labels, m_agg['Profit'], marker='s', linewidth=2.5, color='#10b981', label='Profit')
            ax.fill_between(x_labels, m_agg['Profit'], color='#10b981', alpha=0.12)
            ax.fill_between(x_labels, m_agg['Sales'], m_agg['Profit'], color='#38bdf8', alpha=0.08)
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
            plt.xticks(rotation=25, ha='right')
            ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#cbd5e1')
            ax.set_title("Revenue vs. Profit Trend", fontsize=11, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with c2:
        st.subheader("Sales Breakdown by Category")
        cat_agg = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(8, 4.2), dpi=100)
        apply_chart_style(ax, fig)
        
        bars = ax.barh(cat_agg.index, cat_agg.values, color='#6366f1', edgecolor='#818cf8', height=0.6)
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        for bar in bars:
            w = bar.get_width()
            ax.annotate(f'${w:,.0f}',
                        xy=(w, bar.get_y() + bar.get_height() / 2),
                        xytext=(6, 0), textcoords="offset points",
                        ha='left', va='center', color='#f1f5f9', fontsize=8.5, fontweight='bold')
        ax.set_xlim(0, cat_agg.max() * 1.22 if not cat_agg.empty else 100)
        ax.set_title("Revenue by Retail Category", fontsize=11, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


def render_sales_analysis(filtered_df):
    st.markdown('<div class="section-header">📈 Comprehensive Sales Analytics</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Revenue & Profit Dynamics", "🌍 Regional Intelligence", "📅 Temporal & Day Patterns"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("1. Monthly Revenue Trend")
            m_agg = filtered_df.set_index('Date').resample('ME')['Sales'].sum().reset_index()
            fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
            apply_chart_style(ax, fig)
            
            x_labels = m_agg['Date'].dt.strftime('%b %Y')
            ax.plot(x_labels, m_agg['Sales'], marker='o', markersize=6, linewidth=2.8, color='#3b82f6', label='Sales')
            ax.fill_between(x_labels, m_agg['Sales'], color='#3b82f6', alpha=0.15)
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
            ax.set_ylabel("Sales ($ USD)")
            ax.set_title("Monthly Gross Sales Velocity", fontsize=11, fontweight='bold', pad=12)
            plt.xticks(rotation=30, ha='right')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with col_b:
            st.subheader("2. Profit Contribution by Category")
            p_cat = filtered_df.groupby('Category')['Profit'].sum().sort_values(ascending=True)
            fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
            apply_chart_style(ax, fig)
            
            colors = ['#10b981' if p >= 0 else '#ef4444' for p in p_cat.values]
            bars = ax.barh(p_cat.index, p_cat.values, color=colors, height=0.55)
            ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
            for bar in bars:
                w = bar.get_width()
                offset = 6 if w >= 0 else -6
                ha = 'left' if w >= 0 else 'right'
                ax.annotate(f'${w:,.0f}',
                            xy=(w, bar.get_y() + bar.get_height() / 2),
                            xytext=(offset, 0), textcoords="offset points",
                            ha=ha, va='center', color='#f8fafc', fontsize=8.5, fontweight='bold')
            ax.axvline(0, color='#64748b', linewidth=1)
            ax.set_title("Net Profit Generated by Category", fontsize=11, fontweight='bold', pad=12)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.subheader("3. Revenue vs Profit Cross-Comparison")
        comp_df = filtered_df.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
        fig, ax = plt.subplots(figsize=(10, 4.5), dpi=100)
        apply_chart_style(ax, fig)
        
        x = np.arange(len(comp_df))
        width = 0.35
        rects1 = ax.bar(x - width/2, comp_df['Sales'], width, label='Revenue', color='#3b82f6')
        rects2 = ax.bar(x + width/2, comp_df['Profit'], width, label='Profit', color='#10b981')
        
        ax.set_xticks(x)
        ax.set_xticklabels(comp_df['Category'], rotation=15, ha='right')
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        ax.set_ylabel("Amount ($ USD)")
        ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#cbd5e1')
        ax.set_title("Revenue Conversion to Net Profit per Category", fontsize=11, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with tab2:
        st.subheader("Regional Performance Benchmark")
        r_col1, r_col2 = st.columns(2)
        
        reg_df = filtered_df.groupby('Region').agg(
            Revenue=('Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Transactions=('Sales', 'count'),
            Units=('Quantity', 'sum')
        ).reset_index()
        reg_df['Margin'] = (reg_df['Profit'] / reg_df['Revenue'] * 100).round(1)

        with r_col1:
            fig, ax = plt.subplots(figsize=(7, 4.5), dpi=100)
            apply_chart_style(ax, fig)
            bars = ax.bar(reg_df['Region'], reg_df['Revenue'], color='#8b5cf6', width=0.55)
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
            for bar in bars:
                h = bar.get_height()
                ax.annotate(f'${h:,.0f}',
                            xy=(bar.get_x() + bar.get_width() / 2, h),
                            xytext=(0, 4), textcoords="offset points",
                            ha='center', va='bottom', color='#f8fafc', fontsize=8.5, fontweight='bold')
            ax.set_title("Sales by Geographic Region", fontsize=11, fontweight='bold', pad=12)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with r_col2:
            fig, ax = plt.subplots(figsize=(7, 4.5), dpi=100)
            apply_chart_style(ax, fig)
            bars = ax.bar(reg_df['Region'], reg_df['Margin'], color='#06b6d4', width=0.55)
            for bar in bars:
                h = bar.get_height()
                ax.annotate(f'{h:.1f}%',
                            xy=(bar.get_x() + bar.get_width() / 2, h),
                            xytext=(0, 4), textcoords="offset points",
                            ha='center', va='bottom', color='#f8fafc', fontsize=8.5, fontweight='bold')
            ax.set_ylabel("Profit Margin (%)")
            ax.set_title("Operating Margin by Geographic Region", fontsize=11, fontweight='bold', pad=12)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.dataframe(
            reg_df.style.format({
                'Revenue': '${:,.2f}',
                'Profit': '${:,.2f}',
                'Margin': '{:.1f}%',
                'Transactions': '{:,}',
                'Units': '{:,}'
            }),
            use_container_width=True
        )

    with tab3:
        st.subheader("Day-of-Week Sales Distribution")
        filtered_df['DayName'] = filtered_df['Date'].dt.day_name()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_agg = filtered_df.groupby('DayName')['Sales'].sum().reindex(days_order).fillna(0)
        
        fig, ax = plt.subplots(figsize=(9, 4.2), dpi=100)
        apply_chart_style(ax, fig)
        
        bar_colors = ['#4f46e5' if d not in ['Saturday', 'Sunday'] else '#ec4899' for d in day_agg.index]
        bars = ax.bar(day_agg.index, day_agg.values, color=bar_colors, width=0.55)
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f'${h:,.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 4), textcoords="offset points",
                        ha='center', va='bottom', color='#cbd5e1', fontsize=8.5)
        ax.set_title("Weekday vs Weekend Sales Footprint", fontsize=11, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


def render_product_performance(filtered_df):
    st.markdown('<div class="section-header">📦 SKU & Product Performance Matrix</div>', unsafe_allow_html=True)
    prod_summary = filtered_df.groupby('Product').agg(
        Category=('Category', 'first'),
        Units_Sold=('Quantity', 'sum'),
        Revenue=('Sales', 'sum'),
        Total_Cost=('Unit Cost', lambda c: (c * filtered_df.loc[c.index, 'Quantity']).sum()),
        Total_Profit=('Profit', 'sum'),
        Avg_Discount=('Discount', 'mean')
    ).reset_index()

    prod_summary['Margin'] = np.where(
        prod_summary['Revenue'] > 0,
        (prod_summary['Total_Profit'] / prod_summary['Revenue'] * 100).round(1),
        0.0
    )

    top_10 = prod_summary.sort_values('Revenue', ascending=True).tail(10)
    pcol1, pcol2 = st.columns([1.2, 1])
    
    with pcol1:
        st.subheader("Top 10 Products by Revenue")
        fig, ax = plt.subplots(figsize=(8, 5.5), dpi=100)
        apply_chart_style(ax, fig)
        
        bars = ax.barh(top_10['Product'], top_10['Revenue'], color='#3b82f6', height=0.6)
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        for bar in bars:
            w = bar.get_width()
            ax.annotate(f'${w:,.0f}',
                        xy=(w, bar.get_y() + bar.get_height() / 2),
                        xytext=(6, 0), textcoords="offset points",
                        ha='left', va='center', color='#f8fafc', fontsize=8, fontweight='bold')
        ax.set_xlim(0, top_10['Revenue'].max() * 1.25)
        ax.set_title("Revenue Generation per Top SKU", fontsize=11, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with pcol2:
        st.subheader("Volume vs Profit Margin Distribution")
        fig, ax = plt.subplots(figsize=(7, 5.5), dpi=100)
        apply_chart_style(ax, fig)
        
        colors = ['#10b981' if m >= 20 else ('#f59e0b' if m >= 5 else '#ef4444') for m in prod_summary['Margin']]
        scatter = ax.scatter(
            prod_summary['Units_Sold'],
            prod_summary['Margin'],
            s=prod_summary['Revenue'] / (prod_summary['Revenue'].max() + 1) * 450 + 50,
            c=colors,
            alpha=0.75,
            edgecolors='#f8fafc',
            linewidths=0.8
        )
        ax.axhline(0, color='#ef4444', linestyle='--', linewidth=1, label='Break-even (0%)')
        ax.axhline(20, color='#10b981', linestyle=':', linewidth=1, label='Target Margin (20%)')
        ax.set_xlabel("Units Sold (Volume)")
        ax.set_ylabel("Profit Margin (%)")
        ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#cbd5e1', loc='lower right')
        ax.set_title("Product Volume vs. Margin % (Bubble = Revenue)", fontsize=10, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.subheader("Complete SKU Profitability Table")
    st.dataframe(
        prod_summary.sort_values('Revenue', ascending=False).style.format({
            'Units_Sold': '{:,}',
            'Revenue': '${:,.2f}',
            'Total_Cost': '${:,.2f}',
            'Total_Profit': '${:,.2f}',
            'Avg_Discount': '${:,.2f}',
            'Margin': '{:.1f}%'
        }),
        use_container_width=True
    )


def render_profit_leak_detector(filtered_df):
    st.markdown('<div class="section-header">⚠️ Profit Leak Detector: Margin Risk Engine</div>', unsafe_allow_html=True)
    st.caption("Identify high-revenue, low-margin products, hidden clearance losses, and heavy discount erosion.")

    leak_df = filtered_df.groupby('Product').agg(
        Category=('Category', 'first'),
        Units=('Quantity', 'sum'),
        Revenue=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Avg_Discount=('Discount', 'mean'),
        Unit_Price=('Unit Price', 'mean'),
        Unit_Cost=('Unit Cost', 'mean')
    ).reset_index()

    leak_df['Cost'] = leak_df['Revenue'] - leak_df['Profit']
    leak_df['Margin'] = np.where(leak_df['Revenue'] > 0, (leak_df['Profit'] / leak_df['Revenue'] * 100).round(1), 0.0)

    def classify_status(row):
        if row['Margin'] < 0:
            return "Loss Making"
        elif row['Margin'] < 5.0:
            return "Profit Warning"
        elif row['Margin'] < 20.0:
            return "Low Margin"
        else:
            return "Healthy"

    leak_df['Status'] = leak_df.apply(classify_status, axis=1)

    status_counts = leak_df['Status'].value_counts()
    loss_count = status_counts.get("Loss Making", 0)
    warn_count = status_counts.get("Profit Warning", 0)
    low_count = status_counts.get("Low Margin", 0)
    healthy_count = status_counts.get("Healthy", 0)

    lcol1, lcol2, lcol3, lcol4 = st.columns(4)
    with lcol1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #ef4444;">
            <div class="kpi-label">Loss-Making Products</div>
            <div class="kpi-value" style="color: #f87171;">{loss_count}</div>
            <div class="kpi-subtext">Immediate action required</div>
        </div>
        """, unsafe_allow_html=True)
    with lcol2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #f97316;">
            <div class="kpi-label">Profit Warnings (<5%)</div>
            <div class="kpi-value" style="color: #fb923c;">{warn_count}</div>
            <div class="kpi-subtext">Volume without profit</div>
        </div>
        """, unsafe_allow_html=True)
    with lcol3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #f59e0b;">
            <div class="kpi-label">Low Margin (5–20%)</div>
            <div class="kpi-value" style="color: #fbbf24;">{low_count}</div>
            <div class="kpi-subtext">Sub-optimal pricing</div>
        </div>
        """, unsafe_allow_html=True)
    with lcol4:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #10b981;">
            <div class="kpi-label">Healthy Products (>20%)</div>
            <div class="kpi-value" style="color: #34d399;">{healthy_count}</div>
            <div class="kpi-subtext">Core profit drivers</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔍 Automated Profit Diagnostic Insights</div>', unsafe_allow_html=True)
    leak_insights = []
    
    loss_items = leak_df[leak_df['Status'] == 'Loss Making']
    if not loss_items.empty:
        for _, row in loss_items.iterrows():
            leak_insights.append(
                f"🚨 **LOSS LEAK:** **{row['Product']}** generated **${row['Revenue']:,.2f}** in revenue but incurred a net loss of **-${abs(row['Profit']):,.2f}** (Margin: **{row['Margin']:.1f}%**). *Recommendation: Halt clearance discounts immediately or renegotiate unit cost (${row['Unit_Cost']:.2f}).*"
            )
            
    warn_items = leak_df[leak_df['Status'] == 'Profit Warning'].sort_values('Revenue', ascending=False)
    if not warn_items.empty:
        for _, row in warn_items.head(2).iterrows():
            leak_insights.append(
                f"⚠️ **VOLUME TRAP:** **{row['Product']}** produced significant revenue of **${row['Revenue']:,.2f}** but only **${row['Profit']:,.2f}** in profit. Its razor-thin margin (**{row['Margin']:.1f}%**) indicates dangerous revenue churn. *Recommendation: Increase retail price by 3–5% or cap promotions.*"
            )

    low_items = leak_df[leak_df['Status'] == 'Low Margin'].sort_values('Revenue', ascending=False)
    if not low_items.empty and len(leak_insights) < 3:
        top_low = low_items.iloc[0]
        leak_insights.append(
            f"⚡ **MARGIN OPTIMIZATION:** **{top_low['Product']}** operates at **{top_low['Margin']:.1f}%** margin across {top_low['Units']} units. Average discount was ${top_low['Avg_Discount']:.2f}. *Recommendation: Test a reduced discount tier to recapture profit without hurting volume.*"
        )
        
    if not leak_insights:
        leak_insights.append("✅ **All products in the selected dataset maintain healthy margins exceeding 20%. No acute profit leaks detected.**")

    for ins in leak_insights:
        st.markdown(f'<div class="insight-card">{ins}</div>', unsafe_allow_html=True)

    st.subheader("Visual Profit-Risk Quadrant Map")
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=100)
    apply_chart_style(ax, fig)
    
    color_map = {
        "Healthy": "#10b981",
        "Low Margin": "#f59e0b",
        "Profit Warning": "#f97316",
        "Loss Making": "#ef4444"
    }
    
    for status, grp in leak_df.groupby('Status'):
        ax.scatter(
            grp['Revenue'],
            grp['Margin'],
            label=status,
            color=color_map.get(status, '#94a3b8'),
            s=120,
            alpha=0.85,
            edgecolors='#ffffff',
            linewidths=0.9
        )
        for _, r in grp.iterrows():
            if r['Status'] in ['Loss Making', 'Profit Warning'] or r['Revenue'] > leak_df['Revenue'].quantile(0.85):
                ax.annotate(r['Product'],
                            (r['Revenue'], r['Margin']),
                            textcoords="offset points",
                            xytext=(0, 8),
                            ha='center',
                            fontsize=7.5,
                            color='#f8fafc',
                            fontweight='semibold')
                
    ax.axhline(0, color='#ef4444', linestyle='--', linewidth=1.2, label='Break-Even Margin')
    ax.axhline(20, color='#10b981', linestyle=':', linewidth=1.2, label='Target Benchmark (20%)')
    ax.set_xlabel("Total Product Revenue ($ USD)")
    ax.set_ylabel("Profit Margin (%)")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#cbd5e1', loc='lower right')
    ax.set_title("Product Revenue vs Margin Risk Quadrant", fontsize=11, fontweight='bold', pad=12)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.subheader("Product Profitability & Risk Ranking Table")
    selected_status = st.multiselect(
        "Filter by Risk Status:",
        options=["Loss Making", "Profit Warning", "Low Margin", "Healthy"],
        default=["Loss Making", "Profit Warning", "Low Margin", "Healthy"]
    )
    
    display_leak = leak_df[leak_df['Status'].isin(selected_status)].sort_values('Profit', ascending=True)
    st.dataframe(
        display_leak[['Product', 'Category', 'Revenue', 'Cost', 'Profit', 'Margin', 'Status']].style.format({
            'Revenue': '${:,.2f}',
            'Cost': '${:,.2f}',
            'Profit': '${:,.2f}',
            'Margin': '{:.1f}%'
        }),
        use_container_width=True
    )


def render_anomaly_detection(filtered_df):
    st.markdown('<div class="section-header">🔍 Sales Anomaly Detector: Statistical Pattern Recognition</div>', unsafe_allow_html=True)
    st.caption("Detect unexpected sales drops, promotional spikes, and irregular daily sales deviations using rolling statistics.")

    daily_sales = filtered_df.groupby(filtered_df['Date'].dt.date)['Sales'].sum().reset_index()
    daily_sales.columns = ['Date', 'Sales']
    daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])
    daily_sales = daily_sales.sort_values('Date').reset_index(drop=True)

    if len(daily_sales) < 7:
        st.warning("Anomaly detection requires at least 7 days of sales data to compute statistical baselines.")
    else:
        window = 7
        daily_sales['Rolling_Mean'] = daily_sales['Sales'].rolling(window=window, min_periods=3, center=True).mean()
        daily_sales['Rolling_Std'] = daily_sales['Sales'].rolling(window=window, min_periods=3, center=True).std().fillna(0)
        daily_sales['Upper_Bound'] = daily_sales['Rolling_Mean'] + (1.96 * daily_sales['Rolling_Std'])
        daily_sales['Lower_Bound'] = (daily_sales['Rolling_Mean'] - (1.96 * daily_sales['Rolling_Std'])).clip(lower=0)
        
        def detect_type(row):
            if row['Sales'] > row['Upper_Bound'] and row['Rolling_Std'] > 0:
                return 'Spike'
            elif row['Sales'] < row['Lower_Bound'] and row['Rolling_Std'] > 0:
                return 'Drop'
            return 'Normal'

        daily_sales['Anomaly_Type'] = daily_sales.apply(detect_type, axis=1)
        anomalies = daily_sales[daily_sales['Anomaly_Type'] != 'Normal'].copy()

        acol1, acol2, acol3 = st.columns(3)
        with acol1:
            st.markdown(f"""
            <div class="kpi-card" style="border-top: 4px solid #6366f1;">
                <div class="kpi-label">Total Outliers Detected</div>
                <div class="kpi-value">{len(anomalies)}</div>
                <div class="kpi-subtext">Across {len(daily_sales)} calendar days</div>
            </div>
            """, unsafe_allow_html=True)
        with acol2:
            spike_cnt = (anomalies['Anomaly_Type'] == 'Spike').sum()
            st.markdown(f"""
            <div class="kpi-card" style="border-top: 4px solid #10b981;">
                <div class="kpi-label">Revenue Spikes</div>
                <div class="kpi-value" style="color: #34d399;">{spike_cnt}</div>
                <div class="kpi-subtext">High demand / promo peaks</div>
            </div>
            """, unsafe_allow_html=True)
        with acol3:
            drop_cnt = (anomalies['Anomaly_Type'] == 'Drop').sum()
            st.markdown(f"""
            <div class="kpi-card" style="border-top: 4px solid #ef4444;">
                <div class="kpi-label">Sales Drops</div>
                <div class="kpi-value" style="color: #f87171;">{drop_cnt}</div>
                <div class="kpi-subtext">Potential stockouts / technical issues</div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Daily Sales Trend with Statistical Anomaly Bounds")
        fig, ax = plt.subplots(figsize=(10, 4.8), dpi=100)
        apply_chart_style(ax, fig)

        ax.plot(daily_sales['Date'], daily_sales['Sales'], color='#38bdf8', linewidth=1.8, label='Daily Actual Sales', alpha=0.9)
        ax.plot(daily_sales['Date'], daily_sales['Rolling_Mean'], color='#818cf8', linestyle='--', linewidth=1.5, label='7-Day Rolling Baseline')
        ax.fill_between(daily_sales['Date'], daily_sales['Lower_Bound'], daily_sales['Upper_Bound'], color='#6366f1', alpha=0.12, label='Expected Statistical Range (±2σ)')

        spikes = daily_sales[daily_sales['Anomaly_Type'] == 'Spike']
        if not spikes.empty:
            ax.scatter(spikes['Date'], spikes['Sales'], color='#10b981', s=80, marker='^', zorder=5, label='Positive Anomaly (Spike)')

        drops = daily_sales[daily_sales['Anomaly_Type'] == 'Drop']
        if not drops.empty:
            ax.scatter(drops['Date'], drops['Sales'], color='#ef4444', s=80, marker='v', zorder=5, label='Negative Anomaly (Drop)')

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        plt.xticks(rotation=25, ha='right')
        ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#cbd5e1', loc='upper left')
        ax.set_title("Statistical Outlier & Anomaly Surveillance", fontsize=11, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.subheader("Detected Anomalies Detailed Log")
        if anomalies.empty:
            st.info("No statistically significant sales spikes or drops detected in this date window.")
        else:
            anomalies['Date_Str'] = anomalies['Date'].dt.strftime('%Y-%m-%d')
            anomalies['Expected_Range'] = anomalies.apply(lambda r: f"${r['Lower_Bound']:,.0f} – ${r['Upper_Bound']:,.0f}", axis=1)
            anomalies['Deviation'] = ((anomalies['Sales'] - anomalies['Rolling_Mean']) / anomalies['Rolling_Mean'] * 100).round(1)
            
            def explain_anomaly(r):
                if r['Anomaly_Type'] == 'Spike':
                    return f"Sales surged +{r['Deviation']:.1f}% above expected normal range. Likely attributable to marketing campaign, seasonal spike, or bulk purchase."
                else:
                    return f"Sales plunged {r['Deviation']:.1f}% below normal corridor. Investigate inventory stockouts, website downtime, or checkout payment failures."
            
            anomalies['Business_Diagnosis'] = anomalies.apply(explain_anomaly, axis=1)
            st.dataframe(
                anomalies[['Date_Str', 'Sales', 'Expected_Range', 'Deviation', 'Anomaly_Type', 'Business_Diagnosis']].rename(columns={
                    'Date_Str': 'Date',
                    'Sales': 'Actual Sales ($)',
                    'Deviation': 'Deviation (%)',
                    'Anomaly_Type': 'Type'
                }).style.format({
                    'Actual Sales ($)': '${:,.2f}',
                    'Deviation (%)': '{:+.1f}%'
                }),
                use_container_width=True
            )


def render_sales_forecast(filtered_df):
    st.markdown('<div class="section-header">🔮 Sales Forecasting & Projections</div>', unsafe_allow_html=True)
    st.caption("Indicative moving-average forecasting for short-term retail demand planning.")

    monthly_sales = filtered_df.set_index('Date').resample('ME')['Sales'].sum().reset_index()
    monthly_sales = monthly_sales.sort_values('Date').reset_index(drop=True)

    if len(monthly_sales) < 3:
        st.warning(f"⚠️ Insufficient historical data: Found only {len(monthly_sales)} distinct month(s). A minimum of 3 consecutive months is required to compute indicative moving-average projections.")
    else:
        window = min(3, len(monthly_sales))
        weights = np.arange(1, window + 1)
        w_sum = weights.sum()

        forecast_periods = 3
        last_date = monthly_sales['Date'].iloc[-1]
        
        hist_values = monthly_sales['Sales'].tolist()
        forecast_dates = []
        forecast_values = []
        
        curr_hist = hist_values.copy()
        for i in range(1, forecast_periods + 1):
            next_date = last_date + pd.DateOffset(months=i)
            sub_window = curr_hist[-window:]
            w_avg = sum(val * w for val, w in zip(sub_window, weights)) / w_sum
            
            if len(sub_window) >= 2:
                momentum = (sub_window[-1] - sub_window[0]) / len(sub_window) * 0.5
            else:
                momentum = 0
            
            proj = max(0, w_avg + momentum)
            forecast_dates.append(next_date)
            forecast_values.append(round(proj, 2))
            curr_hist.append(proj)

        st.subheader("Historical vs Projected Sales (3-Month Outlook)")
        fig, ax = plt.subplots(figsize=(10, 4.8), dpi=100)
        apply_chart_style(ax, fig)

        hist_x = [d.strftime('%b %Y') for d in monthly_sales['Date']]
        ax.plot(hist_x, monthly_sales['Sales'], marker='o', linewidth=2.5, color='#38bdf8', label='Historical Actuals')

        conn_x = [hist_x[-1]] + [d.strftime('%b %Y') for d in forecast_dates]
        conn_y = [monthly_sales['Sales'].iloc[-1]] + forecast_values
        
        ax.plot(conn_x, conn_y, marker='D', markersize=6, linestyle='--', linewidth=2.2, color='#f59e0b', label='Projected Forecast (Indicative)')
        
        upper_f = [val * 1.10 for val in conn_y]
        lower_f = [val * 0.90 for val in conn_y]
        ax.fill_between(conn_x, lower_f, upper_f, color='#f59e0b', alpha=0.12, label='Indicative Range (±10%)')

        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        plt.xticks(rotation=25, ha='right')
        ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#cbd5e1', loc='upper left')
        ax.set_title("Retail Sales Forecast Projection", fontsize=11, fontweight='bold', pad=12)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.subheader("Projected Revenue Schedule")
        fcol1, fcol2, fcol3 = st.columns(3)
        cols = [fcol1, fcol2, fcol3]
        for idx, (f_date, f_val) in enumerate(zip(forecast_dates, forecast_values)):
            with cols[idx]:
                st.markdown(f"""
                <div class="kpi-card" style="border-top: 4px solid #f59e0b;">
                    <div class="kpi-label">{f_date.strftime('%B %Y')}</div>
                    <div class="kpi-value" style="color: #fbbf24;">${f_val:,.2f}</div>
                    <div class="kpi-subtext">Estimated Projection</div>
                </div>
                """, unsafe_allow_html=True)

        st.info("ℹ️ **Methodology Note:** Forecasts are calculated using a 3-month weighted moving average with recent momentum adjustment. Projections are indicative estimates intended for directional guidance, assuming baseline macroeconomic and market conditions persist.")


def render_what_if_simulator(filtered_df):
    st.markdown('<div class="section-header">🎛️ What-If Profit Simulator</div>', unsafe_allow_html=True)
    st.caption("Simulate how retail price adjustments, supplier cost inflation, and promotional discount strategies impact bottom-line profit.")

    products_list = sorted(filtered_df['Product'].unique().tolist())
    selected_prod = st.selectbox("Select Target Product for Simulation:", products_list)

    prod_records = filtered_df[filtered_df['Product'] == selected_prod]
    base_qty = int(prod_records['Quantity'].sum())
    base_unit_price = float(prod_records['Unit Price'].mean())
    base_unit_cost = float(prod_records['Unit Cost'].mean())
    base_sales = float(prod_records['Sales'].sum())
    base_profit = float(prod_records['Profit'].sum())
    base_margin = (base_profit / base_sales * 100) if base_sales > 0 else 0.0
    base_avg_disc_pct = float((prod_records['Discount'].sum() / (base_qty * base_unit_price) * 100)) if (base_qty * base_unit_price) > 0 else 0.0

    st.markdown("---")
    sim_col1, sim_col2 = st.columns([1, 1.2])

    with sim_col1:
        st.subheader("Interactive Strategy Levers")
        price_adj = st.slider("1. Selling Price Adjustment (%)", -30, 50, 5, 1, help="Simulate increasing or decreasing retail list price.")
        cost_adj = st.slider("2. Supplier Unit Cost Adjustment (%)", -30, 50, 0, 1, help="Simulate cost inflation or supplier bulk renegotiation savings.")
        disc_val = st.slider("3. Promotional Discount Rate (%)", 0, 50, int(round(base_avg_disc_pct)), 1, help="Adjust promotional discount percentage.")
        st.caption("Assumption: Sales volume remains constant at baseline units sold (price elasticity = 0).")

    sim_unit_price = base_unit_price * (1 + price_adj / 100.0)
    sim_unit_cost = base_unit_cost * (1 + cost_adj / 100.0)
    sim_gross_rev = base_qty * sim_unit_price
    sim_discount = sim_gross_rev * (disc_val / 100.0)
    sim_sales = sim_gross_rev - sim_discount
    sim_total_cost = base_qty * sim_unit_cost
    sim_profit = sim_sales - sim_total_cost
    sim_margin = (sim_profit / sim_sales * 100) if sim_sales > 0 else 0.0

    profit_diff = sim_profit - base_profit
    profit_pct_change = ((sim_profit - base_profit) / abs(base_profit) * 100) if abs(base_profit) > 0 else 0.0

    with sim_col2:
        st.subheader("Side-by-Side Financial Impact")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.metric(label="Simulated Revenue", value=f"${sim_sales:,.2f}", delta=f"${sim_sales - base_sales:+,.2f}")
        with sc2:
            st.metric(label="Simulated Profit", value=f"${sim_profit:,.2f}", delta=f"${profit_diff:+,.2f} ({profit_pct_change:+.1f}%)")
        with sc3:
            st.metric(label="Profit Margin", value=f"{sim_margin:.1f}%", delta=f"{sim_margin - base_margin:+.1f}%")

        fig, ax = plt.subplots(figsize=(7, 3.6), dpi=100)
        apply_chart_style(ax, fig)
        
        metrics = ['Revenue', 'Total Cost', 'Net Profit']
        baseline_vals = [base_sales, base_qty * base_unit_cost, base_profit]
        sim_vals = [sim_sales, sim_total_cost, sim_profit]
        
        x = np.arange(len(metrics))
        w = 0.32
        ax.bar(x - w/2, baseline_vals, w, label='Current Baseline', color='#64748b')
        ax.bar(x + w/2, sim_vals, w, label='Simulated Scenario', color='#38bdf8')
        
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
        ax.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='#cbd5e1')
        ax.set_title(f"Baseline vs Simulated Comparison: {selected_prod}", fontsize=10, fontweight='bold', pad=10)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.markdown('<div class="section-header">💬 Dynamic Strategic Assessment</div>', unsafe_allow_html=True)
    narrative_tone = "beneficial" if profit_diff >= 0 else "detrimental"
    direction_word = "increases" if profit_diff >= 0 else "decreases"
    
    st.markdown(f"""
    <div class="insight-card">
        <strong>Strategic Summary for {selected_prod}:</strong><br>
        Under this scenario (Selling Price <strong>{price_adj:+d}%</strong>, Supplier Cost <strong>{cost_adj:+d}%</strong>, Discount <strong>{disc_val}%</strong>),
        projected profit <strong>{direction_word} by ${abs(profit_diff):,.2f}</strong> ({profit_pct_change:+.1f}%), moving from <strong>${base_profit:,.2f}</strong> to <strong>${sim_profit:,.2f}</strong>.
        The operating profit margin shifts from <strong>{base_margin:.1f}%</strong> to <strong>{sim_margin:.1f}%</strong>.
        This represents a <strong>{narrative_tone}</strong> pricing optimization path.
    </div>
    """, unsafe_allow_html=True)


def render_export_reports(filtered_df, total_revenue, total_profit, total_orders, total_units, avg_order_value, profit_margin, top_prod, top_cat, top_reg):
    st.markdown('<div class="section-header">📑 Executive Reports & Data Export Center</div>', unsafe_allow_html=True)
    st.caption("Export filtered sales records, product profitability audits, and executive summaries.")

    rcol1, rcol2, rcol3 = st.columns(3)
    with rcol1:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #3b82f6;">
            <div class="kpi-label">Filtered Dataset</div>
            <div class="kpi-value">Sales CSV</div>
            <div class="kpi-subtext">All active filtered records</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        csv_filtered = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered CSV",
            data=csv_filtered,
            file_name=f"retailiq_filtered_sales_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with rcol2:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #10b981;">
            <div class="kpi-label">SKU Audit Report</div>
            <div class="kpi-value">Profitability CSV</div>
            <div class="kpi-subtext">Margin & cost audit by product</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        prod_rep = filtered_df.groupby('Product').agg(
            Category=('Category', 'first'),
            Units_Sold=('Quantity', 'sum'),
            Total_Revenue=('Sales', 'sum'),
            Total_Profit=('Profit', 'sum'),
            Avg_Discount=('Discount', 'mean')
        ).reset_index()
        prod_rep['Margin_Pct'] = (prod_rep['Total_Profit'] / prod_rep['Total_Revenue'] * 100).round(2)
        
        csv_prod = prod_rep.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Profitability Audit",
            data=csv_prod,
            file_name=f"retailiq_product_profitability_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with rcol3:
        st.markdown("""
        <div class="kpi-card" style="border-top: 4px solid #f59e0b;">
            <div class="kpi-label">Executive Briefing</div>
            <div class="kpi-value">Summary Report</div>
            <div class="kpi-subtext">Key business performance narrative</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        summary_text = f"""================================================================================
RETAILIQ EXECUTIVE SALES & PROFIT INTELLIGENCE REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Date Window Analyzed: {filtered_df['Date'].min().strftime('%Y-%m-%d')} to {filtered_df['Date'].max().strftime('%Y-%m-%d')}
================================================================================

1. CORE FINANCIAL HIGHLIGHTS
--------------------------------------------------------------------------------
- Total Gross Revenue:        ${total_revenue:,.2f}
- Total Net Profit:          ${total_profit:,.2f}
- Net Operating Margin:       {profit_margin:.2f}%
- Total Orders Processed:     {total_orders:,}
- Total Units Shipped:        {total_units:,}
- Average Order Value (AOV):  ${avg_order_value:,.2f}

2. TOP PERFORMERS
--------------------------------------------------------------------------------
- Top Selling SKU:            {top_prod}
- Most Profitable Category:   {top_cat}
- Leading Geographic Region:  {top_reg}

3. CATEGORY PERFORMANCE BREAKDOWN
--------------------------------------------------------------------------------
"""
        cat_breakdown = filtered_df.groupby('Category').agg(
            Revenue=('Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Transactions=('Sales', 'count')
        ).reset_index()
        cat_breakdown['Margin'] = (cat_breakdown['Profit'] / cat_breakdown['Revenue'] * 100).round(1)

        for _, r in cat_breakdown.iterrows():
            summary_text += f"• {r['Category']:<22} | Revenue: ${r['Revenue']:>10,.2f} | Profit: ${r['Profit']:>9,.2f} | Margin: {r['Margin']:>5.1f}%\n"

        summary_text += f"""
================================================================================
Confidential Retail Intelligence - Generated by RetailIQ
================================================================================
"""
        st.download_button(
            label="📥 Download Executive Briefing (TXT)",
            data=summary_text.encode('utf-8'),
            file_name=f"retailiq_executive_briefing_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.subheader("Executive Report Preview")
    st.code(summary_text, language="text")


if __name__ == "__main__":
    main()
