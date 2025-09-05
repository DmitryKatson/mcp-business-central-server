#!/usr/bin/env python3
"""
Main entry point for the Business Central MCP Server.

This file allows the package to be executed with: python -m mcp_business_central
"""

import asyncio
from .core.dependencies import mcp


async def main() -> None:
    """
    Main entry point for the Business Central MCP server.
    
    Initializes all components and starts the MCP server to handle client requests.
    """
    try:
        # Import tools to register them with the MCP server
        from .tools import implementations  # noqa: F401
        
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


if __name__ == "__main__":
    asyncio.run(main())
