"""
Main server module for the Business Central MCP server.

This module handles server startup, initialization, and MCP server execution.
"""

import asyncio
from .dependencies import logger, mcp


async def main() -> None:
    """
    Main entry point for the Business Central MCP server.
    
    Initializes all components and starts the MCP server to handle client requests.
    """
    try:
        # Log server startup
        logger.info("Starting Business Central MCP server...")
        
        # Import tools to register them with the MCP server
        from ..tools import implementations  # noqa: F401
        
        # Run the MCP server
        logger.info("Running MCP server...")
        await mcp.run_stdio_async()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        logger.info("Business Central MCP server stopped")


if __name__ == "__main__":
    # Direct script execution entry point
    asyncio.run(main())