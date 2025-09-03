# Business Central MCP Server Architecture

## Overview

The Business Central MCP Server has been redesigned with a clean, modular architecture that follows professional software development best practices. The codebase is now SaaS-ready, scalable, and maintainable.

## Architecture Principles

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Components are loosely coupled and easily testable
- **Error Handling**: Comprehensive exception hierarchy with proper error propagation
- **Type Safety**: Full type hints throughout the codebase
- **Scalability**: No global state, thread-safe design
- **Observability**: Structured logging with configurable levels

## Module Structure

### Core Modules

#### 1. `config.py` - Configuration Management
- `BCServerConfig`: Business Central connection configuration
- `LoggingConfig`: Logging configuration
- Environment variable loading and validation

#### 2. `exceptions.py` - Exception Hierarchy
- `BCServerError`: Base exception class
- `AuthenticationError`: Authentication failures
- `CompanyNotFoundError`: Company lookup failures
- `ResourceNotFoundError`: Resource lookup failures
- `ValidationError`: Input validation failures
- `APIError`: Business Central API errors
- `ConfigurationError`: Configuration issues

#### 3. `logging.py` - Logging Infrastructure
- Centralized logging configuration
- Support for console and file logging
- Configurable log levels and formats

#### 4. `auth.py` - Authentication Management
- `BCAuthManager`: OAuth2 token management
- Token caching with expiration handling
- Azure AD integration for service-to-service authentication

#### 5. `api_client.py` - API Client
- `BCAPIClient`: HTTP client for Business Central APIs
- Request/response handling with proper error mapping
- ETag support for PATCH/DELETE operations
- Structured logging of API calls

#### 6. `company_manager.py` - Company Management
- `CompanyManager`: Company discovery and selection
- Caching of company information
- Thread-safe company context management

#### 7. `models.py` - Data Models
- `Company`: Business Central company representation
- `APIResponse`: Standardized API response structure
- `Resource`: API resource representation
- `SchemaInfo`: Resource schema information

#### 8. `utils.py` - Utility Functions
- Input validation and sanitization
- Type conversion utilities
- OData filter building
- Security-conscious data sanitization

#### 9. `tools.py` - MCP Tool Implementations
- All MCP tool definitions
- Comprehensive error handling
- Input validation and sanitization
- Structured response formatting

#### 10. `common.py` - Dependency Injection Container
- Component initialization and wiring
- Legacy function wrappers for backward compatibility
- MCP server instance

## Key Improvements

### 1. Eliminated Global State
- **Before**: Global variables for tokens, company selection, caching
- **After**: Stateful components with proper lifecycle management
- **Benefit**: Thread-safe, testable, scalable for multi-tenant scenarios

### 2. Proper Error Handling
- **Before**: Basic error strings and generic exception handling
- **After**: Structured exception hierarchy with proper error context
- **Benefit**: Better debugging, proper error propagation, meaningful error messages

### 3. Type Safety
- **Before**: Minimal type hints, duck typing
- **After**: Comprehensive type annotations throughout
- **Benefit**: Better IDE support, fewer runtime errors, self-documenting code

### 4. Separation of Concerns
- **Before**: Mixed authentication, API calls, and business logic
- **After**: Clear separation between auth, API client, business logic, and tools
- **Benefit**: Easier testing, maintenance, and feature development

### 5. Configuration Management
- **Before**: Environment variables scattered throughout code
- **After**: Centralized configuration with validation
- **Benefit**: Better configuration management, easier deployment, validation

### 6. Logging Infrastructure
- **Before**: Basic logging with hardcoded file paths
- **After**: Configurable logging with structured output
- **Benefit**: Better observability, configurable log levels, multiple output targets

## SaaS Readiness Features

### Multi-Tenancy Support
- No global state prevents tenant data bleeding
- Company context is properly isolated per request
- Token management supports multiple tenants

### Scalability
- Stateless design allows horizontal scaling
- Efficient caching with proper cache invalidation
- Resource pooling for HTTP connections

### Observability
- Structured logging for monitoring and debugging
- Request tracing and performance metrics
- Error tracking and alerting support

### Security
- Secure token handling with automatic refresh
- Input validation and sanitization
- No sensitive data in logs

### Maintainability
- Clear module boundaries and interfaces
- Comprehensive documentation and type hints
- Testable components with dependency injection

## Usage Examples

### Basic Setup
```python
from mcp_bc_server.config import BCServerConfig
from mcp_bc_server.auth import BCAuthManager
from mcp_bc_server.api_client import BCAPIClient
from mcp_bc_server.company_manager import CompanyManager

# Load configuration
config = BCServerConfig.from_environment()

# Initialize components
auth_manager = BCAuthManager(config)
api_client = BCAPIClient(config, auth_manager)
company_manager = CompanyManager(api_client)

# Use the components
companies = await company_manager.discover_companies()
await company_manager.set_active_company(companies[0].id)
```

### Error Handling
```python
from mcp_bc_server.exceptions import CompanyNotFoundError, APIError

try:
    company = await company_manager.set_active_company("invalid-id")
except CompanyNotFoundError as e:
    logger.error(f"Company not found: {e}")
except APIError as e:
    logger.error(f"API error: {e}")
```

## Migration Guide

The refactored code maintains backward compatibility through legacy wrapper functions in `common.py`. However, new development should use the new architecture:

### Old Way (Deprecated)
```python
from .common import bc_request, discover_companies

companies = await discover_companies()
result = await bc_request("GET", "items")
```

### New Way (Recommended)
```python
from .common import company_manager, api_client

companies = await company_manager.discover_companies()
result = await api_client.request("GET", "items", company_id=company_id)
```

## Testing Strategy

The new architecture enables comprehensive testing:

1. **Unit Tests**: Each component can be tested in isolation
2. **Integration Tests**: Components can be tested together with mocked dependencies
3. **Mock Testing**: Dependency injection allows easy mocking
4. **Error Testing**: Exception hierarchy enables comprehensive error testing

## Future Enhancements

The clean architecture enables future improvements:

1. **Caching Layer**: Redis-based caching for better performance
2. **Rate Limiting**: API rate limiting and backoff strategies
3. **Metrics**: Prometheus metrics for monitoring
4. **Health Checks**: Health check endpoints for load balancers
5. **API Versioning**: Support for multiple Business Central API versions
6. **Batch Operations**: Bulk operations for better performance
