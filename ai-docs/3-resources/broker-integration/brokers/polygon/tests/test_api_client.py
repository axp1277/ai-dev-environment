"""Simple unit tests for API client functionality."""
import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.brokers.polygon.core import fetch_ohlcv


class TestAPIClient(unittest.TestCase):
    """Test Polygon API client functions."""
    
    @patch('src.brokers.polygon.core.load_api_key')
    @patch('src.brokers.polygon.core.requests.get')
    def test_fetch_ohlcv_success(self, mock_get, mock_load_key):
        """Test successful OHLCV data fetch."""
        # Mock API key
        mock_load_key.return_value = "test_api_key"
        
        # Mock successful response
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
        
        # Test fetch
        results = fetch_ohlcv("SPY", 5, "minute", "2023-01-01", "2023-01-02")
        
        # Verify URL construction
        expected_url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/5/minute/2023-01-01/2023-01-02"
        mock_get.assert_called_once_with(
            expected_url,
            params={
                "apiKey": "test_api_key",
                "adjusted": "true",
                "sort": "asc",
                "limit": 50000
            }
        )
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["o"], 100.0)
        self.assertEqual(results[1]["c"], 101.0)
    
    @patch('src.brokers.polygon.core.load_api_key')
    @patch('src.brokers.polygon.core.requests.get')
    def test_fetch_ohlcv_api_error(self, mock_get, mock_load_key):
        """Test API error handling."""
        mock_load_key.return_value = "test_api_key"
        
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response
        
        # Test error handling
        with self.assertRaises(Exception) as context:
            fetch_ohlcv("SPY", 5, "minute", "2023-01-01", "2023-01-02")
        
        self.assertIn("API error: 401", str(context.exception))
        self.assertIn("Unauthorized", str(context.exception))
    
    @patch('src.brokers.polygon.core.load_api_key')
    @patch('src.brokers.polygon.core.requests.get')
    def test_fetch_ohlcv_status_not_ok(self, mock_get, mock_load_key):
        """Test handling of non-OK status."""
        mock_load_key.return_value = "test_api_key"
        
        # Mock response with error status
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "ERROR",
            "message": "Invalid ticker"
        }
        mock_get.return_value = mock_response
        
        # Test status handling
        with self.assertRaises(Exception) as context:
            fetch_ohlcv("INVALID", 5, "minute", "2023-01-01", "2023-01-02")
        
        self.assertIn("API returned status: ERROR", str(context.exception))
    
    @patch('src.brokers.polygon.core.load_api_key')
    @patch('src.brokers.polygon.core.requests.get')
    def test_fetch_ohlcv_empty_results(self, mock_get, mock_load_key):
        """Test handling of empty results."""
        mock_load_key.return_value = "test_api_key"
        
        # Mock response with no results
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "OK",
            "results": []
        }
        mock_get.return_value = mock_response
        
        # Test empty results
        results = fetch_ohlcv("SPY", 5, "minute", "2023-01-01", "2023-01-02")
        self.assertEqual(results, [])
    
    @patch('src.brokers.polygon.core.load_api_key')
    @patch('src.brokers.polygon.core.requests.get')
    def test_fetch_ohlcv_url_construction(self, mock_get, mock_load_key):
        """Test URL construction with different parameters."""
        mock_load_key.return_value = "test_api_key"
        
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "OK", "results": []}
        mock_get.return_value = mock_response
        
        # Test different parameter combinations
        test_cases = [
            ("AAPL", 1, "minute", "2023-01-01", "2023-01-02"),
            ("MSFT", 15, "minute", "2023-02-01", "2023-02-28"),
            ("GOOGL", 1, "hour", "2023-03-01", "2023-03-31"),
        ]
        
        for ticker, multiplier, timespan, from_date, to_date in test_cases:
            mock_get.reset_mock()
            fetch_ohlcv(ticker, multiplier, timespan, from_date, to_date)
            
            expected_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
            actual_url = mock_get.call_args[0][0]
            self.assertEqual(actual_url, expected_url)


if __name__ == "__main__":
    unittest.main()