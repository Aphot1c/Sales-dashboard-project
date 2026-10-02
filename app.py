"""
Sales Dashboard
Professional, modern, responsive sales analytics application.
"""

from datetime import datetime
import importlib
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Defensive module reload to prevent stale cached imports in Streamlit server
import config
importlib.reload(config)

from config import CUSTOM_CSS, CURRENCY_SYMBOLS

# Safe fallback for SVG icons
SVG_ICONS = getattr(config, "SVG_ICONS", {
    "wallet": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></svg>""",
    "trending": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>""",
    "percent": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>""",
    "package": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>"""
})

from utils.analytics import (
    load_data,
    calculate_kpis,
    add_order_record,
    reset_database,
    load_sample_orders
)
from utils.visualizations import (
    plot_sales_trend,
    plot_category_distribution,
    plot_payment_breakdown
)

# Apply modern styling
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------------------------------------------
# Sidebar: Settings & Database Management
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    currency_label = st.selectbox(
        "Currency",
        list(CURRENCY_SYMBOLS.keys()),
        index=0  # Default: INR (₹)
    )
    curr = CURRENCY_SYMBOLS[currency_label]

    st.write("")
    st.markdown("### 🗄️ Database Actions")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🗑️ Reset", help="Clear all orders back to 0", width="stretch"):
            reset_database()
            st.success("Cleared!")
            st.rerun()
    with col_btn2:
        if st.button("📦 Demo", help="Load 5 realistic sample orders", width="stretch"):
            load_sample_orders()
            st.success("Loaded!")
            st.rerun()

    st.write("")
    df_count = load_data()
    st.markdown(f"<span style='font-size: 0.85rem; color: #64748B;'>Total Orders in DB: <b>{len(df_count):,}</b></span>", unsafe_allow_html=True)

# -------------------------------------------------------------
# Main Header
# -------------------------------------------------------------
st.markdown("<h1>Sales Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-heading'>Real-time revenue monitoring, customer orders, and performance insights.</div>", unsafe_allow_html=True)

df = load_data()
kpis = calculate_kpis(df)

# -------------------------------------------------------------
# Responsive Modern Metric Cards with Vector SVG Icons
# -------------------------------------------------------------
metric_tiles_html = f"""
<div class="metric-grid">
    <div class="metric-card-pro">
        <div class="card-top">
            <span class="card-title">Total Revenue</span>
            <div class="icon-badge">{SVG_ICONS['wallet']}</div>
        </div>
        <div class="card-val">{curr}{kpis['total_sales']:,.2f}</div>
        <div class="card-note">Net amount after discounts</div>
    </div>
    <div class="metric-card-pro">
        <div class="card-top">
            <span class="card-title">Total Profit</span>
            <div class="icon-badge">{SVG_ICONS['trending']}</div>
        </div>
        <div class="card-val">{curr}{kpis['total_profit']:,.2f}</div>
        <div class="card-note">Revenue minus cost of goods</div>
    </div>
    <div class="metric-card-pro">
        <div class="card-top">
            <span class="card-title">Profit Margin</span>
            <div class="icon-badge">{SVG_ICONS['percent']}</div>
        </div>
        <div class="card-val">{kpis['profit_margin']:.1f}%</div>
        <div class="card-note">Overall operating margin</div>
    </div>
    <div class="metric-card-pro">
        <div class="card-top">
            <span class="card-title">Total Orders</span>
            <div class="icon-badge">{SVG_ICONS['package']}</div>
        </div>
        <div class="card-val">{kpis['total_orders']:,}</div>
        <div class="card-note">Transactions in system</div>
    </div>
</div>
"""
st.markdown(metric_tiles_html, unsafe_allow_html=True)

# -------------------------------------------------------------
# Segmented Navigation Tabs
# -------------------------------------------------------------
tab_charts, tab_add, tab_list = st.tabs([
    "📊 Analytics",
    "➕ Add Order",
    "📋 Orders List"
])

# -------------------------------------------------------------
# TAB 1: ANALYTICS & CHARTS
# -------------------------------------------------------------
with tab_charts:
    if df.empty:
        st.info("ℹ️ Your database is currently empty. Go to the **'➕ Add Order'** tab to record your first transaction, or click **'Demo'** in the sidebar to load starter orders.")
    else:
        col_c1, col_c2 = st.columns([1.5, 1.1])
        
        with col_c1:
            trend_fig = plot_sales_trend(df, currency=curr)
            if trend_fig:
                st.plotly_chart(trend_fig, width="stretch")
        
        with col_c2:
            cat_fig = plot_category_distribution(df, currency=curr)
            if cat_fig:
                st.plotly_chart(cat_fig, width="stretch")

        st.write("")
        pay_fig = plot_payment_breakdown(df, currency=curr)
        if pay_fig:
            st.plotly_chart(pay_fig, width="stretch")

