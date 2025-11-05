"""Simple unit tests for CLI functionality."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.brokers.polygon.cli import main


class TestCLI(unittest.TestCase):
    """Test CLI interface."""
    
    def test_cli_wrong_arguments(self):
        """Test CLI with wrong number of arguments."""
        # Test with too few arguments
        with patch.object(sys, "argv", ["fetch.py", "SPY"]):
            result = main()
            self.assertEqual(result, 1)
        
        # Test with too many arguments
        with patch.object(sys, "argv", ["fetch.py", "SPY", "5minute", "100", "extra"]):
            result = main()
            self.assertEqual(result, 1)
    
    def test_cli_invalid_bars(self):
        """Test CLI with invalid bars value."""
        with patch.object(sys, "argv", ["fetch.py", "SPY", "5minute", "not_a_number"]):
            result = main()
            self.assertEqual(result, 1)
    
    def test_cli_invalid_timeframe(self):
        """Test CLI with invalid timeframe."""
        with patch.object(sys, "argv", ["fetch.py", "SPY", "invalid", "100"]):
            result = main()
            self.assertEqual(result, 1)
    
    @patch("src.brokers.polygon.cli.fetch_ohlcv")
    @patch("src.brokers.polygon.cli.create_table")
    @patch("src.brokers.polygon.cli.insert_bars")
    def test_cli_success(self, mock_insert, mock_create, mock_fetch):
        """Test successful CLI execution."""
        # Mock return values
        mock_fetch.return_value = [
            {"t": 1640995200000, "o": 100.0, "h": 101.0, "l": 99.0, "c": 100.5, "v": 1000}
        ]
        mock_insert.return_value = 1
        
        with patch.object(sys, "argv", ["fetch.py", "SPY", "5minute", "100"]):
            result = main()
            self.assertEqual(result, 0)
            
            # Verify calls
            mock_create.assert_called_once_with("SPY", "5Minute")
            mock_insert.assert_called_once()
    
    @patch("src.brokers.polygon.cli.fetch_ohlcv")
    def test_cli_api_error(self, mock_fetch):
        """Test CLI handling of API errors."""
        mock_fetch.side_effect = Exception("API error")
        
        with patch.object(sys, "argv", ["fetch.py", "SPY", "5minute", "100"]):
            result = main()
            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()