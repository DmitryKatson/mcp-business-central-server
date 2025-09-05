"""
FastMCP Cloud entry point for Business Central MCP Server
"""

from .server import mcp

# Import tools to register them with the MCP server
from .tools import implementations  # noqa: F401

# FastMCP Cloud will import this object
server = mcp