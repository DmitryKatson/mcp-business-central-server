"""
FastMCP Cloud entry point for Business Central MCP Server
"""
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_business_central.core.dependencies import mcp

# FastMCP Cloud will import this object
server = mcp