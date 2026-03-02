"""
Asana Membership Tools
"""

from typing import Optional, List


def get_membership(
    client,
    membership_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve a single membership by its ID. Use this when you need to get details about a specific membership relationship between a user/team and a goal, project, portfolio, or custom field."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not membership_gid:
            return {"successful": False, "data": {}, "error": "membership_gid is required."}

        params = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/memberships/{membership_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_membership(
    client,
    membership_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Delete a membership by its GID. Use when you need to remove a user or team's access to a project, portfolio, goal, or custom field. Get membership_gid from GET_MEMBERSHIP, GET_MEMBERSHIPS, GET_PROJECT_MEMBERSHIPS_FOR_PROJECT, or GET_PORTFOLIO_MEMBERSHIPS."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not membership_gid:
            return {"successful": False, "data": {}, "error": "membership_gid is required."}

        params = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.delete(f"/memberships/{membership_gid}", params=params if params else None)
        data = result.get("data", {})
        if data == {}:
            data = {"message": "Membership deleted.", "membership_gid": membership_gid}
        return {"successful": True, "data": data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_membership(
    client,
    member: str,
    parent: str,
    role: Optional[str] = None,
    access_level: Optional[str] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a membership by adding a user or team to a project, goal, or portfolio. Use when you need to grant access to an Asana resource. Get member GID (user or team) from GET_MULTIPLE_USERS, GET_USERS_FOR_WORKSPACE, or GET_TEAMS_IN_WORKSPACE. Get parent GID (project, goal, or portfolio) from GET_A_PROJECT, GET_GOALS, or GET_PORTFOLIO."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not member:
            return {"successful": False, "data": {}, "error": "member (user or team GID) is required."}
        if not parent:
            return {"successful": False, "data": {}, "error": "parent (project, goal, or portfolio GID) is required."}

        data = {"member": member, "parent": parent}
        if role:
            data["role"] = role
        if access_level:
            data["access_level"] = access_level

        params = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post("/memberships", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_memberships(
    client,
    parent: Optional[str] = None,
    member: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[str] = None
) -> dict:
    """Retrieve memberships for goals, projects, portfolios, or custom fields."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if parent:
            params["parent"] = parent
        if member:
            params["member"] = member
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = opt_fields

        result = client.get("/memberships", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_portfolio_memberships(
    client,
    portfolio: Optional[str] = None,
    user: Optional[str] = None,
    workspace: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None
) -> dict:
    """Retrieve multiple portfolio memberships. List memberships for a specific portfolio, a user within a portfolio, or a user across all portfolios in a workspace."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if portfolio:
            params["portfolio"] = portfolio
        if user:
            params["user"] = user
        if workspace:
            params["workspace"] = workspace
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)

        result = client.get("/portfolio_memberships", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

