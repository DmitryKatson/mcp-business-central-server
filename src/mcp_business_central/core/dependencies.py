"""
Dependency injection container for the Business Central MCP server.

This module provides centralized dependency injection and component
initialization for the entire application.
"""

from typing import Tuple, Any, Mapping
from mcp.server.fastmcp import FastMCP

from ..config import BCServerConfig, setup_logging, get_logger
from ..auth import BCAuthManager, build_clients_from_headers
from ..api import BCAPIClient
from .company_manager import CompanyManager

# Initialize logging with MCP-safe configuration
setup_logging()

# Enable verbose logging if requested via environment variable
import os
if os.getenv('MCP_VERBOSE', '').lower() == 'true':
    from ..config.logging import enable_verbose_logging
    enable_verbose_logging()

logger = get_logger(__name__)

# Lazy initialization - components will be created when first needed
_config = None
_auth_manager = None
_api_client = None
_company_manager = None

def get_config():
    """Get configuration, loading it lazily when first needed."""
    global _config
    if _config is None:
        try:
            _config = BCServerConfig.from_environment()
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    return _config

def get_auth_manager():
    """Get auth manager, creating it lazily when first needed."""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = BCAuthManager(get_config())
    return _auth_manager

def get_api_client():
    """Get API client, creating it lazily when first needed."""
    global _api_client
    if _api_client is None:
        _api_client = BCAPIClient(get_config(), get_auth_manager())
    return _api_client

def get_company_manager():
    """Get company manager, creating it lazily when first needed."""
    global _company_manager
    if _company_manager is None:
        _company_manager = CompanyManager(get_api_client())
    return _company_manager

# Initialize MCP server
mcp = FastMCP(
    name="mcp-business-central-server",
    instructions=(
        "This server provides tools to interact with Microsoft Dynamics 365 Business Central. "
        "Companies are auto-discovered and the server supports multi-tenant operations with "
        "professional-grade architecture and comprehensive business data access."
    )
)


# --- Request-scoped auth support (headers-driven) ---


def get_request_clients(ctx: Any) -> Tuple['BCAPIClient', 'CompanyManager']:
    """Resolve per-request clients from context headers, or fall back to env-backed singletons."""
    try:
        headers: Mapping[str, str] = {}
        req = getattr(ctx, 'request', None)
        if req is not None:
            headers = getattr(req, 'headers', {}) or {}
        built = build_clients_from_headers(headers)
        if built is not None:
            return built
    except Exception:
        # Ignore context/header parsing issues and fall back gracefully
        pass

    # Fallback to env-backed singletons
    return get_api_client(), get_company_manager()
