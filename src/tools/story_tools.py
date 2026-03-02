"""
Asana Story Tools
"""

from typing import Optional, List, Dict, Any


def get_stories_for_task(
    client,
    task_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None
) -> dict:
    """Get stories (comments, status updates, etc.) for a task."""
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

        result = client.get(f"/tasks/{task_gid}/stories", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_story_for_task(
    client,
    task_gid: str,
    text: str,
    is_pinned: Optional[bool] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a comment story on a task. Use when you need to add a comment to a task as the authenticated user."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if not text:
            return {"successful": False, "data": {}, "error": "text is required for the comment story."}

        data: Dict[str, Any] = {"text": text}
        if is_pinned is not None:
            data["is_pinned"] = is_pinned

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/stories",
            json={"data": data},
            params=params if params else None,
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_story(
    client,
    story_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve the complete record for a single story."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get(f"/stories/{story_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def update_story(
    client,
    story_gid: str,
    data: Dict[str, Any],
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Update a story on a task. Use when you need to modify text, html_text, or pinned status. Only comment stories can have text/html_text updated; only comment and attachment stories can be pinned. Get story_gid from GET_STORIES_FOR_TASK or GET_STORY."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not story_gid:
            return {"successful": False, "data": {}, "error": "story_gid is required."}
        if not data:
            return {"successful": False, "data": {}, "error": "data is required (e.g. text, html_text, or pinned)."}

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.put(
            f"/stories/{story_gid}",
            json={"data": data},
            params=params if params else None,
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_story(
    client,
    story_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Delete a story by its GID. Use when you need to remove a story (e.g. comment) from Asana. Only the user who created the story can delete it. Get story_gid from GET_STORIES_FOR_TASK or GET_STORY."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not story_gid:
            return {"successful": False, "data": {}, "error": "story_gid is required."}

        params: Dict[str, Any] = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.delete(f"/stories/{story_gid}", params=params if params else None)
        data = result.get("data", {})
        if data == {}:
            data = {"message": "Story deleted.", "story_gid": story_gid}
        return {"successful": True, "data": data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

