"""
Core business logic for Business Central MCP integration.

This module contains the central business logic components including
dependency injection and company management.
"""

from .company_manager import CompanyManager

__all__ = ["CompanyManager"]
