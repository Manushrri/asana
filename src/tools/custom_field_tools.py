"""
Asana Custom Field Tools
"""

from typing import Optional, List, Dict, Any


def get_custom_field(
    client,
    custom_field_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get a single custom field by its globally unique identifier."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/custom_fields/{custom_field_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_custom_fields_for_workspace(
    client,
    workspace_gid: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get all custom fields in a workspace."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or omit to use your default workspace)."}

        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/workspaces/{workspace_gid}/custom_fields", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_custom_field(
    client,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a new custom field in a workspace. Use when you need to define a new field for tracking specific information within Asana tasks."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            "/custom_fields",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_enum_option_for_custom_field(
    client,
    custom_field_gid: str,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a new enum option for a custom field in Asana. Use this when you need to add a new selectable option to an existing custom field."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/custom_fields/{custom_field_gid}/enum_options",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def insert_enum_option_for_custom_field(
    client,
    custom_field_gid: str,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Reorder an existing enum option within a custom field by moving it before or after another specified enum option."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/custom_fields/{custom_field_gid}/enum_options/insert",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "custom_field_gid": custom_field_gid,
                "enum_option_moved": data.get("enum_option"),
                "before_enum_option": data.get("before_enum_option"),
                "after_enum_option": data.get("after_enum_option"),
                "message": "Enum option reordered.",
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_custom_field(
    client,
    custom_field_gid: str,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Update a custom field by its globally unique identifier. Use when you need to modify properties of an existing custom field in Asana."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.put(
            f"/custom_fields/{custom_field_gid}",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_enum_option(
    client,
    enum_option_gid: str,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Update an enum option for a custom field. Use when you need to modify the name, color, or enabled status of an existing enum option."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.put(
            f"/enum_options/{enum_option_gid}",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_custom_field(
    client,
    custom_field_gid: str
) -> dict:
    """Delete a custom field by its globally unique identifier."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        result = client.delete(f"/custom_fields/{custom_field_gid}")
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

