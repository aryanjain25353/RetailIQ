import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate realistic retail sales dataset
categories = {
    "Electronics": [
        ("Ultra HD Smart TV 55\"", 480.0, 420.0),    # High revenue, thin margin (~12.5% baseline, low after discount)
        ("Wireless Noise-Canceling Headphones", 120.0, 55.0), # Healthy margin (~54%)
        ("Bluetooth Portable Speaker", 65.0, 32.0), # Healthy margin (~50%)
        ("Fast USB-C Charging Hub", 25.0, 24.0),     # Problem item: low margin, prone to loss on discount
        ("Mechanical Gaming Keyboard", 95.0, 50.0),  # Good margin (~47%)
    ],
    "Apparel": [
        ("Premium Cotton Crewneck T-Shirt", 28.0, 10.0), # High margin (~64%)
        ("Slim-Fit Denim Jeans", 55.0, 24.0),           # Good margin (~56%)
        ("Thermal Winter Parka Jacket", 140.0, 75.0),   # Healthy margin (~46%)
        ("Breathable Athletic Running Shoes", 85.0, 48.0), # Good margin (~43%)
    ],
    "Home & Kitchen": [
        ("Ergonomic Mesh Office Chair", 195.0, 110.0), # Healthy margin (~43%)
        ("Stainless Steel Thermal Flask", 22.0, 8.0),   # High margin (~63%)
        ("Ceramic Artisan Coffee Mug", 14.0, 13.5),     # Profit leak product: cost nearly equals price
        ("Programmable Drip Coffee Maker", 78.0, 45.0), # Healthy margin (~42%)
    ],
    "Office Supplies": [
        ("Executive Hardcover Notebook", 16.0, 5.0),   # High margin (~68%)
        ("Gel Ink Rollerball Pens (Set of 10)", 12.0, 4.0), # High margin (~66%)
        ("Dual Monitor Desk Mount", 68.0, 38.0),       # Healthy margin (~44%)
    ],
    "Health & Personal Care": [
        ("Sonic Electric Toothbrush", 45.0, 20.0),     # Good margin (~55%)
        ("Smart Digital Body Scale", 38.0, 22.0),      # Moderate margin (~42%)
        ("Deep Tissue Massage Gun", 89.0, 50.0),       # Healthy margin (~43%)
    ]
}

regions = ["North", "South", "East", "West", "Central"]

# Generate dates over 8 months from Jan 1 2025 to Aug 31 2025 (243 days)
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 8, 31)
date_range_days = (end_date - start_date).days

records = []
order_id = 1001

# Create 160 realistic transactions
for i in range(160):
    # Select random date
    day_offset = np.random.randint(0, date_range_days + 1)
    trans_date = start_date + timedelta(days=int(day_offset))
    
    # Select category and product
    cat = np.random.choice(list(categories.keys()), p=[0.30, 0.25, 0.20, 0.15, 0.10])
    prod_info = categories[cat][np.random.randint(0, len(categories[cat]))]
    prod_name, base_price, base_cost = prod_info
    
    region = np.random.choice(regions, p=[0.28, 0.24, 0.18, 0.20, 0.10])
    
    # Quantities: mostly 1 to 5, occasionally larger for office supplies or mugs
    if cat in ["Office Supplies"]:
        quantity = np.random.choice([1, 2, 3, 5, 8, 10], p=[0.3, 0.25, 0.2, 0.15, 0.05, 0.05])
    elif prod_name == "Ultra HD Smart TV 55\"":
        quantity = np.random.choice([1, 2, 3], p=[0.8, 0.15, 0.05])
    else:
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.45, 0.30, 0.15, 0.07, 0.03])
        
    unit_price = round(base_price * np.random.uniform(0.95, 1.05), 2)
    unit_cost = round(base_cost * np.random.uniform(0.98, 1.02), 2)
    
    # Discount: normal discounts 0%, 5%, 10%, 15%. For special leak items, occasionally heavy discount
    if prod_name in ["Fast USB-C Charging Hub", "Ceramic Artisan Coffee Mug"]:
        discount_rate = np.random.choice([0.0, 0.10, 0.15, 0.25], p=[0.2, 0.3, 0.3, 0.2])
    elif prod_name == "Ultra HD Smart TV 55\"":
        discount_rate = np.random.choice([0.0, 0.05, 0.10, 0.15], p=[0.3, 0.3, 0.25, 0.15])
    else:
        discount_rate = np.random.choice([0.0, 0.05, 0.10, 0.15], p=[0.5, 0.3, 0.15, 0.05])
        
    gross_sales = quantity * unit_price
    discount = round(gross_sales * discount_rate, 2)
    sales = round(gross_sales - discount, 2)
    total_cost = round(quantity * unit_cost, 2)
    profit = round(sales - total_cost, 2)
    
    records.append({
        "Date": trans_date.strftime("%Y-%m-%d"),
        "Product": prod_name,
        "Category": cat,
        "Quantity": int(quantity),
        "Unit Price": unit_price,
        "Unit Cost": unit_cost,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
        "Region": region
    })

# Add deliberate specific anomalies for testing Anomaly Detector:
# 1. High spike on 2025-05-15 (Mega Flash Sale)
records.append({
    "Date": "2025-05-15",
    "Product": "Ultra HD Smart TV 55\"",
    "Category": "Electronics",
    "Quantity": 12,
    "Unit Price": 480.0,
    "Unit Cost": 415.0,
    "Discount": 300.0,
    "Sales": 5460.0,
    "Profit": 480.0,
    "Region": "North"
})
records.append({
    "Date": "2025-05-15",
    "Product": "Wireless Noise-Canceling Headphones",
    "Category": "Electronics",
    "Quantity": 15,
    "Unit Price": 120.0,
    "Unit Cost": 55.0,
    "Discount": 180.0,
    "Sales": 1620.0,
    "Profit": 795.0,
    "Region": "West"
})

# 2. Add an explicit loss-making clearance transaction
records.append({
    "Date": "2025-06-20",
    "Product": "Fast USB-C Charging Hub",
    "Category": "Electronics",
    "Quantity": 20,
    "Unit Price": 25.0,
    "Unit Cost": 24.5,
    "Discount": 125.0, # 25% discount on $500 -> sales $375, cost $490 -> profit -$115
    "Sales": 375.0,
    "Profit": -115.0,
    "Region": "Central"
})

df = pd.DataFrame(records)
# Sort by Date
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

csv_path = r"C:\Users\Aryan jain\.gemini\antigravity\scratch\RetailIQ\sample_sales.csv"
df.to_csv(csv_path, index=False)
print(f"Generated {len(df)} rows to {csv_path}")
print(df.head())