# -------------------------------------------------------------
# TAB 2: ADD ORDER (Clean, Aligned, Reactive)
# -------------------------------------------------------------
with tab_add:
    st.markdown("### Record New Customer Order")
    st.markdown("<p style='color: #64748B; font-size: 0.875rem;'>Fill in customer information and pricing. Values calculate live on screen.</p>", unsafe_allow_html=True)

    # 1. Customer Details
    st.markdown("<span style='font-size: 0.875rem; font-weight: 700; color: #0F172A;'>1. Customer Details</span>", unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        cust_name = st.text_input("Customer Name", placeholder="e.g. Rahul Sharma", key="in_name")
    with c_col2:
        cust_city = st.text_input("City / Location", placeholder="e.g. Mumbai, New Delhi, Bengaluru", key="in_city")

    # 2. Product & Rates
    st.write("")
    st.markdown("<span style='font-size: 0.875rem; font-weight: 700; color: #0F172A;'>2. Product & Pricing</span>", unsafe_allow_html=True)
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        category_choice = st.selectbox(
            "Category",
            ["Technology", "Furniture", "Office Supplies", "Electronics", "Accessories"],
            key="in_cat"
        )
    with p_col2:
        product_item = st.text_input("Product Name", placeholder="e.g. Wireless Mouse, Standing Desk, Ergonomic Chair", key="in_prod")

    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        rate_val = st.number_input(f"Rate / Unit Price ({curr})", min_value=1.0, max_value=5000000.0, value=500.0, step=50.0, key="in_rate")
    with r_col2:
        qty_val = st.number_input("Quantity", min_value=1, max_value=1000, value=1, step=1, key="in_qty")
    with r_col3:
        discount_val = st.number_input("Discount (%)", min_value=0.0, max_value=90.0, value=0.0, step=1.0, key="in_disc")

    # 3. Payment Method & Status
    st.write("")
    st.markdown("<span style='font-size: 0.875rem; font-weight: 700; color: #0F172A;'>3. Payment & Fulfillment</span>", unsafe_allow_html=True)
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        pay_choice = st.selectbox("Payment Method", ["UPI / QR", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"], key="in_pay")
    with m_col2:
        status_choice = st.selectbox("Order Status", ["Delivered", "Shipped", "Processing"], key="in_status")

    # Real-Time Calculations Preview
    gross_amount = rate_val * qty_val
    discount_amount = gross_amount * (discount_val / 100.0)
    net_total = gross_amount - discount_amount
    est_cost = rate_val * 0.65 * qty_val
    est_profit = net_total - est_cost

    summary_html = f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px 18px; margin: 20px 0; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
        <span style="font-weight: 700; color: #0F172A; font-size: 0.9rem;">⚡ Order Calculation Summary:</span><br>
        <span style="color: #475569; font-size: 0.875rem;">
            Gross: <b>{curr}{gross_amount:,.2f}</b> &nbsp;|&nbsp; 
            Discount: <b>{curr}{discount_amount:,.2f}</b> ({discount_val:.0f}%) &nbsp;|&nbsp; 
            <b>Final Net Total: <span style="color: #2563EB;">{curr}{net_total:,.2f}</span></b> &nbsp;|&nbsp; 
            Estimated Profit: <span style="color: #059669; font-weight: 600;">{curr}{est_profit:,.2f}</span>
        </span>
    </div>
    """
    st.markdown(summary_html, unsafe_allow_html=True)

    # Save Button
    if st.button("💾 Save Order", type="primary"):
        if not cust_name.strip():
            st.error("Please enter a valid Customer Name.")
        elif not product_item.strip():
            st.error("Please enter a valid Product Name.")
        else:
            city_final = cust_city.strip() if cust_city.strip() else "Direct"
            saved = add_order_record(
                customer_name=cust_name.strip(),
                city=city_final,
                category=category_choice,
                product_name=product_item.strip(),
                unit_price=float(rate_val),
                quantity=int(qty_val),
                discount_pct=float(discount_val),
                payment_method=pay_choice,
                order_status=status_choice
            )
            st.success(f"✅ Order #{saved['Order_ID']} saved successfully! Total: {curr}{saved['Net_Sales']:,.2f}")
            st.rerun()

# -------------------------------------------------------------
# TAB 3: ORDERS LIST & EXPORT
# -------------------------------------------------------------
with tab_list:
    st.markdown("### All Orders")
    
    if df.empty:
        st.info("No orders in database yet. Add an order in the '➕ Add Order' tab.")
    else:
        # Search Box
        search_term = st.text_input("🔎 Search orders:", placeholder="Filter by customer name, city, order ID, or product...")

        view_df = df.copy()
        if search_term.strip():
            kw = search_term.strip().lower()
            view_df = view_df[
                view_df["Order_ID"].astype(str).str.lower().str.contains(kw) |
                view_df["Customer_Name"].astype(str).str.lower().str.contains(kw) |
                view_df["City"].astype(str).str.lower().str.contains(kw) |
                view_df["Product_Name"].astype(str).str.lower().str.contains(kw)
            ]

        col_dl, col_cnt = st.columns([1, 3])
        with col_dl:
            csv_bytes = view_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export to CSV",
                data=csv_bytes,
                file_name=f"sales_orders_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        with col_cnt:
            st.caption(f"Showing **{len(view_df):,}** matching transactions")

        show_cols = [
            "Order_ID", "Order_Date", "Customer_Name", "City",
            "Category", "Product_Name", "Unit_Price", "Quantity",
            "Discount_Pct", "Net_Sales", "Profit", "Payment_Method", "Order_Status"
        ]

        display_df = view_df[show_cols].copy()
        display_df["Unit_Price"] = display_df["Unit_Price"].apply(lambda x: f"{curr}{x:,.2f}")
        display_df["Net_Sales"] = display_df["Net_Sales"].apply(lambda x: f"{curr}{x:,.2f}")
        display_df["Profit"] = display_df["Profit"].apply(lambda x: f"{curr}{x:,.2f}")
        display_df["Discount_Pct"] = display_df["Discount_Pct"].apply(lambda x: f"{x:.0f}%")

        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True
        )
