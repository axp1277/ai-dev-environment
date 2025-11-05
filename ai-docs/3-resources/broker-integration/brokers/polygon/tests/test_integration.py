"""Simple integration tests for Polygon data fetcher."""
import os
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.brokers.polygon.core import (
    calculate_date_range,
    create_table,
    fetch_ohlcv,
    get_db_connection,
    insert_bars,
    map_timeframe_for_api,
    map_timeframe_for_table,
)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete data fetching pipeline."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.test_db.close()
        
        # Patch database connection
        self.db_patcher = patch("src.brokers.polygon.core.get_db_connection")
        mock_get_db = self.db_patcher.start()
        mock_get_db.return_value = sqlite3.connect(self.test_db.name)
        
        # Patch API key loading
        self.api_key_patcher = patch("src.brokers.polygon.core.load_api_key")
        mock_load_key = self.api_key_patcher.start()
        mock_load_key.return_value = "test_api_key"
    
    def tearDown(self):
        """Clean up test environment."""
        self.db_patcher.stop()
        self.api_key_patcher.stop()
        Path(self.test_db.name).unlink()
    
    @patch('src.brokers.polygon.core.requests.get')
    def test_end_to_end_data_fetching(self, mock_get):
        """Test complete pipeline for various tickers."""
        # Test data for different tickers
        test_cases = [
            ("SPY", "5minute", "5Minute"),
            ("AAPL", "1minute", "1Minute"),
            ("MSFT", "15minute", "15Minute"),
            ("GOOGL", "60minute", "60Minute"),
        ]
        
        for ticker, cli_timeframe, db_timeframe in test_cases:
            with self.subTest(ticker=ticker, timeframe=cli_timeframe):
                # Mock API response
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "status": "OK",
                    "results": [
                        {"t": 1640995200000, "o": 100.0, "h": 101.0, "l": 99.0, "c": 100.5, "v": 1000},
                        {"t": 1640995500000, "o": 100.5, "h": 101.5, "l": 100.0, "c": 101.0, "v": 1500},
                        {"t": 1640995800000, "o": 101.0, "h": 102.0, "l": 100.5, "c": 101.5, "v": 2000}
                    ]
                }
                mock_get.return_value = mock_response
                
                # Calculate date range
                from_date, to_date = calculate_date_range(10, cli_timeframe)
                
                # Get API parameters
                multiplier, timespan = map_timeframe_for_api(cli_timeframe)
                
                # Fetch data
                bars = fetch_ohlcv(ticker, multiplier, timespan, from_date, to_date)
                
                # Create table
                create_table(ticker, db_timeframe)
                
                # Insert data
                inserted = insert_bars(ticker, db_timeframe, bars)
                
                # Verify results
                self.assertEqual(inserted, 3)
                
                # Verify data in database
                conn = sqlite3.connect(self.test_db.name)
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM market_data_{ticker}_{db_timeframe}")
                count = cursor.fetchone()[0]
                self.assertEqual(count, 3)
                
                # Verify data content
                cursor.execute(f"""
                    SELECT timestamp, open, high, low, close, volume 
                    FROM market_data_{ticker}_{db_timeframe}
                    ORDER BY timestamp
                """)
                rows = cursor.fetchall()
                
                # Check first row
                self.assertEqual(rows[0][1], 100.0)  # open
                self.assertEqual(rows[0][2], 101.0)  # high
                self.assertEqual(rows[0][3], 99.0)   # low
                self.assertEqual(rows[0][4], 100.5)  # close
                self.assertEqual(rows[0][5], 1000)   # volume
                
                conn.close()
    
    @patch('src.brokers.polygon.core.requests.get')
    def test_duplicate_prevention(self, mock_get):
        """Test that duplicate data is not inserted."""
        # Mock API response with duplicates
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "OK",
            "results": [
                {"t": 1640995200000, "o": 100.0, "h": 101.0, "l": 99.0, "c": 100.5, "v": 1000},
                {"t": 1640995500000, "o": 100.5, "h": 101.5, "l": 100.0, "c": 101.0, "v": 1500}
            ]
        }
        mock_get.return_value = mock_response
        
        # Create table
        create_table("TEST", "5Minute")
        
        # First insert
        bars = [
            {"t": 1640995200000, "o": 100.0, "h": 101.0, "l": 99.0, "c": 100.5, "v": 1000},
            {"t": 1640995500000, "o": 100.5, "h": 101.5, "l": 100.0, "c": 101.0, "v": 1500}
        ]
        inserted1 = insert_bars("TEST", "5Minute", bars)
        self.assertEqual(inserted1, 2)
        
        # Try to insert same data again
        inserted2 = insert_bars("TEST", "5Minute", bars)
        self.assertEqual(inserted2, 0)
        
        # Try to insert partially overlapping data
        bars_partial = [
            {"t": 1640995500000, "o": 100.5, "h": 101.5, "l": 100.0, "c": 101.0, "v": 1500},  # Duplicate
            {"t": 1640995800000, "o": 101.0, "h": 102.0, "l": 100.5, "c": 101.5, "v": 2000}   # New
        ]
        inserted3 = insert_bars("TEST", "5Minute", bars_partial)
        self.assertEqual(inserted3, 1)  # Only new record inserted
        
        # Verify total count
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM market_data_TEST_5Minute")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 3)  # Total of 3 unique records
        conn.close()
    
    def test_table_creation_idempotent(self):
        """Test that table creation is idempotent."""
        # Create table multiple times
        for _ in range(3):
            create_table("IDEMPOTENT", "1Minute")
        
        # Verify only one table exists
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM sqlite_master 
            WHERE type='table' AND name='market_data_IDEMPOTENT_1Minute'
        """)
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)
        conn.close()
    
    def test_empty_results_handling(self):
        """Test handling of empty API results."""
        # Create table
        create_table("EMPTY", "5Minute")
        
        # Insert empty bars
        inserted = insert_bars("EMPTY", "5Minute", [])
        self.assertEqual(inserted, 0)
        
        # Verify no data in table
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM market_data_EMPTY_5Minute")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)
        conn.close()
    
    def test_date_range_calculation_consistency(self):
        """Test date range calculation for different bar counts."""
        test_cases = [
            (100, "5minute"),
            (500, "15minute"),
            (1000, "1minute"),
            (50, "60minute"),
        ]
        
        for bars, timeframe in test_cases:
            with self.subTest(bars=bars, timeframe=timeframe):
                from_date, to_date = calculate_date_range(bars, timeframe)
                
                # Parse dates
                from_dt = datetime.strptime(from_date, "%Y-%m-%d")
                to_dt = datetime.strptime(to_date, "%Y-%m-%d")
                
                # Verify from_date is before to_date
                self.assertLess(from_dt, to_dt)
                
                # Verify reasonable date range (not too far in past)
                days_diff = (to_dt - from_dt).days
                self.assertLess(days_diff, 365)  # Should be less than a year


if __name__ == "__main__":
    unittest.main()