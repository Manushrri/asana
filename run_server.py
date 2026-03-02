#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "fastmcp>=0.1.0",
#     "requests>=2.31.0",
#     "python-dotenv>=1.0.0",
#     "aiohttp>=3.9.0",
# ]
# ///
"""
Asana MCP Server
Run this to start the MCP server for Asana integration.
"""

import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.main import main

if __name__ == "__main__":
    main()

