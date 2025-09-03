# Business Central MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A modern MCP Server for seamless integration with Microsoft Dynamics 365 Business Central using OAuth2 authentication and API v2.0 endpoints. Features automatic company discovery and supports any entity in your Business Central environment. Developed by [Dmitry Katson](https://github.com/DmitryKatson), Microsoft AI & Business Central MVP.

## Features

This server provides a secure, modern interface to Business Central resources through the Model Context Protocol (MCP), with OAuth2 authentication and optimized API v2.0 endpoint handling.

### Key Capabilities

- **OAuth2 Authentication**: Secure authentication using Azure AD client credentials flow
- **API v2.0 Endpoints**: Uses the latest Business Central API v2.0 for optimal performance
- **Automatic Company Discovery**: Automatically discovers and lists available companies
- **Dynamic Company Selection**: Switch between companies without reconfiguration
- **Full CRUD Operations**: Create, read, update, and delete any Business Central entity
- **Action Execution**: Execute Business Central actions and procedures
- **Schema Discovery**: Automatically discover entity schemas and available fields

### Tools

The server implements the following tools:

- `list_companies`: Automatically discover all available companies in your Business Central environment
- `set_active_company`: Set the active company for subsequent operations
- `get_active_company`: Get information about the currently active company
- `get_resource_schema`: Retrieve the schema of any Business Central entity including available fields
- `list_records`: Fetch a list of entities with optional filtering and pagination
- `find_records_by_field`: Search for entities based on a specific field value
- `get_record_by_id`: Get a specific item by its unique identifier

## Working with Business Central Entities

This server can work with any entity (table) in Business Central. When using the tools, you must provide the exact entity name as it appears in Business Central API v2.0. For example:

- `employees`
- `customers`
- `items`
- `vendors`
- `salesOrders`
- `purchaseOrders`
- `generalLedgerEntries`

The entity name is case-sensitive and must match exactly what Business Central exposes through its API v2.0 endpoints.

## Prerequisites

### Azure AD App Registration

Before using this server, you need to register an application in Azure AD:

