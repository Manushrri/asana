"""
Asana Task Tools
"""

import json
from typing import Optional, List, Dict, Any


def get_projects_for_task(
    client,
    task_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get all projects a task is in."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}

        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/tasks/{task_gid}/projects", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_task(
    client,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Creates a new Asana task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not data:
            return {"successful": False, "data": {}, "error": "data is required."}
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

        result = client.post("/tasks", json={"data": data}, params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_subtask(
    client,
    task_gid: str,
    name: str,
    assignee: Optional[str] = None,
    notes: Optional[str] = None,
    due_on: Optional[str] = None,
    due_at: Optional[str] = None,
    completed: Optional[bool] = None,
    followers: Optional[List[str]] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Creates a new subtask under an existing parent task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if not name:
            return {"successful": False, "data": {}, "error": "name is required."}
        if due_on and due_at:
            return {"successful": False, "data": {}, "error": "due_on and due_at are mutually exclusive."}

        data: Dict[str, Any] = {"name": name}
        if assignee:
            data["assignee"] = assignee
        if notes is not None:
            data["notes"] = notes
        if due_on:
            data["due_on"] = due_on
        if due_at:
            data["due_at"] = due_at
        if completed is not None:
            data["completed"] = completed
        if followers:
            data["followers"] = followers

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/subtasks",
            json={"data": data},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_task_comment(
    client,
    task_id: str,
    text: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Adds a new text comment (story) to an existing Asana task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_id:
            return {"successful": False, "data": {}, "error": "task_id is required."}
        if not text:
            return {"successful": False, "data": {}, "error": "text is required."}

        data = {"text": text}
        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_id}/stories",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        # If Asana returns an empty or non-object data, synthesize a clean summary.
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Comment story created on task.",
                "task_id": task_id,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_followers_to_task(
    client,
    task_gid: str,
    followers: List[str],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add followers to a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
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
            f"/tasks/{task_gid}/addFollowers",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Followers added to task.",
                "task_gid": task_gid,
                "followers": follower_list,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_project_for_task(
    client,
    task_gid: str,
    project: str,
    section: Optional[str] = None,
    insert_before: Optional[str] = None,
    insert_after: Optional[str] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add a project to a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if not project:
            return {"successful": False, "data": {}, "error": "project is required."}

        data: Dict[str, Any] = {"project": project}
        if section:
            data["section"] = section
        if insert_before:
            data["insert_before"] = insert_before
        if insert_after:
            data["insert_after"] = insert_after

        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/addProject",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        # Asana often returns 200 with an empty or non-object data for addProject;
        # synthesize a helpful summary so the caller sees what was done.
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Project added to task.",
                "task_gid": task_gid,
                "project": project,
            }
            if section:
                api_data["section"] = section
            if insert_before:
                api_data["insert_before"] = insert_before
            if insert_after:
                api_data["insert_after"] = insert_after
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def remove_project_from_task(
    client,
    task_gid: str,
    project: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Remove a project from a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if not project:
            return {"successful": False, "data": {}, "error": "project is required."}

        data = {"project": project}
        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/removeProject",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        # Asana often returns 200 with an empty or non-object data for removeProject;
        # synthesize a helpful summary so the caller sees what was done.
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Project removed from task.",
                "task_gid": task_gid,
                "project": project,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def set_parent_for_task(
    client,
    task_gid: str,
    parent: Optional[str] = None,
    insert_before: Optional[str] = None,
    insert_after: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Set the parent of a task (make it a subtask) or remove the parent."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}

        data: Dict[str, Any] = {}
        if parent is not None:
            data["parent"] = parent
        if insert_before:
            data["insert_before"] = insert_before
        if insert_after:
            data["insert_after"] = insert_after

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/setParent",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            msg = "Parent removed from task." if parent is None else "Parent set for task."
            api_data = {
                "message": msg,
                "task_gid": task_gid,
            }
            if parent is not None:
                api_data["parent"] = parent
            if insert_before:
                api_data["insert_before"] = insert_before
            if insert_after:
                api_data["insert_after"] = insert_after
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_tag_to_task(
    client,
    task_gid: str,
    tag_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add an existing tag to a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if not tag_gid:
            return {"successful": False, "data": {}, "error": "tag_gid is required."}

        data = {"tag": tag_gid}
        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields) if isinstance(opt_fields, list) else opt_fields
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/addTag",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        # Asana often returns 200 with an empty or non-object data for addTag;
        # synthesize a helpful summary so the caller sees what was done.
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Tag added to task.",
                "task_gid": task_gid,
                "tag_gid": tag_gid,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_task_dependencies(
    client,
    task_gid: str,
    dependencies: List[str],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Add dependency relationships to a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        dep_list = dependencies if isinstance(dependencies, list) else [dependencies]
        if not dep_list:
            return {"successful": False, "data": {}, "error": "At least one dependency (task GID) is required."}

        data = {"dependencies": dep_list}
        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields) if isinstance(opt_fields, list) else opt_fields
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/addDependencies",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Dependencies added to task.",
                "task_gid": task_gid,
                "dependencies": dep_list,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_multiple_tasks(
    client,
    assignee: Optional[str] = None,
    workspace: Optional[str] = None,
    project: Optional[str] = None,
    section: Optional[str] = None,
    tag: Optional[str] = None,
    user_task_list: Optional[str] = None,
    completed_since: Optional[str] = None,
    modified_since: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieves a list of tasks with optional filters."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params: Dict[str, Any] = {}
        if assignee:
            params["assignee"] = assignee
        if workspace:
            params["workspace"] = workspace
        if project:
            params["project"] = project
        if section:
            params["section"] = section
        if tag:
            params["tag"] = tag
        if user_task_list:
            params["user_task_list"] = user_task_list
        if completed_since:
            params["completed_since"] = completed_since
        if modified_since:
            params["modified_since"] = modified_since
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/tasks", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_tasks_from_a_project(
    client,
    project_gid: str,
    completed_since: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieves tasks from a specified project."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not project_gid:
            return {"successful": False, "data": {}, "error": "project_gid is required."}

        params: Dict[str, Any] = {"project": project_gid}
        if completed_since:
            params["completed_since"] = completed_since
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/tasks", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_tasks_from_a_section(
    client,
    section_gid: str,
    completed_since: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve tasks in a specific section."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not section_gid:
            return {"successful": False, "data": {}, "error": "section_gid is required."}

        params: Dict[str, Any] = {}
        if completed_since:
            params["completed_since"] = completed_since
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/sections/{section_gid}/tasks", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_tasks_for_tag(
    client,
    tag_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve tasks associated with a specific tag."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not tag_gid:
            return {"successful": False, "data": {}, "error": "tag_gid is required."}

        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/tags/{tag_gid}/tasks", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_tasks_for_user_task_list(
    client,
    user_task_list_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    completed_since: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve tasks from a user task list."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not user_task_list_gid:
            return {"successful": False, "data": {}, "error": "user_task_list_gid is required."}

        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if completed_since:
            params["completed_since"] = completed_since
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(
            f"/user_task_lists/{user_task_list_gid}/tasks",
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_task_subtasks(
    client,
    task_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve subtasks of a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}

        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/tasks/{task_gid}/subtasks", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_a_task(
    client,
    task_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieves full details for a specified task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/tasks/{task_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def add_task_to_section(
    client,
    task_gid: str,
    section_gid: str,
    insert_before: Optional[str] = None,
    insert_after: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Adds an existing task to a section."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if not section_gid:
            return {"successful": False, "data": {}, "error": "section_gid is required."}

        data: Dict[str, Any] = {"task": task_gid}
        if insert_before:
            data["insert_before"] = insert_before
        if insert_after:
            data["insert_after"] = insert_after

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/sections/{section_gid}/addTask",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Task added to section.",
                "task_gid": task_gid,
                "section_gid": section_gid,
            }
            if insert_before:
                api_data["insert_before"] = insert_before
            if insert_after:
                api_data["insert_after"] = insert_after
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def remove_follower_from_task(
    client,
    task_gid: str,
    followers: List[str],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Remove one or more followers from a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        follower_list = followers if isinstance(followers, list) else [f.strip() for f in str(followers).split(",") if f.strip()]
        if not follower_list:
            return {"successful": False, "data": {}, "error": "At least one follower (user GID) is required."}

        data = {"followers": follower_list}
        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/removeFollowers",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Followers removed from task.",
                "task_gid": task_gid,
                "followers": follower_list,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def remove_tag_from_task(
    client,
    task_gid: str,
    tag: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Remove a tag from a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if not tag:
            return {"successful": False, "data": {}, "error": "tag is required."}

        data = {"tag": tag}
        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields) if isinstance(opt_fields, list) else opt_fields
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/removeTag",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Tag removed from task.",
                "task_gid": task_gid,
                "tag": tag,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def search_tasks_in_workspace(
    client,
    workspace_gid: Optional[str] = None,
    text: Optional[str] = None,
    resource_subtype: Optional[str] = None,
    assignee_any: Optional[List[str]] = None,
    projects_any: Optional[List[str]] = None,
    limit: Optional[int] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Search tasks across a workspace with advanced filters."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not workspace_gid:
            workspace_gid = getattr(client, "default_workspace_gid", None)
        if not workspace_gid:
            return {"successful": False, "data": {}, "error": "workspace_gid is required (or set default workspace)."}

        params: Dict[str, Any] = {}
        if text:
            params["text"] = text
        if resource_subtype:
            params["resource_subtype"] = resource_subtype
        if assignee_any:
            params["assignee.any"] = ",".join(assignee_any)
        if projects_any:
            params["projects.any"] = ",".join(projects_any)
        if limit is not None:
            params["limit"] = limit
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/workspaces/{workspace_gid}/tasks/search",
            json={"data": {}},
            params=params if params else None
        )
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_a_task(
    client,
    task_gid: str,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Updates attributes of an existing Asana task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if not data:
            return {"successful": False, "data": {}, "error": "data is required."}
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return {"successful": False, "data": {}, "error": "data must be a JSON object."}
        if not isinstance(data, dict):
            return {"successful": False, "data": {}, "error": "data must be an object."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.put(
            f"/tasks/{task_gid}",
            json={"data": data},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Task updated.",
                "task_gid": task_gid,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_task(
    client,
    task_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Delete a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}

        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.delete(f"/tasks/{task_gid}", params=params if params else None)
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Task deleted.",
                "task_gid": task_gid,
            }
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def duplicate_task(
    client,
    task_gid: str,
    name: Optional[str] = None,
    include: Optional[List[str]] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Duplicate a task."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}

        data: Dict[str, Any] = {}
        if name:
            data["name"] = name
        if include:
            data["include"] = include

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/duplicate",
            json={"data": data} if data else {"data": {}},
            params=params if params else None
        )
        api_data = result.get("data")
        if not isinstance(api_data, dict) or not api_data:
            api_data = {
                "message": "Task duplication requested.",
                "task_gid": task_gid,
            }
            if name:
                api_data["name"] = name
            if include:
                api_data["include"] = include
        return {"successful": True, "data": api_data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}
