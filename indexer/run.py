#!/usr/bin/env python3
"""
RocketScope Indexer
Run this to update the player mention database.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the main indexer."""
    indexer_path = Path(__file__).parent / 'main.py'
    
    print("RocketScope Indexer")
    print("This will search for player mentions in YouTube videos.")
    print()
    
    try:
        subprocess.run([sys.executable, str(indexer_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Indexer failed with exit code {e.returncode}")
        return 1
    except KeyboardInterrupt:
        print("\\nIndexing interrupted by user")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())