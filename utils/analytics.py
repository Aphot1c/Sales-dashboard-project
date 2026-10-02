"""
Core Business Logic & Analytics Engine
Handles data storage, validation, order calculations, database reset, and KPI aggregation.
"""

from datetime import datetime
import os
import pandas as pd
import numpy as np

DATA_PATH = "data/sales_data.csv"

COLUMNS = [
    "Order_ID", "Order_Date", "Customer_Name", "City", "Category",
    "Product_Name", "Unit_Price", "Quantity", "Discount_Pct",
    "Gross_Sales", "Discount_Amount", "Net_Sales", "Cost", "Profit",
    "Payment_Method", "Order_Status"
]

def init_database(filepath: str = DATA_PATH) -> None:
    """Ensures the data directory and sales CSV exist with proper headers."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath) or os.stat(filepath).st_size == 0:
        empty_df = pd.DataFrame(columns=COLUMNS)
        empty_df.to_csv(filepath, index=False)

def load_data(filepath: str = DATA_PATH) -> pd.DataFrame:
    """Loads transactions from CSV safely, handling empty states without errors."""
    init_database(filepath)
    try:
        df = pd.read_csv(filepath)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(filepath, index=False)

    # Ensure all required columns exist
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    if not df.empty:
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
        df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce").fillna(0.0)
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
        df["Discount_Pct"] = pd.to_numeric(df["Discount_Pct"], errors="coerce").fillna(0.0)
        df["Gross_Sales"] = pd.to_numeric(df["Gross_Sales"], errors="coerce").fillna(0.0)
        df["Discount_Amount"] = pd.to_numeric(df["Discount_Amount"], errors="coerce").fillna(0.0)
        df["Net_Sales"] = pd.to_numeric(df["Net_Sales"], errors="coerce").fillna(0.0)
        df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce").fillna(0.0)
        df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").fillna(0.0)
        
        # Date helper for charts
        df["Year_Month"] = df["Order_Date"].dt.strftime("%Y-%m")
        df.sort_values(by="Order_Date", ascending=False, inplace=True)
    else:
        df["Year_Month"] = pd.Series(dtype="str")

    return df

def calculate_kpis(df: pd.DataFrame) -> dict:
    """Computes headline metrics safely for both empty and populated states."""
    if df.empty:
        return {
            "total_sales": 0.0,
            "total_profit": 0.0,
            "profit_margin": 0.0,
            "total_orders": 0,
            "total_units": 0,
            "aov": 0.0
        }

    total_sales = float(df["Net_Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_orders = int(df["Order_ID"].nunique())
    total_units = int(df["Quantity"].sum())
    
    profit_margin = float((total_profit / total_sales * 100)) if total_sales > 0 else 0.0
    aov = float((total_sales / total_orders)) if total_orders > 0 else 0.0

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "total_orders": total_orders,
        "total_units": total_units,
        "aov": aov
    }

def add_order_record(
    customer_name: str,
    city: str,
    category: str,
    product_name: str,
    unit_price: float,
    quantity: int,
    discount_pct: float,
    payment_method: str,
    order_status: str = "Delivered",
    filepath: str = DATA_PATH
) -> dict:
    """Inserts a new order, calculates totals, and appends to the dataset."""
    df = load_data(filepath)
    next_id_num = 1001 if df.empty else len(df) + 1001
    order_id = f"ORD-{next_id_num}"
    order_date = datetime.now().strftime("%Y-%m-%d")

    unit_price = float(unit_price)
    quantity = int(quantity)
    discount_pct = float(discount_pct)

    gross_sales = round(unit_price * quantity, 2)
    discount_amount = round(gross_sales * (discount_pct / 100.0), 2)
    net_sales = round(gross_sales - discount_amount, 2)
    cost = round(unit_price * 0.65 * quantity, 2)
    profit = round(net_sales - cost, 2)

    new_row = {
        "Order_ID": order_id,
        "Order_Date": order_date,
        "Customer_Name": customer_name.strip(),
        "City": city.strip(),
        "Category": category.strip(),
        "Product_Name": product_name.strip(),
        "Unit_Price": unit_price,
        "Quantity": quantity,
        "Discount_Pct": discount_pct,
        "Gross_Sales": gross_sales,
        "Discount_Amount": discount_amount,
        "Net_Sales": net_sales,
        "Cost": cost,
        "Profit": profit,
        "Payment_Method": payment_method.strip(),
        "Order_Status": order_status.strip()
    }

    raw_df = pd.read_csv(filepath) if os.path.exists(filepath) and os.stat(filepath).st_size > 0 else pd.DataFrame(columns=COLUMNS)
    updated_df = pd.concat([raw_df, pd.DataFrame([new_row])], ignore_index=True)
    updated_df.to_csv(filepath, index=False)
    return new_row

def reset_database(filepath: str = DATA_PATH) -> None:
    """Resets the sales dataset to an empty state with zero orders."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    empty_df = pd.DataFrame(columns=COLUMNS)
    empty_df.to_csv(filepath, index=False)

def load_sample_orders(filepath: str = DATA_PATH) -> int:
    """Populates 5 starter orders for quick testing or demonstration."""
    sample_data = [
        ("Aarav Sharma", "Mumbai", "Technology", "MacBook Pro M3", 1999.0, 1, 5.0, "Credit Card"),
        ("Priya Verma", "Bengaluru", "Technology", "Wireless Headphones", 149.0, 2, 10.0, "UPI / QR"),
        ("Rahul Patel", "New Delhi", "Furniture", "Ergonomic Office Chair", 249.0, 2, 0.0, "Net Banking"),
        ("Ananya Mehta", "Pune", "Office Supplies", "Laser Printer Toner", 45.0, 4, 0.0, "Credit Card"),
        ("Rohan Gupta", "Hyderabad", "Furniture", "Standing Electric Desk", 499.0, 1, 8.0, "UPI / QR")
    ]
    reset_database(filepath)
    for cust, city, cat, prod, price, qty, disc, pay in sample_data:
        add_order_record(cust, city, cat, prod, price, qty, disc, pay, filepath=filepath)
    return len(sample_data)