1. **Navigate to Azure Portal**: Go to [Azure Portal](https://portal.azure.com)
2. **Azure Active Directory**: Navigate to Azure Active Directory > App registrations
3. **New Registration**: Click "New registration" and provide:
   - **Name**: "Business Central MCP Server" (or your preferred name)
   - **Supported account types**: "Accounts in this organizational directory only"
   - **Redirect URI**: Leave blank for client credentials flow
4. **Create Application**: Click "Register"

### Configure API Permissions

After creating the app registration:

1. **API Permissions**: Go to "API permissions" in your app registration
2. **Add Permission**: Click "Add a permission"
3. **Microsoft APIs**: Choose "Dynamics 365 Business Central"
4. **Application Permissions**: Select "Application permissions"
5. **Select Permissions**: Choose:
   - `Financials.ReadWrite.All` (for full access)
   - Or `Financials.Read.All` (for read-only access)
6. **Grant Consent**: Click "Grant admin consent" and approve

### Create Client Secret

1. **Certificates & secrets**: Go to "Certificates & secrets"
2. **New Client Secret**: Click "New client secret"
3. **Description**: Provide a description (e.g., "MCP Server Secret")
4. **Expires**: Choose appropriate expiration (6 months, 12 months, or 24 months)
5. **Add**: Click "Add"
6. **Copy Secret**: **Important**: Copy the secret value immediately (it won't be shown again)

### Get Required Information

From your Azure AD app registration, collect:
- **Tenant ID**: Found in "Overview" section
- **Application (client) ID**: Found in "Overview" section  
- **Client Secret**: The secret value you copied above

## Environment Variables

The server requires these environment variables for OAuth2 authentication:

- `BC_TENANT_ID`: Your Azure AD tenant ID
- `BC_CLIENT_ID`: Your Azure AD application (client) ID
- `BC_CLIENT_SECRET`: Your Azure AD client secret
- `BC_ENVIRONMENT`: Your Business Central environment ('production' or 'sandbox', defaults to 'production')

### Example .env file

```bash
BC_TENANT_ID=12345678-1234-1234-1234-123456789012
BC_CLIENT_ID=87654321-4321-4321-4321-210987654321
BC_CLIENT_SECRET=your-client-secret-value-here
BC_ENVIRONMENT=production
```

## Architecture

The server is built with modern security and performance in mind:

- **OAuth2 Authentication**: Secure token-based authentication with Azure AD
- **API v2.0**: Uses the latest Business Central API endpoints
- **Automatic Company Discovery**: No need to hardcode company names
- **Async HTTP Client**: High-performance async requests using aiohttp
- **Token Caching**: Intelligent token caching with automatic refresh
- **Clean Architecture**: Separation of concerns with modular design

## Quickstart

### Installation

```bash
pip install -e .
```

Or install from PyPI once published:

```bash
pip install mcp-business-central-server
```

Using uv:

```bash
uv pip install mcp-business-central-server
```

### Claude Desktop Integration

To integrate with Claude Desktop, update the configuration file:

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`
On macOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

#### Standard Integration

```json
{
  "mcpServers": {
    "businesscentral": {
      "command": "mcp-business-central-server",
      "env": {
        "BC_TENANT_ID": "your-tenant-id",
        "BC_CLIENT_ID": "your-client-id",
        "BC_CLIENT_SECRET": "your-client-secret",
        "BC_ENVIRONMENT": "production"
      }
    }
  }
}
```

#### Using uvx

```json
{
  "mcpServers": {
    "businesscentral": {
      "command": "uvx",
      "args": [
        "mcp-business-central-server"
      ],
      "env": {
        "BC_TENANT_ID": "your-tenant-id",
        "BC_CLIENT_ID": "your-client-id", 
        "BC_CLIENT_SECRET": "your-client-secret",
        "BC_ENVIRONMENT": "production"
      }
    }
  }
}
```

## Usage Examples

### Company Discovery and Selection

```python
# Discover available companies
companies = await discover_companies_tool()

# Set active company
await set_company_tool("company-id-here")

# Get current active company
active_company = await get_active_company_tool()
```

### Working with Entities

```python
# Get customer schema
schema = await get_schema_tool("customers")

# List all customers
customers = await list_items_tool("customers")

# List customers with pagination (parameters can be strings or integers)
customers_page = await list_items_tool("customers", top="50", skip="0")
# or
customers_page = await list_items_tool("customers", top=50, skip=0)

# Get customers by city
customers_in_seattle = await get_items_by_field_tool("customers", "city", "Seattle")

# List customers with filtering
filtered_customers = await list_items_tool("customers", filter="city eq 'Seattle'")

# Create a new customer
new_customer = await create_item_tool("customers", {
    "displayName": "Acme Corp",
    "email": "contact@acme.com",
    "phoneNumber": "+1-555-0123"
})

# Update customer
await update_item_tool("customers", "customer-id", {"phoneNumber": "+1-555-0124"})
```

### MCP Tool Call Examples

Here are practical examples of how to call the tools through MCP:

#### Basic Customer Listing
```json
{
  "tool": "list_records",
  "parameters": {
    "resource": "customers",
    "top": "10"
  }
}
```

#### Get Customer Schema
```json
{
  "tool": "get_resource_schema", 
  "parameters": {
    "resource": "customers"
  }
}
```

#### Find Customers by Field
```json
{
  "tool": "find_records_by_field",
  "parameters": {
    "resource": "customers",
    "field": "city", 
    "value": "Seattle"
  }
}
```

#### Company Discovery
```json
{
  "tool": "list_companies",
  "parameters": {}
}
```

### Common Business Central Entity Names

Use these exact entity names (case-sensitive) for the `resource` parameter:

**Core Entities** (Available in most Business Central environments):
- **Customers**: `customers`
- **Vendors**: `vendors` 
- **Items**: `items`
- **Employees**: `employees`
- **Sales Orders**: `salesOrders`
- **Purchase Orders**: `purchaseOrders`
- **Sales Invoices**: `salesInvoices`
- **Purchase Invoices**: `purchaseInvoices`
- **Accounts**: `accounts`
- **Company Information**: `companyInformation`
- **Units of Measure**: `unitsOfMeasure`
- **Payment Terms**: `paymentTerms`
- **Dimensions**: `dimensions`
- **Dimension Values**: `dimensionValues`

**Advanced Entities** (May not be available in all environments):
- **General Ledger Entries**: `generalLedgerEntries` ⚠️
- **Customer Ledger Entries**: Not available in API v2.0 (use `customers` with OData filters instead)
- **Vendor Ledger Entries**: Not available in API v2.0 (use `vendors` with OData filters instead) 
- **Item Ledger Entries**: Not available in API v2.0 (use `items` with related data instead)

**Note**: Resource availability varies by Business Central environment, version, and configuration. Use the `get_resource_schema` tool to check if a specific resource is available and see its fields.

### Resource Schema Information

The server provides schema information for Business Central resources to help you understand available fields and data types.

**Get schema for a specific resource:**
```json
{
  "tool": "get_resource_schema",
  "parameters": {
    "resource": "customers"
  }
}
```

**Alternative Approaches for Ledger Data**

Since `customerLedgerEntries` is not available in API v2.0, try:
```json
{
  "tool": "list_records",
  "parameters": {
    "resource": "customers",
    "filter": "balance ne 0"
  }
}
```

**Always check schemas before working with resources:**
```json
{
  "tool": "get_resource_schema",
  "parameters": {
    "resource": "items"
  }
}
```

### Parameter Guidelines

- **Strings**: Resource names, filters, field names, and values should be strings
- **Integers**: `top` and `skip` parameters accept both strings and integers (e.g., `"50"` or `50`)
- **Optional parameters**: All parameters except `resource` are optional in most tools
- **Company ID**: If not provided, uses the currently active company

## Development

### Requirements

- Python 3.10+
- Azure AD app registration with Business Central permissions
- Access to Microsoft Dynamics 365 Business Central

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e .
   ```
4. Set up Azure AD app registration (see Prerequisites above)
5. Create a `.env` file with your OAuth2 credentials:
   ```bash
   BC_TENANT_ID=your-tenant-id
   BC_CLIENT_ID=your-client-id
   BC_CLIENT_SECRET=your-client-secret
   BC_ENVIRONMENT=production
   ```
6. Run the server:
   ```bash
   python -m mcp_bc_server
   ```

### Debugging

For debugging the MCP server, you can use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx @modelcontextprotocol/inspector -- python -m mcp_bc_server
```

## Security Considerations

- **Client Secret Protection**: Never commit client secrets to version control
- **Token Management**: Access tokens are automatically cached and refreshed
- **Permissions**: Use least-privilege principle when assigning API permissions
- **Environment Isolation**: Use different app registrations for production and development

## Migration from v0.1.x

If you're upgrading from the basic authentication version:

1. **Remove old environment variables**: Remove `BC_USER`, `BC_PASS`, and `BC_COMPANY` 
2. **Set up Azure AD**: Follow the prerequisites section to create an app registration
3. **Update environment variables**: Use the new OAuth2 variables
4. **Update Claude Desktop config**: Use the new environment variable names
5. **Test company discovery**: Use the new company discovery tools

## Troubleshooting

### Authentication Issues

- Verify your tenant ID, client ID, and client secret are correct
- Ensure API permissions are granted and admin consent is provided
- Check that your Business Central environment name is correct

### API Access Issues

- Verify your app has the required Business Central permissions
- Ensure your Azure AD app has admin consent for the permissions
- Check the Business Central environment is accessible

### Company Discovery Issues

- Verify your user/app has access to the Business Central environment
- Check that companies exist in the specified environment
- Ensure the environment name ('production' or 'sandbox') is correct

### Parameter Type Issues

**Problem**: Getting "Parameter 'top' must be one of types [integer, null], got string"

**Solution**: The tools now accept both string and integer parameters. Use either:
```json
{"top": "50"}  // String (will be converted)
```
or
```json
{"top": 50}    // Integer (used directly)
```

### Common Error Messages

**"Resource name must be a non-empty string"**
- Ensure the `resource` parameter is provided and not empty
- Check for extra whitespace in the resource name

**"Parameter validation error"**
- Check that required parameters are provided
- Verify parameter types match expectations
- Review the tool documentation for correct parameter formats

**"No company available"**
- Run `list_companies` first to see available companies
- Use `set_active_company` to select a company if multiple are available
- Verify your Business Central environment has accessible companies

**"HTTP 401: Unauthorized"**
- Check your Azure AD app registration settings
- Verify client ID, tenant ID, and client secret are correct
- Ensure API permissions include Business Central access
- Check that admin consent has been granted

**"HTTP 404: Not Found"**
- Verify the resource name is correct (case-sensitive)
- Check that the entity exists in your Business Central environment
- Ensure you're using the correct API v2.0 entity names

## Author

**Dmitry Katson** - [GitHub](https://github.com/DmitryKatson) | [Website](https://katson.com)

💻 Microsoft AI & Business Central MVP  
🏆 Contribution Hero 2024  
👨‍💼 Architect, Developer, and Team Leader  
🌐 Creator of [CentralQ.ai](https://centralq.ai) - AI search for Business Central community  
🤖 Making BC smart with AI

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Dmitry Katson