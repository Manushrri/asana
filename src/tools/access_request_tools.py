"""
Asana Access Request Tools
"""

from typing import Optional, List


def get_access_requests(
    client,
    target: str,
    user: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve access requests for a target object. Use to get pending access requests for a specific project or portfolio, optionally filtered by user."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not target:
            return {"successful": False, "data": {}, "error": "target (project or portfolio GID) is required."}

        params = {"target": target}
        if user:
            params["user"] = user
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/access_requests", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def approve_access_request(
    client,
    access_request_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Approve an access request in Asana. Use when you need to grant access to a resource that requires approval workflow. Get access_request_gid from access request lists or notifications."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not access_request_gid:
            return {"successful": False, "data": {}, "error": "access_request_gid is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields) if isinstance(opt_fields, list) else opt_fields
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/access_requests/{access_request_gid}/approve",
            json={"data": {}},
            params=params if params else None,
        )
        data = result.get("data", {})
        if data == {}:
            data = {"message": "Access request approved.", "access_request_gid": access_request_gid}
        return {"successful": True, "data": data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def reject_access_request(
    client,
    access_request_gid: str,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Reject an access request in Asana. Use when you need to deny a user's request for access to a project or portfolio. Get access_request_gid from access request lists or notifications."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not access_request_gid:
            return {"successful": False, "data": {}, "error": "access_request_gid is required."}

        params = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields) if isinstance(opt_fields, list) else opt_fields
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/access_requests/{access_request_gid}/reject",
            json={"data": {}},
            params=params if params else None,
        )
        data = result.get("data", {})
        if data == {}:
            data = {"message": "Access request rejected.", "access_request_gid": access_request_gid}
        return {"successful": True, "data": data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_access_request(
    client,
    target: str,
    message: Optional[str] = None
) -> dict:
    """Create an access request in Asana. Use when you need to request access to a project or portfolio that you don't currently have access to. Get target GID from the project or portfolio URL or from GET_MULTIPLE_PROJECTS / GET_PORTFOLIOS (if you have partial visibility)."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not target:
            return {"successful": False, "data": {}, "error": "target (project or portfolio GID) is required."}

        data = {"target": target}
        if message:
            data["message"] = message

        result = client.post("/access_requests", json={"data": data})
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}
