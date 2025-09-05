"""
Authentication management for Business Central APIs.

This module handles OAuth2 authentication with Azure AD for accessing
Microsoft Dynamics 365 Business Central APIs.
"""

from .manager import BCAuthManager, BearerAuthManager, build_clients_from_headers

__all__ = ["BCAuthManager", "BearerAuthManager", "build_clients_from_headers"]
