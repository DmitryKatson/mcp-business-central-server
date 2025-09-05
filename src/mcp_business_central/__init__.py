"""
Microsoft Dynamics 365 Business Central MCP Server.

This package provides MCP tools for interacting with Business Central APIs,
featuring OAuth2 authentication, company management, and comprehensive
business data access with a professional, scalable architecture.
"""

import asyncio
from .server import mcp

# --- Main Entry Point Functions ---

async def main() -> None:
    """
    Main entry point for the Business Central MCP server.
    
    Initializes all components and starts the MCP server to handle client requests.
    """
    try:
        # Import tools to register them with the MCP server
        from .tools import mcp_tools  # noqa: F401
        
        # Run the MCP server - logging happens after protocol establishment
        await mcp.run_stdio_async()
        
    except KeyboardInterrupt:
        # Silent shutdown for MCP compatibility
        pass
    except Exception as e:
        # Only log critical errors that would prevent server startup
        import sys
        print(f"Critical server error: {e}", file=sys.stderr)
        raise

def main_entry():
    """Main entry point for the package."""
    asyncio.run(main())

# --- FastMCP Cloud Entry Point ---
# FastMCP Cloud will import this object
server = mcp

# --- Python Module Execution Support ---
# This allows: python -m mcp_business_central
if __name__ == "__main__":
    asyncio.run(main())

__all__ = [
    "main_entry",
    "main", 
    "server",  # FastMCP Cloud entry point
    "mcp",     # Direct MCP server access
    # Main modules
    "api",      # Everything to work with BC APIs
    "auth",     # Everything to work with BC auth  
    "tools",    # MCP tools definitions
    "logging",  # Logging and error handling
    "utils"     # Helper functions
]

__version__ = "1.0.0"
