"""
Asana Team Tools
"""

from typing import Optional, List, Dict, Any


def get_team(
    client,
    team_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve details of a specific team by its GID."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/teams/{team_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_team_memberships(
    client,
    team: Optional[str] = None,
    user: Optional[str] = None,
    workspace: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve compact team membership records. List members of a team, teams a user belongs to, or all team memberships in a workspace."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if team:
            params["team"] = team
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
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/team_memberships", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_team_membership(
    client,
    team_membership_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve a complete team membership record by its GID. Get team_membership_gid from GET_TEAM_MEMBERSHIPS or GET_TEAM_MEMBERSHIPS_FOR_TEAM."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not team_membership_gid:
            return {"successful": False, "data": {}, "error": "team_membership_gid is required."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(
            f"/team_memberships/{team_membership_gid}",
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_teams_in_workspace(
    client,
    workspace_gid: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None
) -> dict:
    """Returns the compact records for all teams in the workspace visible to the authorized user."""
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

        result = client.get(f"/organizations/{workspace_gid}/teams", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_team(
    client,
    data: Dict[str, Any]
) -> dict:
    """Create a new team in an Asana workspace. Use when you need to establish a new team for collaboration."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        result = client.post("/teams", json={"data": data})
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_team(
    client,
    team_gid: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    organization: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Update details of an existing team. Use when you need to change a team's name, description, or organization."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if organization is not None:
            data["organization"] = organization

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.put(f"/teams/{team_gid}", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_user_for_team(
    client,
    team_gid: str,
    user: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add a user to a team. user can be user GID, email, or 'me' for current user. Get team_gid from GET_TEAMS_IN_WORKSPACE. Get user from GET_MULTIPLE_USERS or GET_USERS_FOR_WORKSPACE."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not team_gid:
            return {"successful": False, "data": {}, "error": "team_gid is required."}
        if not user:
            return {"successful": False, "data": {}, "error": "user (GID, email, or 'me') is required."}

        data: Dict[str, Any] = {"user": user}
        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/teams/{team_gid}/addUser",
            json={"data": data},
            params=params if params else None,
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def remove_user_for_team(
    client,
    team_gid: str,
    user: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Remove a user from a team. Use when you need to revoke team membership for a specific user. Get team_gid from GET_TEAMS_IN_WORKSPACE or GET_TEAM. Get user identifier from GET_CURRENT_USER or GET_MULTIPLE_USERS (user GID, email, or \"me\")."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not team_gid:
            return {"successful": False, "data": {}, "error": "team_gid is required."}
        if not user:
            return {"successful": False, "data": {}, "error": "user (GID, email, or \"me\") is required."}

        data: Dict[str, Any] = {"user": user}

        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/teams/{team_gid}/removeUser",
            json={"data": data},
            params=params if params else None,
        )
        response_data = result.get("data", {})
        if response_data == {}:
            response_data = {"message": "User removed from team.", "team_gid": team_gid, "user": user}
        return {"successful": True, "data": response_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}
