"""
Regression Test Suite for Sales Dashboard
Verifies data loading, empty states, math accuracy, reset, and visualizations.
"""

import os
import sys
import unittest
import pandas as pd

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

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

TEST_DB_PATH = "data/test_sales_data.csv"

class TestSalesDashboardRegression(unittest.TestCase):

    def setUp(self):
        """Reset test database before each test."""
        reset_database(filepath=TEST_DB_PATH)

    def tearDown(self):
        """Clean up test database after tests."""
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_01_empty_database_loading(self):
        """Ensure loading an empty database returns empty dataframe and zeroes KPIs."""
        df = load_data(filepath=TEST_DB_PATH)
        self.assertTrue(df.empty, "Dataframe should be empty.")
        self.assertEqual(len(df), 0, "Row count should be 0.")

        kpis = calculate_kpis(df)
        self.assertEqual(kpis["total_sales"], 0.0)
        self.assertEqual(kpis["total_profit"], 0.0)
        self.assertEqual(kpis["profit_margin"], 0.0)
        self.assertEqual(kpis["total_orders"], 0)
        self.assertEqual(kpis["aov"], 0.0)

    def test_02_visualizations_with_empty_data(self):
        """Ensure charts handle empty datasets gracefully without exceptions."""
        df = load_data(filepath=TEST_DB_PATH)
        self.assertIsNone(plot_sales_trend(df, currency="₹"))
        self.assertIsNone(plot_category_distribution(df, currency="₹"))
        self.assertIsNone(plot_payment_breakdown(df, currency="₹"))

    def test_03_add_single_order_calculations(self):
        """Verify mathematical precision of gross sales, discounts, net sales, and profit."""
        rec = add_order_record(
            customer_name="Test Customer",
            city="New Delhi",
            category="Technology",
            product_name="Wireless Mouse",
            unit_price=1000.0,
            quantity=3,
            discount_pct=10.0,
            payment_method="UPI / QR",
            order_status="Delivered",
            filepath=TEST_DB_PATH
        )

        expected_gross = 3000.0  # 1000 * 3
        expected_discount = 300.0  # 3000 * 0.10
        expected_net = 2700.0  # 3000 - 300
        expected_cost = 1950.0  # 1000 * 0.65 * 3
        expected_profit = 750.0  # 2700 - 1950

        self.assertEqual(rec["Gross_Sales"], expected_gross)
        self.assertEqual(rec["Discount_Amount"], expected_discount)
        self.assertEqual(rec["Net_Sales"], expected_net)
        self.assertEqual(rec["Cost"], expected_cost)
        self.assertEqual(rec["Profit"], expected_profit)

        # Check DB reflects row
        df = load_data(filepath=TEST_DB_PATH)
        self.assertEqual(len(df), 1)

        kpis = calculate_kpis(df)
        self.assertEqual(kpis["total_sales"], expected_net)
        self.assertEqual(kpis["total_profit"], expected_profit)
        self.assertEqual(kpis["total_orders"], 1)

    def test_04_multiple_orders_and_kpis(self):
        """Verify KPI aggregations across multiple diverse orders."""
        add_order_record("Cust 1", "Mumbai", "Technology", "Item 1", 500.0, 2, 0.0, "Credit Card", filepath=TEST_DB_PATH)
        add_order_record("Cust 2", "Pune", "Furniture", "Item 2", 200.0, 1, 10.0, "UPI / QR", filepath=TEST_DB_PATH)

        df = load_data(filepath=TEST_DB_PATH)
        self.assertEqual(len(df), 2)

        kpis = calculate_kpis(df)
        self.assertEqual(kpis["total_orders"], 2)
        # Order 1: 500*2 = 1000 net
        # Order 2: 200*1 - 20 disc = 180 net
        self.assertEqual(kpis["total_sales"], 1180.0)

    def test_05_database_reset(self):
        """Verify database reset completely clears records back to zero."""
        add_order_record("Cust 1", "City", "Category", "Item", 100.0, 1, 0.0, "COD", filepath=TEST_DB_PATH)
        df_before = load_data(filepath=TEST_DB_PATH)
        self.assertEqual(len(df_before), 1)

        reset_database(filepath=TEST_DB_PATH)
        df_after = load_data(filepath=TEST_DB_PATH)
        self.assertTrue(df_after.empty)
        self.assertEqual(len(df_after), 0)

    def test_06_load_sample_orders(self):
        """Verify loading sample orders populates 5 records."""
        count = load_sample_orders(filepath=TEST_DB_PATH)
        self.assertEqual(count, 5)
        df = load_data(filepath=TEST_DB_PATH)
        self.assertEqual(len(df), 5)
        kpis = calculate_kpis(df)
        self.assertGreater(kpis["total_sales"], 0.0)

    def test_07_visualizations_with_data(self):
        """Verify charts render correctly when records exist."""
        load_sample_orders(filepath=TEST_DB_PATH)
        df = load_data(filepath=TEST_DB_PATH)

        trend_fig = plot_sales_trend(df, currency="₹")
        self.assertIsNotNone(trend_fig)

        cat_fig = plot_category_distribution(df, currency="₹")
        self.assertIsNotNone(cat_fig)

        pay_fig = plot_payment_breakdown(df, currency="₹")
        self.assertIsNotNone(pay_fig)

if __name__ == "__main__":
    unittest.main()
