"""
Enterprise Sales Dataset Generator
Generates realistic multi-year sales transactions for business analytics and machine learning forecasting.
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_sales_data(num_records: int = 2500, output_path: str = "data/enterprise_sales.csv") -> pd.DataFrame:
    random.seed(42)
    np.random.seed(42)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Categories and Sub-categories with baseline pricing and margin profiles
    catalog = {
        "Technology": {
            "Laptops & Desktops": (600, 2200, 0.18, 0.28),
            "Smartphones & Tablets": (300, 1100, 0.15, 0.25),
            "Audio & Accessories": (30, 200, 0.25, 0.45),
            "Printers & Scanners": (150, 600, 0.12, 0.22)
        },
        "Furniture": {
            "Office Chairs": (80, 450, 0.15, 0.30),
            "Executive Desks": (200, 950, 0.10, 0.25),
            "Bookcases & Shelving": (90, 400, 0.12, 0.24),
            "Conference Tables": (350, 1500, 0.10, 0.20)
        },
        "Office Supplies": {
            "Paper & Envelopes": (8, 45, 0.30, 0.50),
            "Binders & Organizers": (5, 35, 0.35, 0.55),
            "Writing Instruments": (4, 25, 0.30, 0.50),
            "Storage Solutions": (25, 120, 0.20, 0.35)
        }
    }

    regions_data = {
        "North": ["New Delhi", "Chandigarh", "Jaipur", "Lucknow", "Dehradun"],
        "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore"],
        "East": ["Kolkata", "Bhubaneswar", "Patna", "Ranchi", "Guwahati"],
        "West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Goa"],
        "Central": ["Bhopal", "Indore", "Nagpur", "Raipur", "Jabalpur"]
    }

    customer_segments = ["Consumer", "Corporate", "Home Office"]
    ship_modes = ["Standard Delivery", "Express Air", "Same Day Priority", "Freight Saver"]
    payment_methods = ["UPI / QR", "Credit Card", "Net Banking", "Corporate Purchase Order", "Cash on Delivery"]
    order_statuses = ["Delivered", "Delivered", "Delivered", "Delivered", "Shipped", "Processing", "Returned"]

    # Generate customer pool for realistic repeat-order dynamics
    customer_pool = []
    first_names = ["Aarav", "Priya", "Rahul", "Ananya", "Rohan", "Sneha", "Vikram", "Neha", "Aditya", "Pooja",
                   "Arjun", "Kavita", "Siddharth", "Meera", "Karan", "Tanvi", "Amit", "Isha", "Naveen", "Divya",
                   "Rajesh", "Swati", "Manish", "Sunita", "Deepak", "Ritu", "Alok", "Shweta", "Sanjay", "Preeti"]
    last_names = ["Sharma", "Verma", "Patel", "Mehta", "Reddy", "Nair", "Gupta", "Singh", "Iyer", "Chopra",
                  "Joshi", "Bose", "Kulkarni", "Deshmukh", "Kapoor", "Malhotra", "Saxena", "Choudhury", "Menon", "Rao"]

    for i in range(1, 151):
        c_id = f"CUST-{1000 + i}"
        c_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        c_segment = random.choice(customer_segments)
        customer_pool.append((c_id, c_name, c_segment))

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 9, 30)
    total_days = (end_date - start_date).days

    rows = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{2023 + (i % 4)}-{10000 + i}"

        # Seasonal distribution (Q4 spike for festive & year-end purchases)
        day_offset = random.randint(0, total_days)
        order_date = start_date + timedelta(days=day_offset)

        # Ship date between 1 to 5 days after order date
        ship_delay = random.choices([1, 2, 3, 4, 5, 7], weights=[0.25, 0.35, 0.20, 0.10, 0.07, 0.03])[0]
        ship_date = order_date + timedelta(days=ship_delay)

        # Pick customer
        cust = random.choice(customer_pool)
        customer_id, customer_name, customer_segment = cust

        # Geographic routing
        region = random.choice(list(regions_data.keys()))
        city = random.choice(regions_data[region])

        # Product selection
        category = random.choices(["Technology", "Furniture", "Office Supplies"], weights=[0.40, 0.32, 0.28])[0]
        sub_category = random.choice(list(catalog[category].keys()))
        min_p, max_p, min_m, max_m = catalog[category][sub_category]

        unit_price = round(random.uniform(min_p, max_p), 2)
        quantity = random.choices([1, 2, 3, 4, 5, 8, 10], weights=[0.45, 0.25, 0.15, 0.08, 0.04, 0.02, 0.01])[0]

        # Discounts (0%, 5%, 10%, 15%, 20%, 25%)
        discount_rate = random.choices([0.0, 0.05, 0.10, 0.15, 0.20, 0.25], weights=[0.40, 0.20, 0.18, 0.12, 0.07, 0.03])[0]

        gross_sales = unit_price * quantity
        discount_amount = round(gross_sales * discount_rate, 2)
        net_sales = round(gross_sales - discount_amount, 2)

        # Profit calculation with cost and margin erosion from heavy discounts
        cost_price = unit_price * (1.0 - random.uniform(min_m, max_m))
        total_cost = round(cost_price * quantity, 2)
        profit = round(net_sales - total_cost, 2)
        profit_margin = round((profit / net_sales) * 100, 2) if net_sales > 0 else 0.0

        ship_mode = random.choice(ship_modes)
        payment_method = random.choice(payment_methods)
        order_status = random.choice(order_statuses)

        # If returned, adjust profit
        if order_status == "Returned":
            profit = round(-total_cost * 0.15, 2) # Restocking loss
            net_sales = 0.0

        rows.append({
            "Order_ID": order_id,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Ship_Date": ship_date.strftime("%Y-%m-%d"),
            "Customer_ID": customer_id,
            "Customer_Name": customer_name,
            "Customer_Segment": customer_segment,
            "Region": region,
            "City": city,
            "Category": category,
            "Sub_Category": sub_category,
            "Unit_Price": unit_price,
            "Quantity": quantity,
            "Gross_Sales": gross_sales,
            "Discount_Rate": discount_rate,
            "Discount_Amount": discount_amount,
            "Net_Sales": net_sales,
            "Cost": total_cost,
            "Profit": profit,
            "Profit_Margin_Pct": profit_margin,
            "Ship_Mode": ship_mode,
            "Payment_Method": payment_method,
            "Order_Status": order_status
        })

    df = pd.DataFrame(rows)
    df.sort_values(by="Order_Date", inplace=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} sales records successfully at {output_path}")
    return df

if __name__ == "__main__":
    generate_sales_data()
