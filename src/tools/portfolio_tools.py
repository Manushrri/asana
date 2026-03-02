"""
Asana Portfolio Tools
"""

from typing import Optional, List, Dict, Any


def get_portfolio(
    client,
    portfolio_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve the full record for a single portfolio by its GID."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/portfolios/{portfolio_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_portfolio_items(
    client,
    portfolio_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None
) -> dict:
    """Retrieve items in a portfolio. Get a list of projects or other portfolios contained within a specific portfolio."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)

        result = client.get(f"/portfolios/{portfolio_gid}/items", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_item_to_portfolio(
    client,
    portfolio_gid: str,
    item: str,
    insert_before: Optional[str] = None,
    insert_after: Optional[str] = None
) -> dict:
    """Add a project (or other supported item) to an Asana portfolio using the native addItem endpoint."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        data = {"item": item}
        if insert_before:
            data["insert_before"] = insert_before
        if insert_after:
            data["insert_after"] = insert_after

        result = client.post(f"/portfolios/{portfolio_gid}/addItem", json={"data": data})
        api_data = result.get("data")
        # Asana addItem often returns 200 with empty or non-object data; synthesize a concise summary.
        if not isinstance(api_data, dict) or not api_data:
            api_data = {"portfolio_gid": portfolio_gid, "item_added": item, "message": "Item added to portfolio."}
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def remove_item_from_portfolio(
    client,
    portfolio_gid: str,
    item: str,
    opt_fields: Optional[str] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Remove an item (e.g. a project) from an Asana portfolio."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = opt_fields
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        data = {"item": item}
        result = client.post(f"/portfolios/{portfolio_gid}/removeItem", json={"data": data}, params=params if params else None)
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {"portfolio_gid": portfolio_gid, "item_removed": item, "message": "Item removed from portfolio."}
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_portfolio(
    client,
    name: str,
    workspace: Optional[str] = None,
    color: Optional[str] = None,
    public: Optional[bool] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a new portfolio in an Asana workspace. Workspace defaults to current user's default if omitted."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace:
            return {"successful": False, "data": {}, "error": "workspace is required (or omit to use your default workspace)."}

        data = {
            "name": name,
            "workspace": workspace,
        }
        if color:
            data["color"] = color
        if public is not None:
            data["public"] = public

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post("/portfolios", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_portfolios(
    client,
    workspace: Optional[str] = None,
    owner: str = "me",
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None
) -> dict:
    """Retrieve multiple portfolios. List portfolios within a specific workspace, optionally filtered by owner."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace:
            return {"successful": False, "data": {}, "error": "workspace is required (or omit to use your default workspace)."}

        params = {
            "workspace": workspace,
            "owner": owner,
        }
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)

        result = client.get("/portfolios", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

