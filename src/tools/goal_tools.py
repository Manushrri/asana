"""
Asana Goal Tools
"""

from typing import Optional, List, Dict, Any


def get_time_periods(
    client,
    workspace: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve time periods (quarters, fiscal years, etc.) for a workspace."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace:
            workspace = getattr(client, "default_workspace_gid", None)
        if not workspace:
            return {"successful": False, "data": {}, "error": "workspace is required (or set default workspace)."}

        params: Dict[str, Any] = {"workspace": workspace}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/time_periods", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_time_period(
    client,
    time_period_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve the full record for a single time period by its GID."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not time_period_gid:
            return {"successful": False, "data": {}, "error": "time_period_gid is required."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(
            f"/time_periods/{time_period_gid}",
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_goal(
    client,
    name: str,
    time_period_gid: str,
    workspace: Optional[str] = None,
    due_on: Optional[str] = None,
    start_on: Optional[str] = None,
    notes: Optional[str] = None,
    owner: Optional[str] = None,
    liked: Optional[bool] = None,
    team: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a new goal in an Asana workspace."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not name:
            return {"successful": False, "data": {}, "error": "name is required."}
        if not time_period_gid:
            return {"successful": False, "data": {}, "error": "time_period_gid is required."}

        data: Dict[str, Any] = {
            "name": name,
            "time_period": time_period_gid,
        }
        if workspace:
            data["workspace"] = workspace
        if due_on:
            data["due_on"] = due_on
        if start_on:
            data["start_on"] = start_on
        if notes is not None:
            data["notes"] = notes
        if owner:
            data["owner"] = owner
        if liked is not None:
            data["liked"] = liked
        if team:
            data["team"] = team

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            "/goals",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_supporting_relationship(
    client,
    goal_gid: str,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add a supporting relationship to a goal."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not goal_gid:
            return {"successful": False, "data": {}, "error": "goal_gid is required."}
        if not data:
            return {"successful": False, "data": {}, "error": "data is required (e.g. supporting_resource, contribution_weight)."}
        if isinstance(data, str):
            import json
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return {"successful": False, "data": {}, "error": "data must be a JSON object."}
        if not data.get("supporting_resource"):
            return {"successful": False, "data": {}, "error": "data.supporting_resource is required (project, task, portfolio, or goal GID)."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/goals/{goal_gid}/addSupportingRelationship",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_goal(
    client,
    goal_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve the full record for a single goal by its GID."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not goal_gid:
            return {"successful": False, "data": {}, "error": "goal_gid is required."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields) if isinstance(opt_fields, list) else opt_fields
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(
            f"/goals/{goal_gid}",
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_goals(
    client,
    workspace: Optional[str] = None,
    team: Optional[str] = None,
    portfolio: Optional[str] = None,
    project: Optional[str] = None,
    is_workspace_level: Optional[bool] = None,
    time_period: Optional[str] = None,
    archived: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve multiple goals. Requires at least one scope (workspace, team, portfolio, project, or time_period)."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params: Dict[str, Any] = {}
        if workspace:
            params["workspace"] = workspace
        if team:
            params["team"] = team
        if portfolio:
            params["portfolio"] = portfolio
        if project:
            params["project"] = project
        if is_workspace_level is not None:
            params["is_workspace_level"] = str(is_workspace_level).lower()
        if time_period:
            params["time_period"] = time_period
        if archived is not None:
            params["archived"] = str(archived).lower()
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/goals", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}
