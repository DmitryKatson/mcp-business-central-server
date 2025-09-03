"""
MCP tools for Business Central integration.

This module contains all the MCP tool implementations for interacting with
Microsoft Dynamics 365 Business Central APIs.
"""

from typing import Dict, Any, Optional, Union

from ..core.dependencies import mcp, logger, api_client, company_manager
from ..config.exceptions import ValidationError, APIError, CompanyNotFoundError
from ..models import APIResponse, SchemaInfo
from ..config.utils import safe_int_convert, validate_resource_name, validate_field_name, build_odata_filter

@mcp.tool(name="list_companies", description="List all available companies in the Business Central environment.")
async def discover_companies_tool() -> Dict[str, Any]:
    """Discover all available companies in Business Central."""
    logger.info("Tool 'list_companies' called")
    
    try:
        companies = await company_manager.discover_companies()
        companies_data = [
            {
                "id": company.id,
                "name": company.name,
                "displayName": company.display_name,
                "businessProfileId": company.business_profile_id
            }
            for company in companies
        ]
        
        response = APIResponse.success_response(
            {"companies": companies_data, "message": f"Found {len(companies)} companies"},
            count=len(companies)
        )
        return response.to_dict()
        
    except Exception as e:
        logger.error(f"Error discovering companies: {e}")
        return APIResponse.error_response(str(e)).to_dict()

@mcp.tool(name="set_active_company", description="Set the active company for subsequent Business Central operations.")
async def set_company_tool(company_id: str) -> Dict[str, Any]:
    """Set the active company for Business Central operations."""
    logger.info(f"Tool 'set_active_company' called with company_id={company_id}")
    
    try:
        company = await company_manager.set_active_company(company_id)
        response = APIResponse.success_response({
                    "company_id": company_id,
            "company_name": company.name,
                    "message": "Company set successfully"
        })
        return response.to_dict()
        
    except CompanyNotFoundError as e:
        logger.error(f"Company not found: {e}")
        return APIResponse.error_response(str(e)).to_dict()
    except Exception as e:
        logger.error(f"Error setting company: {e}")
        return APIResponse.error_response(str(e)).to_dict()

@mcp.tool(name="get_active_company", description="Get information about the currently active company.")
async def get_active_company_tool() -> Dict[str, Any]:
    """Get the currently active company information."""
    logger.info("Tool 'get_active_company' called")
    
    try:
        company = await company_manager.get_active_company()
        if not company:
            return APIResponse.error_response("No active company set").to_dict()
        
        response = APIResponse.success_response({
            "active_company": {
                "id": company.id,
                "name": company.name,
                "displayName": company.display_name,
                "businessProfileId": company.business_profile_id
            },
            "company_id": company.id
        })
        return response.to_dict()
            
    except Exception as e:
        logger.error(f"Error getting active company: {e}")
        return APIResponse.error_response(str(e)).to_dict()



@mcp.tool(name="get_resource_schema", description="Get schema information and available fields for a Business Central resource.")
async def get_schema_tool(resource: str, company_id: Optional[str] = None) -> Dict[str, Any]:
    """Get schema information for a Business Central resource."""
    logger.info(f"Tool 'get_resource_schema' called for resource={resource}")
    
    try:
        # Validate inputs
        resource = validate_resource_name(resource)
        
        if not company_id:
            company_id = await company_manager.get_active_company_id()
        
        logger.info(f"Getting schema for resource: {resource}")
        
        # Get a sample record to determine schema
        result = await api_client.request("GET", resource, params={'$top': 1}, company_id=company_id)
        
        fields = []
        sample_item = {}
        
        if result.get('value') and len(result['value']) > 0:
            sample_item = result['value'][0]
            fields = list(sample_item.keys())
            logger.info(f"Found {len(fields)} fields in schema")
        else:
            logger.warning(f"No sample data found for resource {resource}")
        
        schema_info = SchemaInfo(
            resource=resource,
            fields=fields,
            sample_item=sample_item,
            company_id=company_id
        )
        
        response = APIResponse.success_response({
            "resource": schema_info.resource,
            "available_fields": schema_info.fields,
            "field_count": schema_info.field_count,
            "sample_item": schema_info.sample_item,
            "company_id": schema_info.company_id,
            "has_data": schema_info.has_data
        })
        return response.to_dict()
        
    except ValidationError as e:
        logger.error(f"Validation error in get_resource_schema: {e}")
        return APIResponse.error_response(f"Parameter validation error: {str(e)}").to_dict()
    except APIError as e:
        logger.error(f"API error in get_resource_schema: {e}")
        return APIResponse.error_response(str(e)).to_dict()
    except Exception as e:
        logger.error(f"Unexpected error in get_resource_schema: {e}")
        return APIResponse.error_response(f"Unexpected error: {str(e)}").to_dict()

