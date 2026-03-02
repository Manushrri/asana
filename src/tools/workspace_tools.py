"""
Asana Workspace Tools
"""

from typing import Optional, List


def add_user_for_workspace(
    client,
    workspace_gid: Optional[str] = None,
    user: str = "",
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add a user to a workspace or organization. user can be a user GID, an email address, or \"me\" for the current user.
    Get workspace_gid from GET_CURRENT_USER (workspaces field) or GET_MULTIPLE_WORKSPACES, or omit it to use your default workspace.
    Get user GID from GET_MULTIPLE_USERS or GET_USERS_FOR_WORKSPACE."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            return {
                "successful": False,
                "data": {},
                "error": "workspace_gid is required (or omit to use your default workspace, if configured).",
            }
        if not user:
            return {"successful": False, "data": {}, "error": "user (GID, email, or \"me\") is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        data = {"user": user}
        result = client.post(f"/workspaces/{workspace_gid}/addUser", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def remove_user_for_workspace(
    client,
    workspace_gid: Optional[str] = None,
    user: Optional[str] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Remove a user from a workspace or organization. Omit workspace_gid to use default workspace; omit user to use current user. Get workspace_gid from GET_CURRENT_USER (workspaces field) or GET_MULTIPLE_WORKSPACES. user can be a user GID, an email address, or \"me\" for the current user."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            workspace_gid = getattr(client, "default_workspace_gid", None)
        if not user:
            user = getattr(client, "current_user_gid", None) or "me"
        if not workspace_gid:
            return {
                "successful": False,
                "data": {},
                "error": "workspace_gid is required (or omit to use your default workspace, if configured).",
            }
        if not user:
            return {"successful": False, "data": {}, "error": "user (GID, email, or \"me\") is required (or omit to use current user)."}

        params = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        data = {"user": user}
        result = client.post(f"/workspaces/{workspace_gid}/removeUser", json={"data": data}, params=params if params else None)
        response_data = result.get("data", {})
        if response_data == {}:
            response_data = {"message": "User removed from workspace.", "workspace_gid": workspace_gid, "user": user}
        return {"successful": True, "data": response_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_typeahead_objects(
    client,
    workspace_gid: Optional[str] = None,
    resource_type: Optional[str] = None,
    query: Optional[str] = None,
    count: Optional[int] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve objects in a workspace via a typeahead search algorithm. Useful for auto-completion features."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or omit to use your default workspace)."}

        params = {}
        if resource_type:
            params["resource_type"] = resource_type
        if query:
            params["query"] = query
        if count is not None:
            params["count"] = count
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/workspaces/{workspace_gid}/typeahead", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_workspace(
    client,
    workspace_gid: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve details of a specific workspace by its GID."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or omit to use your default workspace)."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/workspaces/{workspace_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_workspace_memberships(
    client,
    workspace_gid: Optional[str] = None,
    user: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None
) -> dict:
    """Retrieve the workspace memberships for a specific workspace."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or omit to use your default workspace)."}

        params = {}
        if user:
            params["user"] = user
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)

        result = client.get(f"/workspaces/{workspace_gid}/workspace_memberships", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_workspace_membership(
    client,
    workspace_membership_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve a specific workspace membership by its GID. Use when you need to get details about a user's membership in a workspace. Get workspace_membership_gid from GET_WORKSPACE_MEMBERSHIPS or GET_WORKSPACE_MEMBERSHIPS_FOR_USER."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_membership_gid:
            return {"successful": False, "data": {}, "error": "workspace_membership_gid is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(
            f"/workspace_memberships/{workspace_membership_gid}",
            params=params if params else None,
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_workspace_memberships_for_user(
    client,
    user_gid: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve workspace memberships for a specific user. Use when you need to list all workspaces a user is a member of. Omit user_gid to use the current user. Get user_gid from GET_CURRENT_USER or GET_MULTIPLE_USERS."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not user_gid:
            user_gid = getattr(client, "current_user_gid", None)
        if not user_gid:
            return {"successful": False, "data": {}, "error": "user_gid is required (or omit to use current user)."}

        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(
            f"/users/{user_gid}/workspace_memberships",
            params=params if params else None,
        )
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_workspace_projects(
    client,
    workspace_gid: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_expand: Optional[List[str]] = None
) -> dict:
    """Retrieve the projects associated with a specific workspace."""
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
        if opt_expand:
            params["opt_expand"] = ",".join(opt_expand)

        result = client.get(f"/workspaces/{workspace_gid}/projects", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_multiple_workspaces(
    client,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieves all workspaces accessible by the authenticated user."""
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

        result = client.get("/workspaces", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

