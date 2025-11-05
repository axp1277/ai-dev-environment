"""Simple unit tests for core functionality."""
import os
import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.brokers.polygon.core import (
    calculate_date_range,
    create_table,
    get_db_connection,
    insert_bars,
    load_api_key,
    map_timeframe_for_api,
    map_timeframe_for_table,
)


class TestEnvironmentConfiguration(unittest.TestCase):
    """Test environment configuration."""
    
    def test_load_api_key_success(self):
        """Test loading API key from environment."""
        with patch.dict(os.environ, {"POLYGON_API_KEY": "test_key_123"}):
            key = load_api_key()
            self.assertEqual(key, "test_key_123")
    
    def test_load_api_key_missing(self):
        """Test error when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                load_api_key()
            self.assertIn("POLYGON_API_KEY not found", str(context.exception))


class TestTimeframeMappings(unittest.TestCase):
    """Test timeframe mapping functions."""
    
    def test_map_timeframe_for_api(self):
        """Test mapping CLI timeframes to API parameters."""
        self.assertEqual(map_timeframe_for_api("1minute"), (1, "minute"))
        self.assertEqual(map_timeframe_for_api("5minute"), (5, "minute"))
        self.assertEqual(map_timeframe_for_api("15minute"), (15, "minute"))
        self.assertEqual(map_timeframe_for_api("60minute"), (1, "hour"))
    
    def test_map_timeframe_for_api_invalid(self):
        """Test error for invalid timeframe."""
        with self.assertRaises(ValueError):
            map_timeframe_for_api("invalid")
    
    def test_map_timeframe_for_table(self):
        """Test mapping CLI timeframes to table names."""
        self.assertEqual(map_timeframe_for_table("1minute"), "1Minute")
        self.assertEqual(map_timeframe_for_table("5minute"), "5Minute")
        self.assertEqual(map_timeframe_for_table("15minute"), "15Minute")
        self.assertEqual(map_timeframe_for_table("60minute"), "60Minute")


class TestDateCalculations(unittest.TestCase):
    """Test date range calculations."""
    
    def test_calculate_date_range(self):
        """Test date range calculation."""
        from_date, to_date = calculate_date_range(100, "5minute")
        
        # Check format
        self.assertRegex(from_date, r"\d{4}-\d{2}-\d{2}")
        self.assertRegex(to_date, r"\d{4}-\d{2}-\d{2}")
        
        # Check from_date is before to_date
        self.assertLess(from_date, to_date)
    
    def test_calculate_date_range_invalid_timeframe(self):
        """Test error for invalid timeframe."""
        with self.assertRaises(ValueError):
            calculate_date_range(100, "invalid")


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations."""
    
    def setUp(self):
        """Set up test database."""
        self.test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.test_db.close()
        
        # Patch get_db_connection to use test database
        self.patcher = patch("src.brokers.polygon.core.get_db_connection")
        mock_get_db = self.patcher.start()
        mock_get_db.return_value = sqlite3.connect(self.test_db.name)
    
    def tearDown(self):
        """Clean up test database."""
        self.patcher.stop()
        Path(self.test_db.name).unlink()
    
    def test_create_table(self):
        """Test table creation."""
        create_table("SPY", "5Minute")
        
        # Check table exists
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='market_data_SPY_5Minute'
        """)
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
    
    def test_insert_bars(self):
        """Test inserting bars."""
        create_table("SPY", "5Minute")
        
        # Test data
        bars = [
            {"t": 1640995200000, "o": 100.0, "h": 101.0, "l": 99.0, "c": 100.5, "v": 1000},
            {"t": 1640995500000, "o": 100.5, "h": 101.5, "l": 100.0, "c": 101.0, "v": 1500}
        ]
        
        inserted = insert_bars("SPY", "5Minute", bars)
        self.assertEqual(inserted, 2)
        
        # Verify data in database
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM market_data_SPY_5Minute")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 2)
    
    def test_insert_bars_duplicate_prevention(self):
        """Test duplicate prevention."""
        create_table("SPY", "5Minute")
        
        # Insert same data twice
        bars = [{"t": 1640995200000, "o": 100.0, "h": 101.0, "l": 99.0, "c": 100.5, "v": 1000}]
        
        inserted1 = insert_bars("SPY", "5Minute", bars)
        inserted2 = insert_bars("SPY", "5Minute", bars)
        
        self.assertEqual(inserted1, 1)
        self.assertEqual(inserted2, 0)  # Should not insert duplicate
        
        # Verify only one row in database
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM market_data_SPY_5Minute")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 1)


class TestSchemaValidation(unittest.TestCase):
    """Test database schema validation."""
    
    def setUp(self):
        """Set up test database."""
        self.test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.test_db.close()
        
        # Patch get_db_connection to use test database
        self.patcher = patch("src.brokers.polygon.core.get_db_connection")
        mock_get_db = self.patcher.start()
        mock_get_db.return_value = sqlite3.connect(self.test_db.name)
    
    def tearDown(self):
        """Clean up test database."""
        self.patcher.stop()
        Path(self.test_db.name).unlink()
    
    def test_schema_structure(self):
        """Test that created table has exact schema structure."""
        create_table("ES", "15Minute")
        
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        
        # Get table schema
        cursor.execute("PRAGMA table_info(market_data_ES_15Minute)")
        columns = cursor.fetchall()
        
        # Expected columns
        expected_columns = [
            ('id', 'INTEGER', 0, None, 1),
            ('timestamp', 'DATETIME', 1, None, 0),
            ('open', 'REAL', 1, None, 0),
            ('high', 'REAL', 1, None, 0),
            ('low', 'REAL', 1, None, 0),
            ('close', 'REAL', 1, None, 0),
            ('volume', 'INTEGER', 1, None, 0)
        ]
        
        # Verify columns
        self.assertEqual(len(columns), 7)
        for i, col in enumerate(columns):
            expected = expected_columns[i]
            self.assertEqual(col[1], expected[0])  # name
            self.assertEqual(col[2], expected[1])  # type
            self.assertEqual(col[3], expected[2])  # notnull
            
        conn.close()
    
    def test_unique_constraint(self):
        """Test UNIQUE constraint on timestamp."""
        create_table("NQ", "1Minute")
        
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        
        # Get indexes
        cursor.execute("PRAGMA index_list(market_data_NQ_1Minute)")
        indexes = cursor.fetchall()
        
        # Check for unique index on timestamp
        unique_found = False
        for idx in indexes:
            if idx[2] == 1:  # unique index
                cursor.execute(f"PRAGMA index_info({idx[1]})")
                idx_cols = cursor.fetchall()
                for col in idx_cols:
                    if col[2] == 'timestamp':
                        unique_found = True
                        break
        
        self.assertTrue(unique_found, "UNIQUE constraint on timestamp not found")
        conn.close()
    
    def test_timestamp_index(self):
        """Test index creation on timestamp."""
        create_table("YM", "60Minute")
        
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        
        # Check for timestamp index
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND name='idx_YM_60Minute_timestamp'
        """)
        result = cursor.fetchone()
        
        self.assertIsNotNone(result, "Timestamp index not found")
        conn.close()
    
    def test_primary_key(self):
        """Test id column is primary key with autoincrement."""
        create_table("SPX", "5Minute")
        
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("PRAGMA table_info(market_data_SPX_5Minute)")
        columns = cursor.fetchall()
        
        # First column should be id with pk=1
        id_col = columns[0]
        self.assertEqual(id_col[1], 'id')
        self.assertEqual(id_col[5], 1)  # pk flag
        
        conn.close()


if __name__ == "__main__":
    unittest.main()