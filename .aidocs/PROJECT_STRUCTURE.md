# Project Structure

## Directory Layout

```
src/mcp_business_central/
├── __init__.py                 # Package entry point
├── __main__.py                 # CLI execution
├── core/                       # Business logic
│   ├── server.py              # MCP server setup
│   ├── company_manager.py     # Company management
│   └── dependencies.py        # Dependency injection
├── api/
│   └── client.py              # HTTP client for BC APIs
├── auth/
│   └── manager.py             # OAuth2 authentication
├── models/
│   ├── business.py            # Domain entities
│   └── responses.py           # API response structures
├── tools/
│   └── implementations.py    # MCP tool implementations
└── config/
    ├── settings.py            # Configuration classes
    ├── exceptions.py          # Custom exceptions
    ├── logging.py             # Logging setup
    └── utils.py               # Utility functions
```

## Module Responsibilities

| Module | Purpose |
|--------|---------|
| **core** | Business logic and orchestration |
| **api** | HTTP communication with Business Central |
| **auth** | OAuth2 authentication with Azure AD |
| **models** | Data structures and domain models |
| **tools** | MCP tool implementations |
| **config** | Configuration, exceptions, and utilities |

## Design Principles

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Loose coupling via `dependencies.py`
- **Layered Architecture**: Tools → Core → API → Config
- **Professional Naming**: Clear, descriptive module names

## Key Benefits

- ✅ **Easy Navigation**: Logical file organization
- ✅ **Testability**: Modular design enables unit testing
- ✅ **Maintainability**: Changes isolated to specific modules
- ✅ **Scalability**: Clean separation for distributed deployment
