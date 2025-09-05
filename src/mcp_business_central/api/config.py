"""
Configuration management for the Business Central MCP server.

This module handles all configuration loading and validation,
providing a centralized configuration management system.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

from ..logging.exceptions import ConfigurationError


def build_business_central_url(tenant_id: str, environment: str = "production") -> str:
    """
    Build the Business Central API base URL.
    
    Args:
        tenant_id: Azure AD tenant ID or Business Central tenant name
        environment: Environment (production or sandbox)
        
    Returns:
        Complete Business Central API base URL
    """
    return f"https://api.businesscentral.dynamics.com/v2.0/{tenant_id}/{environment}/api/v2.0"


@dataclass(frozen=True)
class BCServerConfig:
    """Business Central server configuration."""
    
    tenant_id: str
    client_id: str
    client_secret: str
    environment: str
    base_url: str
    
    @classmethod
    def from_environment(cls) -> 'BCServerConfig':
        """Load configuration from environment variables."""
        load_dotenv()
        
        tenant_id = os.getenv('BC_TENANT_ID')
        client_id = os.getenv('BC_CLIENT_ID')
        client_secret = os.getenv('BC_CLIENT_SECRET')
        environment = os.getenv('BC_ENVIRONMENT', 'production')
        
        # Validate required configuration
        missing_vars = []
        if not tenant_id:
            missing_vars.append('BC_TENANT_ID')
        if not client_id:
            missing_vars.append('BC_CLIENT_ID')
        if not client_secret:
            missing_vars.append('BC_CLIENT_SECRET')
            
        if missing_vars:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
        base_url = build_business_central_url(tenant_id, environment)
        
        return cls(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            environment=environment,
            base_url=base_url
        )
    
    @classmethod
    def from_headers(cls, tenant_id: str, environment: str = "production", 
                     client_id: str = "", client_secret: str = "") -> 'BCServerConfig':
        """
        Create configuration from header-provided values.
        
        Args:
            tenant_id: Azure AD tenant ID or Business Central tenant name
            environment: Environment (production or sandbox)
            client_id: Optional Azure AD client ID
            client_secret: Optional Azure AD client secret
            
        Returns:
            BCServerConfig instance
        """
        base_url = build_business_central_url(tenant_id, environment)
        
        return cls(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            environment=environment,
            base_url=base_url
        )


# Lazy configuration singleton
_config = None

def get_default_config():
    """Get configuration, loading it lazily when first needed."""
    global _config
    if _config is None:
        try:
            from ..logging import get_logger
            logger = get_logger(__name__)
            _config = BCServerConfig.from_environment()
        except Exception as e:
            # Import logger here to avoid circular imports
            from ..logging import get_logger
            logger = get_logger(__name__)
            logger.error(f"Failed to load configuration: {e}")
            raise
    return _config


@dataclass(frozen=True)
class LoggingConfig:
    """Logging configuration."""
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None
    
    @classmethod
    def from_environment(cls) -> 'LoggingConfig':
        """
        Load logging configuration from environment variables.
        
        Environment variables:
        - LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        - LOG_FORMAT: Custom log format string
        - LOG_FILE: Path to log file (optional, enables file logging)
        - MCP_VERBOSE: Set to 'true' to show INFO logs in Cursor (shows as [error])
        """
        load_dotenv()
        
        return cls(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            format=os.getenv('LOG_FORMAT', cls.format),
            log_file=os.getenv('LOG_FILE')
        )
