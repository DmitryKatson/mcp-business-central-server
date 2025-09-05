"""
Adapter file for FastMCP inspect/run.

Usage:
  - pip install -e .
  - fastmcp inspect server_entry.py:server

Or without install:
  - PowerShell:   $env:PYTHONPATH = "$PWD/src"; fastmcp inspect server_entry.py:server
  - macOS/Linux:  PYTHONPATH="$PWD/src" fastmcp inspect server_entry.py:server
"""

from mcp_business_central.server import mcp as server


