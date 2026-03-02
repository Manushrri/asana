"""
Asana Attachment Tools
"""

import os
from typing import Optional, List, Dict, Any

import requests

from src.workspace_utils import is_workspace_configured, validate_attachment_file


def create_attachment_for_object(
    client,
    parent: str,
    file: Optional[Dict[str, Any]] = None,
    url: Optional[str] = None,
    name: Optional[str] = None,
    connect_to_app: Optional[bool] = None,
    resource_subtype: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Upload an attachment or link an external resource to a task or project. Use when you need to attach a file or external URL to a supported Asana object. Get parent GID from a task (CREATE_A_TASK, GET_TASKS_FROM_A_PROJECT) or project (GET_A_PROJECT). For file upload: pass file as {\"path\": \"filename.pdf\"} or {\"url\": \"https://...\", \"name\": \"doc.pdf\"} for external link. resource_subtype: \"asana\" (file) or \"external\" (URL)."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not parent:
            return {"successful": False, "data": {}, "error": "parent (task or project GID) is required."}

        file_obj = file or {}
        # Prefer top-level url/name if provided
        if url is not None:
            file_obj = {**file_obj, "url": url}
        if name is not None:
            file_obj = {**file_obj, "name": name}

        url_val = file_obj.get("url")
        file_path = file_obj.get("path") or file_obj.get("filename")

        if file_path:
            if not is_workspace_configured():
                return {
                    "successful": False,
                    "data": {},
                    "error": "WORKSPACE_PATH is not set. Set WORKSPACE_PATH to upload files from the workspace, or use external URL with url and name.",
                }
            validation = validate_attachment_file(file_path)
            if not validation.get("valid"):
                return {"successful": False, "data": {}, "error": validation.get("error", "Invalid file")}
            abs_path = validation["file_path"]
            name_val = file_obj.get("name") or os.path.basename(abs_path)
            api_url = f"{client.API_BASE_URL}/attachments"
            headers = {"Authorization": f"Bearer {client.access_token}", "Accept": "application/json"}
            params = {}
            if opt_fields:
                params["opt_fields"] = ",".join(opt_fields) if isinstance(opt_fields, list) else opt_fields
            if opt_pretty is not None:
                params["opt_pretty"] = str(opt_pretty).lower()
            with open(abs_path, "rb") as f:
                response = requests.post(
                    api_url,
                    headers=headers,
                    data={"parent": parent},
                    files={"file": (name_val, f, "application/octet-stream")},
                    params=params if params else None,
                )
            response.raise_for_status()
            result = response.json()
            return {"successful": True, "data": result.get("data", {})}

        if url_val:
            subtype = (resource_subtype or "external").lower()
            form_data = {
                "parent": parent,
                "resource_subtype": subtype,
                "url": url_val,
                "name": file_obj.get("name") or name or "attachment",
            }
            if connect_to_app is not None:
                form_data["connect_to_app"] = str(connect_to_app).lower()
            api_url = f"{client.API_BASE_URL}/attachments"
            headers = {"Authorization": f"Bearer {client.access_token}", "Accept": "application/json"}
            params = {}
            if opt_fields:
                params["opt_fields"] = ",".join(opt_fields) if isinstance(opt_fields, list) else opt_fields
            if opt_pretty is not None:
                params["opt_pretty"] = str(opt_pretty).lower()
            response = requests.post(api_url, headers=headers, data=form_data, params=params if params else None)
            response.raise_for_status()
            result = response.json()
            return {"successful": True, "data": result.get("data", {})}

        return {"successful": False, "data": {}, "error": "Provide either file (with path/filename or url+name) or url (and optionally name) for external link."}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_attachment(
    client,
    attachment_gid: str,
    opt_fields: Optional[str] = None
) -> dict:
    """Get a single attachment by its globally unique identifier."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_fields:
            params["opt_fields"] = opt_fields

        result = client.get(f"/attachments/{attachment_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_attachment_for_task(
    client,
    parent_gid: str,
    file: Dict[str, Any],
    resource_subtype: Optional[str] = "external",
    connect_to_app: Optional[bool] = None
) -> dict:
    """Upload an attachment to a task. Use when you need to attach a file to a specific task in Asana.
    File can be: (1) external URL — pass {\"url\": \"https://...\", \"name\": \"doc.pdf\"};
    (2) workspace file — when WORKSPACE_PATH is set, pass {\"path\": \"doc.pdf\"} or {\"filename\": \"doc.pdf\"}."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        url = f"{client.API_BASE_URL}/attachments"
        headers = {"Authorization": f"Bearer {client.access_token}"}

        # Workspace-relative file path: validate and upload as multipart file
        file_path = file.get("path") or file.get("filename")
        if file_path:
            if not is_workspace_configured():
                return {
                    "successful": False,
                    "data": {},
                    "error": "WORKSPACE_PATH is not set. Set WORKSPACE_PATH to upload files from the workspace, or use external URL with {\"url\": \"...\", \"name\": \"...\"}.",
                }
            validation = validate_attachment_file(file_path)
            if not validation.get("valid"):
                return {"successful": False, "data": {}, "error": validation.get("error", "Invalid file")}
            abs_path = validation["file_path"]
            name = file.get("name") or os.path.basename(abs_path)
            # Binary file upload: Asana expects only "parent" and "file" (no resource_subtype).
            with open(abs_path, "rb") as f:
                response = requests.post(
                    url,
                    headers={**headers, "Accept": "application/json"},
                    data={"parent": parent_gid},
                    files={"file": (name, f, "application/octet-stream")},
                )
            response.raise_for_status()
            result = response.json()
            return {"successful": True, "data": result.get("data", {})}

        # External URL attachment: send as form data (not JSON)
        form_data = {
            "parent": parent_gid,
            "resource_subtype": resource_subtype or "external",
            "url": file.get("url", ""),
            "name": file.get("name", "attachment"),
        }
        if connect_to_app is not None:
            form_data["connect_to_app"] = str(connect_to_app).lower()

        response = requests.post(url, headers=headers, data=form_data)
        response.raise_for_status()
        result = response.json()
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_task_attachments(
    client,
    parent_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None
) -> dict:
    """Get the list of attachments for a given task or project (by parent GID)."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {"parent": parent_gid}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)

        result = client.get("/attachments", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def delete_attachment(
    client,
    attachment_gid: str,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Delete an attachment by its globally unique identifier."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {}
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.delete(f"/attachments/{attachment_gid}", params=params if params else None)
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}
