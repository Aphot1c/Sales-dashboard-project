"""
Minimalist Data Visualization Engine
Generates clean, mostly white Plotly charts with dynamic currency formatting.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def apply_clean_theme(fig: go.Figure, title: str = "") -> go.Figure:
    """Applies modern minimalist white theme."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>" if title else "",
            "font": {"size": 14, "color": "#0F172A", "family": "Plus Jakarta Sans, sans-serif"},
            "x": 0.0,
            "xanchor": "left"
        },
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            font_color="#FFFFFF"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11, color="#475569")
        ),
        margin=dict(l=20, r=20, t=40, b=30),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", linecolor="#E2E8F0"),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", linecolor="#E2E8F0")
    )
    return fig

def plot_sales_trend(df: pd.DataFrame, currency: str = "$") -> go.Figure:
    """Daily/Monthly Net Sales Trend Line."""
    if df.empty:
        return None

    # Group by date
    daily = df.groupby(df["Order_Date"].dt.date).agg(
        Net_Sales=("Net_Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "count")
    ).reset_index()
    daily.sort_values(by="Order_Date", inplace=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=daily["Order_Date"],
        y=daily["Net_Sales"],
        name="Sales",
        marker_color="#2563EB",
        opacity=0.85,
        hovertemplate=f"<b>%{{x}}</b><br>Sales: {currency}%{{y:,.2f}}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=daily["Order_Date"],
        y=daily["Profit"],
        name="Profit",
        mode="lines+markers",
        line=dict(color="#10B981", width=2.5),
        marker=dict(size=6, color="#059669"),
        hovertemplate=f"<b>%{{x}}</b><br>Profit: {currency}%{{y:,.2f}}<extra></extra>"
    ))

    fig.update_layout(
        yaxis=dict(title=f"Amount ({currency})", showgrid=True, gridcolor="#F1F5F9"),
        xaxis=dict(title="Order Date", showgrid=False)
    )

    return apply_clean_theme(fig, "Revenue & Profit Over Time")

def plot_category_distribution(df: pd.DataFrame, currency: str = "$") -> go.Figure:
    """Donut chart for Category sales share."""
    if df.empty or "Category" not in df.columns:
        return None

    cat_df = df.groupby("Category")["Net_Sales"].sum().reset_index()
    if cat_df["Net_Sales"].sum() == 0:
        return None

    fig = px.pie(
        cat_df,
        names="Category",
        values="Net_Sales",
        hole=0.6,
        color_discrete_sequence=["#2563EB", "#0D9488", "#F59E0B", "#8B5CF6"]
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=f"<b>%{{label}}</b><br>Sales: {currency}%{{value:,.2f}}<br>Share: %{{percent}}<extra></extra>"
    )
    return apply_clean_theme(fig, "Sales by Category")

def plot_payment_breakdown(df: pd.DataFrame, currency: str = "$") -> go.Figure:
    """Horizontal bar chart for Payment Methods."""
    if df.empty or "Payment_Method" not in df.columns:
        return None

    pay_df = df.groupby("Payment_Method")["Net_Sales"].sum().reset_index()
    pay_df.sort_values(by="Net_Sales", ascending=True, inplace=True)

    fig = px.bar(
        pay_df,
        x="Net_Sales",
        y="Payment_Method",
        orientation="h",
        color_discrete_sequence=["#2563EB"],
        labels={"Net_Sales": f"Sales ({currency})", "Payment_Method": "Payment Channel"}
    )
    fig.update_traces(hovertemplate=f"<b>%{{y}}</b>: {currency}%{{x:,.2f}}<extra></extra>")
    return apply_clean_theme(fig, "Sales by Payment Method")
