#!/usr/bin/env python3
"""YouTube MP4 Downloader - Main entry point."""

import sys
from pathlib import Path

# Add src to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.main_window import main

if __name__ == "__main__":
    main()
