# Architecture

## Design Principles

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Loosely coupled, testable components
- **Type Safety**: Full type hints throughout
- **No Global State**: Thread-safe, scalable design
- **Structured Logging**: Configurable logging with proper error handling

## Core Components

| Component | Purpose |
|-----------|---------|
| **config** | Environment-based configuration management |
| **auth** | OAuth2 token management with Azure AD |
| **api_client** | HTTP client for Business Central APIs |
| **company_manager** | Company discovery and context management |
| **models** | Data structures and response types |
| **exceptions** | Custom exception hierarchy |
| **tools** | MCP tool implementations |
| **utils** | Validation, sanitization, and utilities |

## Exception Hierarchy

```
BCServerError (base)
├── AuthenticationError
├── CompanyNotFoundError
├── ResourceNotFoundError
├── ValidationError
├── APIError
└── ConfigurationError
```

## SaaS Ready Features

### ✅ **Multi-Tenancy**
- No global state prevents data bleeding
- Isolated company context per request
- Multi-tenant token management

### ✅ **Scalability**
- Stateless design for horizontal scaling
- Efficient caching with proper invalidation
- HTTP connection pooling

### ✅ **Security**
- Secure token handling with auto-refresh
- Input validation and sanitization
- No sensitive data in logs

### ✅ **Observability**
- Structured logging for monitoring
- Request tracing and error tracking
- Configurable log levels

## Usage Pattern

```python
# Initialize components via dependency injection
from .common import config, auth_manager, api_client, company_manager

# Use components
companies = await company_manager.discover_companies()
await company_manager.set_active_company(company_id)
response = await api_client.request("GET", "items")
```

## Benefits

- **Thread-Safe**: Stateful components without global state
- **Testable**: Dependency injection enables comprehensive testing
- **Maintainable**: Clear separation of responsibilities
- **Deployable**: Centralized configuration management
