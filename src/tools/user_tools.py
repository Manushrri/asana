"""
Asana User Tools
"""

from typing import Optional, List, Dict, Any


def get_favorites_for_user(
    client,
    user_gid: str,
    workspace: Optional[str] = None,
    resource_type: str = "",
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get a user's favorites within a specified workspace. Returns favorites ordered as they appear in the user's Asana sidebar. resource_type can be portfolio, project, tag, task, user, or project_template. Omit workspace to use your default workspace."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not user_gid:
            return {"successful": False, "data": {}, "error": "user_gid is required (use \"me\" for current user)."}
        if not workspace:
            workspace = getattr(client, "default_workspace_gid", None)
            if not workspace:
                return {"successful": False, "data": {}, "error": "workspace is required (or omit to use your default workspace, if configured)."}
        if not resource_type:
            return {"successful": False, "data": {}, "error": "resource_type is required."}

        params = {
            "workspace": workspace,
            "resource_type": resource_type,
        }
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/users/{user_gid}/favorites", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_multiple_users(
    client,
    workspace: Optional[str] = None,
    team: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Returns a list of users in an Asana workspace or organization, optionally filtered by workspace or team GID."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if workspace:
            params["workspace"] = workspace
        if team:
            params["team"] = team
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/users", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_user_for_workspace(
    client,
    workspace_gid: Optional[str] = None,
    user_gid: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get a user in a workspace or organization by their GID. Use when you need to retrieve details about a specific user within a workspace context. Omit workspace_gid to use default workspace; omit user_gid to use current user."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            workspace_gid = getattr(client, "default_workspace_gid", None)
        if not user_gid:
            user_gid = getattr(client, "current_user_gid", None)
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or omit to use your default workspace)."}
        if not user_gid:
            return {"successful": False, "data": {}, "error": "user_gid is required (or omit to use current user)."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/workspaces/{workspace_gid}/users/{user_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_a_user_task_list(
    client,
    user_task_list_gid: str,
    workspace: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get a single user task list by its globally unique identifier. Use when you need to retrieve information about a specific user's My Tasks list."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace:
            return {"successful": False, "data": {}, "error": "workspace is required (or omit to use your default workspace)."}

        params = {"workspace": workspace}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/user_task_lists/{user_task_list_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_user_task_list_for_user(
    client,
    user_gid: Optional[str] = None,
    workspace: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get a user's My Tasks list for a workspace. Returns the user task list object (includes gid). Use this to get user_task_list_gid for GET_TASKS_FOR_USER_TASK_LIST or GET_A_USER_TASK_LIST. user_gid and workspace are optional (default to current user and default workspace)."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not user_gid:
            user_gid = getattr(client, "current_user_gid", None) or "me"
        if not workspace:
            workspace = getattr(client, "default_workspace_gid", None)
        if not workspace:
            return {"successful": False, "data": {}, "error": "workspace is required (or omit to use default workspace)."}

        params: Dict[str, Any] = {"workspace": workspace}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/users/{user_gid}/user_task_list", params=params)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_users_for_team(
    client,
    team_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get users in a team."""
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

        result = client.get(f"/teams/{team_gid}/users", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_users_for_workspace(
    client,
    workspace_gid: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get users in a workspace or organization."""
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

        result = client.get(f"/workspaces/{workspace_gid}/users", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_current_user(client) -> dict:
    """Get the current authenticated user's profile including name, email, GID, and workspaces."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        result = client.get("/users/me")
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_user(
    client,
    user_gid: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get a user by their ID. If user_gid is omitted, returns the current user."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not user_gid:
            return {"successful": False, "data": {}, "error": "user_gid is required (or omit for current user; ensure you are authenticated)."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/users/{user_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_user(
    client,
    user_gid: str,
    workspace: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Update a user's custom fields. Asana's API has limited user update capabilities; most properties are read-only. Get user_gid from GET_CURRENT_USER or GET_MULTIPLE_USERS. Get workspace from GET_CURRENT_USER or GET_MULTIPLE_WORKSPACES when updating workspace-scoped custom fields."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not user_gid:
            return {"successful": False, "data": {}, "error": "user_gid is required."}

        data: Dict[str, Any] = {}
        if custom_fields is not None:
            data["custom_fields"] = custom_fields

        params: Dict[str, Any] = {}
        if workspace:
            params["workspace"] = workspace
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.put(f"/users/{user_gid}", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_user_for_workspace(
    client,
    workspace_gid: Optional[str] = None,
    user_gid: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Update a user in a workspace (e.g. user custom field values). Omit workspace_gid to use default workspace; omit user_gid to use current user. You must pass custom_fields: an object with custom field GID as key and value to set (e.g. {\"CUSTOM_FIELD_GID\": \"text\" or number or enum_option_gid}). Get workspace_gid from GET_CURRENT_USER or GET_MULTIPLE_WORKSPACES; user_gid from GET_CURRENT_USER or GET_MULTIPLE_USERS; custom field GIDs from GET_CUSTOM_FIELDS_FOR_WORKSPACE."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            workspace_gid = getattr(client, "default_workspace_gid", None)
        if not user_gid:
            user_gid = getattr(client, "current_user_gid", None)
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or omit to use default workspace)."}
        if not user_gid:
            return {"successful": False, "data": {}, "error": "user_gid is required (or omit to use current user)."}
        if not custom_fields:
            return {"successful": False, "data": {}, "error": "custom_fields is required: object with custom field GID as key and value to set (e.g. {\"1213390201360126\": \"value\"}). Get custom field GIDs from GET_CUSTOM_FIELDS_FOR_WORKSPACE."}

        data: Dict[str, Any] = {}
        if custom_fields is not None:
            data["custom_fields"] = custom_fields

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.put(
            f"/workspaces/{workspace_gid}/users/{user_gid}",
            json={"data": data},
            params=params if params else None,
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

