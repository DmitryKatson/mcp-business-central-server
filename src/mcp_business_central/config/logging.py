"""
Logging configuration and utilities.

This module provides centralized logging configuration and utilities
for the Business Central MCP server.
"""

import logging
import sys
from typing import Optional

from .config import LoggingConfig


def setup_logging(config: Optional[LoggingConfig] = None) -> None:
    """
    Set up logging configuration for the application.
    
    Args:
        config: Logging configuration. If None, loads from environment.
    """
    if config is None:
        config = LoggingConfig.from_environment()
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.level.upper(), logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(config.format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if configured)
    if config.log_file:
        try:
            file_handler = logging.FileHandler(config.log_file)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            # Log to console if file logging fails
            console_handler.handle(
                logging.LogRecord(
                    name="logging_setup",
                    level=logging.WARNING,
                    pathname="",
                    lineno=0,
                    msg=f"Failed to setup file logging: {e}",
                    args=(),
                    exc_info=None
                )
            )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)
