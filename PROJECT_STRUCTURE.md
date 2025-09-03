# Project Structure

## Overview

The Business Central MCP Server follows a professional, modular architecture with clear separation of concerns. The codebase is organized into logical modules that follow industry best practices for Python projects.

## Directory Structure

```
src/mcp_business_central/
├── __init__.py                      # Main package entry point
├── __main__.py                      # CLI execution entry point
├── core/                           # Core business logic
│   ├── __init__.py                 # Core module exports
│   ├── server.py                   # MCP server setup and lifecycle
│   ├── company_manager.py          # Company discovery and management
│   └── dependencies.py            # Dependency injection container
├── api/                           # API layer
│   ├── __init__.py                # API module exports
│   └── client.py                  # HTTP client for Business Central APIs
├── auth/                          # Authentication
│   ├── __init__.py                # Auth module exports
│   └── manager.py                 # OAuth2 authentication management
├── models/                        # Data models
│   ├── __init__.py                # Models module exports
│   ├── business.py                # Business domain entities
│   └── responses.py               # API response structures
├── tools/                         # MCP tools
│   ├── __init__.py                # Tools module exports
│   └── implementations.py        # MCP tool implementations
└── config/                        # Configuration and utilities
    ├── __init__.py                # Config module exports
    ├── settings.py                # Configuration classes
    ├── exceptions.py              # Custom exception hierarchy
    ├── logging.py                 # Logging configuration
    └── utils.py                   # Utility functions
```

## Module Responsibilities

### Core (`core/`)
Contains the fundamental business logic and application orchestration:
- **server.py**: MCP server initialization and main application entry point
- **company_manager.py**: Business Central company discovery, selection, and management
- **dependencies.py**: Dependency injection container that wires up all components

### API (`api/`)
Handles all HTTP communication with Business Central:
- **client.py**: HTTP client with authentication, error handling, and request/response management

### Authentication (`auth/`)
Manages OAuth2 authentication with Azure AD:
- **manager.py**: Token acquisition, caching, and refresh logic

### Models (`models/`)
Contains all data structures and domain models:
- **business.py**: Business domain entities (Company, Resource, SchemaInfo)
- **responses.py**: API response structures and data transfer objects

### Tools (`tools/`)
Implements the MCP tool interface:
- **implementations.py**: All MCP tool implementations that provide the external API

### Configuration (`config/`)
Houses configuration, utilities, and cross-cutting concerns:
- **settings.py**: Configuration classes and environment variable loading
- **exceptions.py**: Custom exception hierarchy for structured error handling
- **logging.py**: Centralized logging configuration and utilities
- **utils.py**: General utility functions and validators

## Design Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- Core handles business logic
- API handles external communication
- Auth handles security
- Models define data structures
- Tools implement the external interface
- Config provides infrastructure

### 2. Dependency Injection
Components are loosely coupled and dependencies are injected through the `dependencies.py` module, making the system:
- Easily testable
- Modular and maintainable
- Scalable for different deployment scenarios

### 3. Layered Architecture
The architecture follows a clear layering pattern:
```
Tools Layer    -> MCP tool implementations
Core Layer     -> Business logic and orchestration
API Layer      -> External API communication
Config Layer   -> Infrastructure and utilities
```

### 4. Professional Naming
- Package name: `mcp_business_central` (follows MCP naming convention)
- Module names: descriptive and follow Python conventions
- Clear hierarchy with logical grouping

## Benefits of This Structure

### For Development
- **Clear ownership**: Each file has a specific purpose
- **Easy navigation**: Logical grouping makes finding code intuitive
- **Testability**: Modular design enables comprehensive unit testing
- **Maintainability**: Changes are isolated to specific modules

### For Deployment
- **Scalability**: Clean separation allows for distributed deployment
- **Configuration**: Centralized config management
- **Monitoring**: Structured logging and error handling
- **Performance**: Optimized imports and minimal coupling

### For Extension
- **New tools**: Add to `tools/implementations.py`
- **New APIs**: Extend `api/client.py` or add new clients
- **New models**: Add to appropriate model files
- **New utilities**: Add to `config/utils.py`

## Import Patterns

### Internal Imports
```python
# From child to parent module
from ..config import BCServerConfig
from ..models import Company

# From child to sibling module
from ..api import BCAPIClient
from ..auth import BCAuthManager
```

### External Imports
```python
# For tools that need dependencies
from ..core.dependencies import mcp, logger, api_client, company_manager
```

## Migration from Old Structure

The new structure maintains backward compatibility through legacy wrappers in `dependencies.py` while providing a clear migration path to the new architecture.

### Old vs New

| Old Structure | New Structure | Purpose |
|--------------|---------------|---------|
| `mcp_bc_server/` | `mcp_business_central/` | Professional package name |
| `config.py` | `config/settings.py` | Configuration management |
| `exceptions.py` | `config/exceptions.py` | Exception hierarchy |
| `logging.py` | `config/logging.py` | Logging infrastructure |
| `utils.py` | `config/utils.py` | Utility functions |
| `auth.py` | `auth/manager.py` | Authentication |
| `api_client.py` | `api/client.py` | API communication |
| `company_manager.py` | `core/company_manager.py` | Company management |
| `server.py` | `core/server.py` | Server setup |
| `tools.py` | `tools/implementations.py` | MCP tools |
| `models.py` | `models/business.py` + `models/responses.py` | Data models |
| `common.py` | `core/dependencies.py` | Dependency injection |

## Testing Strategy

The modular structure enables comprehensive testing:

```
tests/
├── unit/
│   ├── test_core/
│   ├── test_api/
│   ├── test_auth/
│   ├── test_models/
│   ├── test_tools/
│   └── test_config/
├── integration/
└── e2e/
```

Each module can be tested in isolation with mocked dependencies, and integration tests can verify the interaction between modules.
