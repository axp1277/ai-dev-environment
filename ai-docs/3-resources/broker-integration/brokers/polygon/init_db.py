#!/usr/bin/env python
"""Initialize market_data.db with proper schema."""
import sqlite3
from pathlib import Path


def initialize_database():
    """Initialize market_data.db file in data/ directory."""
    # Find project root
    current_dir = Path.cwd()
    project_root = None
    
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / "pyproject.toml").exists():
            project_root = parent
            break
    
    if not project_root:
        db_path = Path("market_data.db")
        print("Warning: Could not find project root, using current directory")
    else:
        # Create data directory if it doesn't exist
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)
        db_path = data_dir / "market_data.db"
    
    # Create connection (this creates the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    
    # Enable foreign keys (good practice)
    conn.execute("PRAGMA foreign_keys = ON")
    
    # Close connection
    conn.close()
    
    print(f"Created database: {db_path.absolute()}")
    return db_path


def verify_schema(ticker: str, timeframe: str):
    """Verify table schema matches expected structure."""
    table_name = f"{ticker}_{timeframe}"
    
    # Use same logic as get_db_connection to find database
    current_dir = Path.cwd()
    project_root = None
    
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / "pyproject.toml").exists():
            project_root = parent
            break
    
    if not project_root:
        db_path = "market_data.db"
    else:
        db_path = project_root / "data" / "market_data.db"
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?
    """, (table_name,))
    
    if not cursor.fetchone():
        print(f"Table {table_name} does not exist")
        conn.close()
        return False
    
    # Get table schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    # Expected schema
    expected_columns = [
        (0, 'id', 'INTEGER', 0, None, 1),
        (1, 'timestamp', 'DATETIME', 1, None, 0),
        (2, 'open', 'REAL', 1, None, 0),
        (3, 'high', 'REAL', 1, None, 0),
        (4, 'low', 'REAL', 1, None, 0),
        (5, 'close', 'REAL', 1, None, 0),
        (6, 'volume', 'INTEGER', 1, None, 0)
    ]
    
    # Verify columns match
    for i, col in enumerate(columns):
        expected = expected_columns[i]
        if col[1] != expected[1] or col[2] != expected[2] or col[3] != expected[3]:
            print(f"Column mismatch: {col} != {expected}")
            conn.close()
            return False
    
    # Check for UNIQUE constraint on timestamp
    cursor.execute(f"PRAGMA index_list({table_name})")
    indexes = cursor.fetchall()
    
    unique_on_timestamp = False
    for idx in indexes:
        if idx[2] == 1:  # unique index
            cursor.execute(f"PRAGMA index_info({idx[1]})")
            idx_info = cursor.fetchall()
            for info in idx_info:
                if info[2] == 'timestamp':
                    unique_on_timestamp = True
                    break
    
    if not unique_on_timestamp:
        print("UNIQUE constraint on timestamp not found")
        conn.close()
        return False
    
    # Check for timestamp index
    index_name = f"idx_{table_name}_timestamp"
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='index' AND name=?
    """, (index_name,))
    
    if not cursor.fetchone():
        print(f"Index {index_name} not found")
        conn.close()
        return False
    
    conn.close()
    print(f"Schema verification passed for {table_name}")
    return True


if __name__ == "__main__":
    # Initialize database
    initialize_database()
    
    try:
        # Test creating a sample table and verifying schema
        from core import create_table
        
        print("\nTesting table creation...")
        create_table("TEST", "5Minute")
        
        print("\nVerifying schema...")
        verify_schema("TEST", "5Minute")
    except ImportError as e:
        print(f"\nSkipping test (missing dependencies): {e}")
        print("Run 'pip install -r requirements.txt' to install dependencies")