"""
Dependency injection container for the Business Central MCP server.

This module provides centralized dependency injection and component
initialization for the entire application.
"""

from typing import Optional, Tuple, Any, Mapping
from mcp.server.fastmcp import FastMCP

from ..config import BCServerConfig, LoggingConfig, setup_logging, get_logger
from ..auth import BCAuthManager
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

# Legacy compatibility - these will be created when first accessed
def config():
    return get_config()

def auth_manager():
    return get_auth_manager()

def api_client():
    return get_api_client()

def company_manager():
    return get_company_manager()

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
class BearerAuthManager:
    """Simple auth manager that returns a pre-provided bearer token."""

    def __init__(self, access_token: str) -> None:
        self._access_token = access_token

    async def get_access_token(self) -> str:
        return self._access_token


def _lower_headers(headers: Mapping[str, str]) -> Mapping[str, str]:
    try:
        return {str(k).lower(): v for k, v in headers.items()}
    except Exception:
        return {}


def build_clients_from_headers(headers: Mapping[str, str]) -> Optional[Tuple['BCAPIClient', 'CompanyManager']]:
    """Build API and company managers from HTTP headers if present.

    Supported headers (case-insensitive):
      - Authorization: Bearer <token>
      - X-BC-Tenant-Id: Tenant GUID or name (required for base URL)
      - X-BC-Environment: production|sandbox (default production)
      - X-BC-Client-Id / X-BC-Client-Secret (for client credentials path)
    """
    h = _lower_headers(headers or {})

    tenant_id = h.get('x-bc-tenant-id')
    environment = h.get('x-bc-environment', 'production')
    authz = h.get('authorization') or ''
    client_id = h.get('x-bc-client-id')
    client_secret = h.get('x-bc-client-secret')

    if not tenant_id:
        # Cannot construct base_url without tenant
        return None

    # Construct a minimal config – client credentials optional for bearer path
    base_url = f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/{environment}/api/v2.0"
    cfg = BCServerConfig(
        tenant_id=tenant_id,
        client_id=client_id or "",
        client_secret=client_secret or "",
        environment=environment,
        base_url=base_url,
    )

    # Prefer bearer token if provided
    if authz.lower().startswith('bearer '):
        token = authz.split(' ', 1)[1].strip()
        auth = BearerAuthManager(token)
        api = BCAPIClient(cfg, auth)
        return api, CompanyManager(api)

    # Fall back to client credentials if both present
    if client_id and client_secret:
        auth = BCAuthManager(cfg)
        api = BCAPIClient(cfg, auth)
        return api, CompanyManager(api)

    return None


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


# Legacy function wrappers for backward compatibility
# These will be removed in the future, use the new components directly

async def bc_request(method: str, resource: str, item_id: Optional[str] = None, 
                    params: Optional[dict] = None, data: Optional[dict] = None,
                    company_id: Optional[str] = None) -> dict:
    """Legacy wrapper for API requests - use api_client.request() instead."""
    from ..config.exceptions import APIError
    
    try:
        if not company_id:
            company_id = await get_company_manager().get_active_company_id()
        
        result = await get_api_client().request(method, resource, item_id, params, data, company_id)
        return result
    except APIError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


async def discover_companies():
    """Legacy wrapper for company discovery - use company_manager.discover_companies() instead."""
    try:
        companies = await get_company_manager().discover_companies()
        return [{"id": c.id, "name": c.name, "displayName": c.display_name} for c in companies]
    except Exception:
        return []


async def get_default_company():
    """Legacy wrapper for default company - use company_manager.get_default_company() instead."""
    try:
        company = await get_company_manager().get_default_company()
        return {"id": company.id, "name": company.name} if company else None
    except Exception:
        return None


async def set_company(company_id: str) -> bool:
    """Legacy wrapper for setting company - use company_manager.set_active_company() instead."""
    try:
        await get_company_manager().set_active_company(company_id)
        return True
    except Exception:
        return False


async def get_active_company_id() -> Optional[str]:
    """Legacy wrapper for active company ID - use company_manager.get_active_company_id() instead."""
    try:
        return await get_company_manager().get_active_company_id()
    except Exception:
        return None
