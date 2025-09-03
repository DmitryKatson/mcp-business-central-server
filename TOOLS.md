# Business Central MCP Tools

This document describes all available MCP tools for interacting with Microsoft Dynamics 365 Business Central.

## Tool Overview

All tools have been renamed to use clean, self-explanatory names that follow natural language patterns. The naming convention uses simple verbs and nouns that clearly indicate the tool's purpose.

## Company Management Tools

### `list_companies`
**Description:** List all available companies in the Business Central environment.

**Parameters:** None

**Returns:** 
- List of companies with their IDs, names, display names, and business profile IDs
- Total count of discovered companies

**Example:**
```json
{
  "success": true,
  "count": 2,
  "data": {
    "companies": [
      {
        "id": "12345-6789-...",
        "name": "CRONUS International Ltd.",
        "displayName": "CRONUS International Ltd.",
        "businessProfileId": "..."
      }
    ],
    "message": "Found 2 companies"
  }
}
```

---

### `set_active_company`
**Description:** Set the active company for subsequent Business Central operations.

**Parameters:**
- `company_id` (string, required): The unique identifier of the company to set as active

**Returns:** 
- Confirmation of the company selection
- Company ID and name

**Example:**
```json
{
  "success": true,
  "data": {
    "company_id": "12345-6789-...",
    "company_name": "CRONUS International Ltd.",
    "message": "Company set successfully"
  }
}
```

---

### `get_active_company`
**Description:** Get information about the currently active company.

**Parameters:** None

**Returns:** 
- Active company details including ID, name, and display name

**Example:**
```json
{
  "success": true,
  "data": {
    "active_company": {
      "id": "12345-6789-...",
      "name": "CRONUS International Ltd.",
      "displayName": "CRONUS International Ltd.",
      "businessProfileId": "..."
    },
    "company_id": "12345-6789-..."
  }
}
```

## Data Access Tools

### `get_resource_schema`
**Description:** Get schema information and available fields for a Business Central resource.

**Parameters:**
- `resource` (string, required): The name of the Business Central resource (e.g., "items", "customers", "salesOrders")
- `company_id` (string, optional): Company ID to use (defaults to active company)

**Returns:** 
- List of available fields
- Sample data item (if available)
- Field count and metadata

**Example:**
```json
{
  "success": true,
  "data": {
    "resource": "items",
    "available_fields": ["id", "number", "displayName", "type", "blocked", "baseUnitOfMeasure"],
    "field_count": 6,
    "sample_item": {
      "id": "...",
      "number": "1000",
      "displayName": "Bicycle"
    },
    "company_id": "12345-6789-...",
    "has_data": true
  }
}
```

---

### `list_records`
**Description:** List records from a Business Central resource with optional filtering and pagination.

**Parameters:**
- `resource` (string, required): The name of the Business Central resource
- `filter` (string, optional): OData filter expression (e.g., "blocked eq false")
- `top` (integer, optional): Maximum number of records to return
- `skip` (integer, optional): Number of records to skip (for pagination)
- `company_id` (string, optional): Company ID to use (defaults to active company)

**Returns:** 
- Array of records matching the criteria
- Metadata about the request

**Example:**
```json
{
  "success": true,
  "count": 10,
  "data": {
    "value": [
      {
        "id": "...",
        "number": "1000",
        "displayName": "Bicycle",
        "type": "Inventory"
      }
    ],
    "_metadata": {
      "company_id": "12345-6789-...",
      "request_params": {
        "resource": "items",
        "filter": "blocked eq false",
        "top": 10,
        "skip": 0
      }
    }
  }
}
```

---

### `find_records_by_field`
**Description:** Find records where a specific field matches a given value.

**Parameters:**
- `resource` (string, required): The name of the Business Central resource
- `field` (string, required): The field name to search in
- `value` (string, required): The value to search for
- `company_id` (string, optional): Company ID to use (defaults to active company)

**Returns:** 
- Array of records where the field matches the value

**Example:**
```json
{
  "success": true,
  "count": 1,
  "data": {
    "value": [
      {
        "id": "...",
        "number": "1000",
        "displayName": "Bicycle",
        "type": "Inventory"
      }
    ]
  }
}
```

---

### `get_record_by_id`
**Description:** Get a specific record by its unique identifier.

**Parameters:**
- `resource` (string, required): The name of the Business Central resource
- `item_id` (string, required): The unique identifier of the record
- `company_id` (string, optional): Company ID to use (defaults to active company)

**Returns:** 
- The specific record with all its fields

**Example:**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "number": "1000",
    "displayName": "Bicycle",
    "type": "Inventory",
    "blocked": false,
    "baseUnitOfMeasure": {
      "code": "PCS",
      "displayName": "Piece"
    },
    "_metadata": {
      "company_id": "12345-6789-..."
    }
  }
}
```

## Common Business Central Resources

Here are some commonly used Business Central API resources you can work with:

### Master Data
- `items` - Inventory items
- `customers` - Customer records
- `vendors` - Vendor/supplier records
- `employees` - Employee records
- `accounts` - Chart of accounts

### Sales
- `salesOrders` - Sales orders
- `salesInvoices` - Sales invoices
- `salesQuotes` - Sales quotes
- `salesCreditMemos` - Sales credit memos

### Purchase
- `purchaseOrders` - Purchase orders
- `purchaseInvoices` - Purchase invoices
- `purchaseQuotes` - Purchase quotes

### Financial
- `generalLedgerEntries` - General ledger transactions
- `customerLedgerEntries` - Customer ledger entries
- `vendorLedgerEntries` - Vendor ledger entries
- `itemLedgerEntries` - Item ledger entries

## Error Handling

All tools return standardized responses with proper error handling:

### Success Response
```json
{
  "success": true,
  "count": 1,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

## Usage Tips

1. **Start with company management**: Always begin by listing companies and setting the active company
2. **Explore schemas first**: Use `get_resource_schema` to understand available fields before querying data
3. **Use filtering**: The `list_records` tool supports OData filtering for efficient data retrieval
4. **Pagination**: Use `top` and `skip` parameters for large datasets
5. **Field-specific searches**: Use `find_records_by_field` for quick lookups by specific criteria

## Tool Design Principles

The tools follow modern naming conventions and design principles:

- ✅ **Action-oriented**: Use clear verbs (list, get, set, find)
- ✅ **Self-explanatory**: Purpose is immediately clear from the name
- ✅ **Consistent**: Follow a uniform naming pattern across all tools
- ✅ **Natural**: Read like normal English phrases
- ✅ **Professional**: Follow industry best practices for API design
