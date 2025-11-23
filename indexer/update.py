#!/usr/bin/env python3
"""
Simple script to run incremental updates (only new videos since last run)
"""

import sys
from pathlib import Path

def run_incremental_update():
    """Run the enhanced indexer for incremental updates."""
    print("🚀 Running incremental update...")
    print("This will only process new videos since the last run.")
    
    # Import and run the enhanced indexer
    sys.path.append(str(Path(__file__).parent))
    from enhanced_indexer import main
    
    main()

if __name__ == '__main__':
    run_incremental_update()