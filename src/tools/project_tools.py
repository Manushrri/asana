"""
Asana Project Tools
"""

import json
from datetime import date
from typing import Optional, List, Dict, Any


def add_followers_to_project(
    client,
    project_gid: str,
    followers: List[str],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add one or more users as followers to a project. Followers receive notifications when tasks are added. Get project_gid from GET_A_PROJECT, GET_MULTIPLE_PROJECTS, GET_WORKSPACE_PROJECTS, or GET_PROJECTS_FOR_TEAM. Get user GIDs from GET_CURRENT_USER, GET_MULTIPLE_USERS, or GET_USERS_FOR_WORKSPACE."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}
        follower_list = followers if isinstance(followers, list) else [f.strip() for f in str(followers).split(",") if f.strip()]
        if not follower_list:
            return {"successful": False, "data": {}, "error": "At least one follower (user GID) is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        data = {"followers": follower_list}
        result = client.post(f"/projects/{project_gid}/addFollowers", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def remove_followers_for_project(
    client,
    project_gid: str,
    followers: List[str],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Remove one or more users as followers from a project. Use when you need to stop users from receiving notifications about a project's activity. Get project_gid from GET_A_PROJECT, GET_MULTIPLE_PROJECTS, GET_WORKSPACE_PROJECTS, or GET_PROJECTS_FOR_TEAM. Get follower user GIDs from GET_CURRENT_USER, GET_MULTIPLE_USERS, or GET_USERS_FOR_WORKSPACE."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}
        follower_list = followers if isinstance(followers, list) else [f.strip() for f in str(followers).split(",") if f.strip()]
        if not follower_list:
            return {"successful": False, "data": {}, "error": "At least one follower (user GID) is required."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        data = {"followers": follower_list}
        result = client.post(
            f"/projects/{project_gid}/removeFollowers",
            json={"data": data},
            params=params if params else None,
        )
        response_data = result.get("data", {})
        if response_data == {}:
            response_data = {"message": "Followers removed from project.", "project_gid": project_gid, "followers": follower_list}
        return {"successful": True, "data": response_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_members_for_project(
    client,
    project_gid: str,
    members: List[str],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add one or more users as members to a project. Members can view and contribute. Get project_gid from GET_A_PROJECT, GET_MULTIPLE_PROJECTS, GET_WORKSPACE_PROJECTS, or GET_PROJECTS_FOR_TEAM. Get user GIDs from GET_CURRENT_USER, GET_MULTIPLE_USERS, or GET_USERS_FOR_WORKSPACE."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}
        member_list = members if isinstance(members, list) else [m.strip() for m in str(members).split(",") if m.strip()]
        if not member_list:
            return {"successful": False, "data": {}, "error": "At least one member (user GID) is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        data = {"members": member_list}
        result = client.post(f"/projects/{project_gid}/addMembers", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def remove_members_for_project(
    client,
    project_gid: str,
    members: List[str],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Remove one or more users as members from a project. Use when you need to revoke project membership while leaving the project itself intact. Get project_gid from GET_A_PROJECT, GET_MULTIPLE_PROJECTS, GET_WORKSPACE_PROJECTS, or GET_PROJECTS_FOR_TEAM. Get user GIDs for members from GET_CURRENT_USER, GET_MULTIPLE_USERS, or GET_USERS_FOR_WORKSPACE."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}
        member_list = members if isinstance(members, list) else [m.strip() for m in str(members).split(",") if m.strip()]
        if not member_list:
            return {"successful": False, "data": {}, "error": "At least one member (user GID) is required."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        data = {"members": member_list}
        result = client.post(
            f"/projects/{project_gid}/removeMembers",
            json={"data": data},
            params=params if params else None,
        )
        response_data = result.get("data", {})
        if response_data == {}:
            response_data = {"message": "Members removed from project.", "project_gid": project_gid, "members": member_list}
        return {"successful": True, "data": response_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_a_project(
    client,
    project_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieves a specific Asana project by its project_gid. Does not return tasks within the project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/projects/{project_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_project(
    client,
    workspace_gid: Optional[str] = None,
    name: str = "",
    team_gid: Optional[str] = None,
    color: Optional[str] = None,
    icon: Optional[str] = None,
    default_view: Optional[str] = None,
    notes: Optional[str] = None,
    archived: Optional[bool] = None,
    public: Optional[bool] = None,
    due_on: Optional[str] = None,
    start_on: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Creates a new Asana project in the specified workspace. Requires a workspace GID, and additionally a team GID if the workspace is an organization."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or omit to use your default workspace)."}
        if not name:
            return {"successful": False, "data": {}, "error": "name is required."}

        data = {
            "workspace": workspace_gid,
            "name": name,
        }
        if team_gid:
            data["team"] = team_gid
        if color:
            data["color"] = color
        if icon:
            data["icon"] = icon
        if default_view:
            data["default_view"] = default_view
        if notes:
            data["notes"] = notes
        if archived is not None:
            data["archived"] = archived
        if public is not None:
            data["public"] = public
        if due_on:
            data["due_on"] = due_on
        if start_on:
            data["start_on"] = start_on

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post("/projects", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_project_for_workspace(
    client,
    workspace_gid: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a project in a workspace. Use when you need to create a new project within a specific Asana workspace. Pass a data object with at least name; team is required when the workspace is an organization. Get workspace_gid from GET_CURRENT_USER (workspaces field) or GET_MULTIPLE_WORKSPACES, or omit to use your default workspace. data can include: name, team, color, icon, default_view, notes, archived, public, due_on, start_on."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or omit to use your default workspace, if configured)."}
        if data is None:
            return {"successful": False, "data": {}, "error": "data is required (must include at least name)."}
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return {"successful": False, "data": {}, "error": "data must be a JSON object or valid JSON string."}
        if not isinstance(data, dict):
            return {"successful": False, "data": {}, "error": "data must be an object."}
        payload = {**data, "workspace": workspace_gid}
        if not payload.get("name"):
            return {"successful": False, "data": {}, "error": "data.name is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post("/projects", json={"data": payload}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_project_for_team(
    client,
    team_gid: str,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a project in a team. The project is shared with the given team. Pass a data object with at least name. Get team_gid from GET_TEAMS_IN_WORKSPACE. data can include: name, color, icon, default_view, notes, archived, public, due_on, start_on."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not team_gid:
            return {"successful": False, "data": {}, "error": "team_gid is required."}
        if data is None:
            return {"successful": False, "data": {}, "error": "data is required (object with at least name)."}
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return {"successful": False, "data": {}, "error": "data must be a JSON object."}
        if not isinstance(data, dict):
            return {"successful": False, "data": {}, "error": "data must be an object."}
        if not data.get("name"):
            return {"successful": False, "data": {}, "error": "data.name is required."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/teams/{team_gid}/projects",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_multiple_projects(
    client,
    workspace: Optional[str] = None,
    team: Optional[str] = None,
    archived: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Returns a list of projects filtered by workspace or team (one required), with optional archived status filter, supporting pagination for large datasets."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        if not workspace and not team:
            return {"successful": False, "data": {}, "error": "Either workspace or team must be provided."}

        params = {}
        if workspace:
            params["workspace"] = workspace
        if team:
            params["team"] = team
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

        result = client.get("/projects", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_project_status_update(
    client,
    project_gid: str,
    title: str,
    text: str,
    status_type: str,
    color: str
) -> dict:
    """Create a new status update on a project. Use when you need to communicate the current status, progress, or any blockers related to a specific project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        data = {
            "parent": project_gid,
            "title": title,
            "text": text,
            "status_type": status_type,
            "color": color,
        }

        result = client.post("/status_updates", json={"data": data})
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_status_for_object(
    client,
    parent: str,
    text: str,
    status_type: str,
    title: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a status update on a project, portfolio, or goal. Use to communicate progress, blockers, or current state to all followers of an object."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not parent:
            return {"successful": False, "data": {}, "error": "parent (project, portfolio, or goal GID) is required."}
        if not text:
            return {"successful": False, "data": {}, "error": "text is required."}
        if not status_type:
            return {"successful": False, "data": {}, "error": "status_type is required."}

        data = {
            "parent": parent,
            "text": text,
            "status_type": status_type,
        }
        if title:
            data["title"] = title

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post("/status_updates", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_project_memberships(
    client,
    project: Optional[str] = None,
    user: Optional[str] = None,
    workspace: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve memberships from a project. Can also get memberships for a user across multiple projects or all projects in a workspace."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        if not project:
            return {"successful": False, "data": {}, "error": "project GID is required."}

        params = {}
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

        result = client.get(f"/projects/{project}/project_memberships", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_project_membership(
    client,
    project_membership_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get a project membership by ID. Use when you need to retrieve details of a specific project membership."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_membership_gid:
            return {"successful": False, "data": {}, "error": "project_membership_gid is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/project_memberships/{project_membership_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_project_memberships_for_project(
    client,
    project_gid: str,
    user: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get memberships from a specific project. Use when you need to see who has access to a project and their permission levels."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}

        params = {}
        if user:
            params["user"] = user
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/projects/{project_gid}/project_memberships", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_projects_for_team(
    client,
    team_gid: str,
    archived: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get a list of projects for a specific team in Asana."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
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

        result = client.get(f"/teams/{team_gid}/projects", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_task_counts_for_project(
    client,
    project_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get task count statistics for a project. Use when you need the number of tasks, completed tasks, incomplete tasks, and milestone counts for a specific project. Note: all fields are excluded by default — you must specify them in opt_fields to get any data."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}

        params = {}
        # Asana excludes all fields by default; use sensible defaults so callers get data without specifying opt_fields
        fields = opt_fields or ["num_tasks", "num_incomplete_tasks", "num_completed_tasks"]
        params["opt_fields"] = ",".join(fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/projects/{project_gid}/task_counts", params=params)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_project_status(
    client,
    project_status_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve the full record for a single project status by its GID."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/project_statuses/{project_status_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_project_status(
    client,
    project_status_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Delete a project status by its GID. Use when you need to remove a specific project status from Asana. Get project_status_gid from project status lists."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_status_gid:
            return {"successful": False, "data": {}, "error": "project_status_gid is required."}

        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.delete(f"/project_statuses/{project_status_gid}", params=params if params else None)
        data = result.get("data", {})
        if data == {}:
            data = {"message": "Project status deleted.", "project_status_gid": project_status_gid}
        return {"successful": True, "data": data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_status(
    client,
    status_update_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve the full record for a single status update by its GID. Works for project, portfolio, or goal status updates."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not status_update_gid:
            return {"successful": False, "data": {}, "error": "status_update_gid is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/status_updates/{status_update_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_status_update(
    client,
    status_update_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Delete a status update by its GID. Use when you need to remove a specific status update from Asana. Get status_update_gid from GET_PROJECT_STATUS_UPDATES or GET_STATUS_UPDATES."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not status_update_gid:
            return {"successful": False, "data": {}, "error": "status_update_gid is required."}

        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.delete(f"/status_updates/{status_update_gid}", params=params if params else None)
        data = result.get("data", {})
        if data == {}:
            data = {"message": "Status update deleted.", "status_update_gid": status_update_gid}
        return {"successful": True, "data": data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_project_status_updates(
    client,
    project_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get status updates for a specific project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {"parent": project_gid}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/status_updates", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_project_templates(
    client,
    workspace_gid: Optional[str] = None,
    team_gid: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None
) -> dict:
    """Retrieve multiple project templates. List available project templates in a workspace or team."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if workspace_gid:
            params["workspace"] = workspace_gid
        if team_gid:
            params["team"] = team_gid
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)

        result = client.get("/project_templates", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_section(
    client,
    section_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve the full record for a single section by its GID."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/sections/{section_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_section(
    client,
    section_gid: str,
    name: Optional[str] = None,
    insert_before: Optional[str] = None,
    insert_after: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Update a section's name or position within a project. Use when you need to rename a section or reorder by specifying insert_before or insert_after. Get section_gid from GET_SECTIONS_IN_PROJECT or GET_SECTION. Get insert_before/insert_after section GIDs from GET_SECTIONS_IN_PROJECT."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not section_gid:
            return {"successful": False, "data": {}, "error": "section_gid is required."}

        data: Dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if insert_before is not None:
            data["insert_before"] = insert_before
        if insert_after is not None:
            data["insert_after"] = insert_after

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.put(
            f"/sections/{section_gid}",
            json={"data": data},
            params=params if params else None,
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_section(
    client,
    section_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Delete a section by its GID. Use when you need to permanently remove a section from a project. Section must be empty; last section in a project cannot be deleted. Get section_gid from GET_SECTIONS_IN_PROJECT or GET_SECTION."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not section_gid:
            return {"successful": False, "data": {}, "error": "section_gid is required."}

        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.delete(f"/sections/{section_gid}", params=params if params else None)
        data = result.get("data", {})
        if data == {}:
            data = {"message": "Section deleted.", "section_gid": section_gid}
        return {"successful": True, "data": data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_sections_in_project(
    client,
    project_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None
) -> dict:
    """Returns compact records for all sections in a specified project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        result = client.get(f"/projects/{project_gid}/sections", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_status_updates(
    client,
    parent: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None
) -> dict:
    """Retrieve status updates from an object (project, portfolio, or goal)."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {"parent": parent}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)

        result = client.get("/status_updates", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def save_project_as_template(
    client,
    project_gid: str,
    name: str,
    public: bool,
    team: Optional[str] = None,
    workspace: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a project template from an existing project. Returns an async job; poll the job for the new project template. In organizations use team (from GET_TEAMS_IN_WORKSPACE); in regular workspaces use workspace (from GET_MULTIPLE_WORKSPACES)."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}
        if not name:
            return {"successful": False, "data": {}, "error": "name is required."}

        data: Dict[str, Any] = {"name": name, "public": public}
        if team:
            data["team"] = team
        if workspace:
            data["workspace"] = workspace

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/projects/{project_gid}/saveAsTemplate",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def instantiate_project_template(
    client,
    project_template_gid: str,
    name: str,
    team: Optional[str] = None,
    privacy_setting: Optional[str] = None,
    is_strict: Optional[bool] = None,
    requested_dates: Optional[List[Dict[str, Any]]] = None,
    requested_roles: Optional[List[Dict[str, Any]]] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Instantiate (create) a real Asana project from a project template, returning the async job record."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        data = {"name": name}
        if team:
            data["team"] = team
        if privacy_setting:
            data["privacy_setting"] = privacy_setting
        if is_strict is not None:
            data["is_strict"] = is_strict
        if requested_dates:
            data["requested_dates"] = requested_dates
        if requested_roles:
            data["requested_roles"] = requested_roles

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/project_templates/{project_template_gid}/instantiateProject",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        err = str(e)
        if (requested_dates is None or requested_dates == []) and ("date variables are missing" in err or "requested_dates" in err.lower()):
            try:
                template_resp = client.get(
                    f"/project_templates/{project_template_gid}",
                    params={"opt_fields": "requested_dates"}
                )
                template_data = template_resp.get("data") or {}
                date_vars = template_data.get("requested_dates") or []
                if date_vars:
                    default_date = date.today().isoformat()
                    auto_dates = [{"gid": str(d["gid"]), "value": default_date} for d in date_vars if d.get("gid") is not None]
                    if auto_dates:
                        data["requested_dates"] = auto_dates
                        result = client.post(
                            f"/project_templates/{project_template_gid}/instantiateProject",
                            json={"data": data},
                            params=params if params else None
                        )
                        return {"successful": True, "data": result.get("data", {})}
            except Exception as retry_e:
                pass
            return {
                "successful": False,
                "data": {},
                "error": (
                    "This template has date variables; you must provide requested_dates as an array of objects: "
                    "[{\"gid\": \"<date_var_gid>\", \"value\": \"YYYY-MM-DD\"}, ...]. Original error: " + err
                ),
            }
        return {"successful": False, "data": {}, "error": err}


def create_section_in_project(
    client,
    project_gid: str,
    name: str,
    insert_before: Optional[str] = None,
    insert_after: Optional[str] = None
) -> dict:
    """Creates a new SECTION (not a task) in a project. Sections are organizational containers within a project used to group and categorize tasks."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        data = {"name": name}
        if insert_before:
            data["insert_before"] = insert_before
        if insert_after:
            data["insert_after"] = insert_after

        result = client.post(f"/projects/{project_gid}/sections", json={"data": data})
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def insert_section_for_project(
    client,
    project_gid: str,
    data: Dict[str, Any],
    opt_pretty: Optional[bool] = None
) -> dict:
    """Move or reorder an existing section within a project. Use when you need to reposition a section before or after another section. This does not create new sections; to create sections, use create_section_in_project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}
        if not data:
            return {"successful": False, "data": {}, "error": "data is required (must include section and before_section or after_section)."}

        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/projects/{project_gid}/sections/insert",
            json={"data": data},
            params=params if params else None,
        )
        response_data = result.get("data", {})
        if response_data == {}:
            response_data = {"message": "Section position updated.", "project_gid": project_gid}
        return {"successful": True, "data": response_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_project(
    client,
    project_gid: str,
    name: Optional[str] = None,
    archived: Optional[bool] = None,
    color: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
    default_view: Optional[str] = None,
    due_date: Optional[str] = None,
    due_on: Optional[str] = None,
    html_notes: Optional[str] = None,
    is_template: Optional[bool] = None,
    notes: Optional[str] = None,
    owner: Optional[str] = None,
    public: Optional[bool] = None,
    start_on: Optional[str] = None,
    team: Optional[str] = None
) -> dict:
    """Update a project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        data = {}
        if name is not None:
            data["name"] = name
        if archived is not None:
            data["archived"] = archived
        if color is not None:
            data["color"] = color
        if custom_fields is not None:
            data["custom_fields"] = custom_fields
        if default_view is not None:
            data["default_view"] = default_view
        if due_date is not None:
            data["due_date"] = due_date
        if due_on is not None:
            data["due_on"] = due_on
        if html_notes is not None:
            data["html_notes"] = html_notes
        if is_template is not None:
            data["is_template"] = is_template
        if notes is not None:
            data["notes"] = notes
        if owner is not None:
            data["owner"] = owner
        if public is not None:
            data["public"] = public
        if start_on is not None:
            data["start_on"] = start_on
        if team is not None:
            data["team"] = team

        result = client.put(f"/projects/{project_gid}", json={"data": data})
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_project(
    client,
    project_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Delete a project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.delete(f"/projects/{project_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def duplicate_project(
    client,
    project_gid: str,
    name: str,
    include: Optional[List[str]] = None,
    schedule_dates: Optional[Dict[str, Any]] = None,
    team: Optional[str] = None
) -> dict:
    """Duplicate a project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        data = {"name": name}
        if include:
            data["include"] = include
        if schedule_dates:
            data["schedule_dates"] = schedule_dates
        if team:
            data["team"] = team

        result = client.post(f"/projects/{project_gid}/duplicate", json={"data": data})
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