@mcp.tool(name="list_records", description="List records from a Business Central resource with optional filtering and pagination.")
async def list_items_tool(resource: str, filter: Optional[str] = None, top: Optional[Union[str, int]] = None, 
                         skip: Optional[Union[str, int]] = None, company_id: Optional[str] = None) -> Dict[str, Any]:
    """List items from a Business Central resource."""
    logger.info(f"Tool 'list_records' called for resource={resource}, filter={filter}, top={top}, skip={skip}")
    
    try:
        # Validate and normalize inputs
        resource = validate_resource_name(resource)
        
        if not company_id:
            company_id = await company_manager.get_active_company_id()
        
        # Convert string parameters to proper types
        top_int = safe_int_convert(top)
        skip_int = safe_int_convert(skip)
        
        logger.debug(f"Converted parameters - top: {top_int}, skip: {skip_int}")
        
        # Build parameters dictionary
        params = {}
        if filter is not None:
            params['$filter'] = filter
        if top_int is not None:
            params['$top'] = top_int
        if skip_int is not None:
            params['$skip'] = skip_int
        
        logger.debug(f"Final request parameters: {params}")
        
        result = await api_client.request("GET", resource, params=params, company_id=company_id)
        
        # Add metadata to response
        if isinstance(result, dict) and 'value' in result:
            result['_metadata'] = {
                "company_id": company_id,
                "request_params": {
                "resource": resource,
                "filter": filter,
                "top": top_int,
                    "skip": skip_int
                }
            }
        
        response = APIResponse.success_response(result)
        return response.to_dict()
        
    except ValidationError as e:
        logger.error(f"Validation error in list_records: {e}")
        return APIResponse.error_response(f"Parameter validation error: {str(e)}").to_dict()
    except APIError as e:
        logger.error(f"API error in list_records: {e}")
        return APIResponse.error_response(str(e)).to_dict()
    except Exception as e:
        logger.error(f"Unexpected error in list_records: {e}")
        return APIResponse.error_response(f"Unexpected error: {str(e)}").to_dict()

@mcp.tool(name="find_records_by_field", description="Find records where a specific field matches a given value.")
async def get_items_by_field_tool(resource: str, field: str, value: str, 
                                 company_id: Optional[str] = None) -> Dict[str, Any]:
    """Get items from Business Central by field value."""
    logger.info(f"Tool 'find_records_by_field' called for resource={resource}, field={field}, value={value}")
    
    try:
        # Validate inputs
        resource = validate_resource_name(resource)
        field = validate_field_name(field)
        
        if value is None:
            raise ValidationError("Value cannot be None")
        
        # Build OData filter using utility function
        filter_expr = build_odata_filter(field, value)
        
        logger.debug(f"Built filter expression: {filter_expr}")
        
        return await list_items_tool(resource, filter=filter_expr, company_id=company_id)
        
    except ValidationError as e:
        logger.error(f"Validation error in find_records_by_field: {e}")
        return APIResponse.error_response(f"Parameter validation error: {str(e)}").to_dict()
    except Exception as e:
        logger.error(f"Unexpected error in find_records_by_field: {e}")
        return APIResponse.error_response(f"Unexpected error: {str(e)}").to_dict()

@mcp.tool(name="get_record_by_id", description="Get a specific record by its unique identifier.")
async def get_item_by_id_tool(resource: str, item_id: str, 
                             company_id: Optional[str] = None) -> Dict[str, Any]:
    """Get a specific item by ID from Business Central."""
    logger.info(f"Tool 'get_record_by_id' called for resource={resource}, item_id={item_id}")
    
    try:
        resource = validate_resource_name(resource)
        
        if not company_id:
            company_id = await company_manager.get_active_company_id()
        
        result = await api_client.request("GET", resource, item_id=item_id, company_id=company_id)
        
        # Add metadata
        if isinstance(result, dict):
            result['_metadata'] = {"company_id": company_id}
        
        response = APIResponse.success_response(result)
        return response.to_dict()
        
    except ValidationError as e:
        logger.error(f"Validation error in get_record_by_id: {e}")
        return APIResponse.error_response(f"Parameter validation error: {str(e)}").to_dict()
    except APIError as e:
        logger.error(f"API error in get_record_by_id: {e}")
        return APIResponse.error_response(str(e)).to_dict()
    except Exception as e:
        logger.error(f"Unexpected error in get_record_by_id: {e}")
        return APIResponse.error_response(f"Unexpected error: {str(e)}").to_dict()