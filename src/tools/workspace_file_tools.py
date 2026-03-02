"""
Workspace File Tools

Utility tools for safely listing files inside the configured WORKSPACE_PATH.
All paths returned are relative to the workspace root and never expose absolute
server paths.
"""

import os
from typing import Optional, List, Dict, Any

from src.workspace_utils import (
    is_workspace_configured,
    get_workspace,
    resolve_workspace_file,
    to_filename,
)


def list_workspace_files(
    client,
    subfolder: Optional[str] = None,
    recursive: Optional[bool] = False,
    max_results: Optional[int] = 200,
) -> dict:
    """
    List files and folders within the configured WORKSPACE_PATH.

    This tool is useful when you need to see what files are available for
    attachments (e.g., for CREATE_ATTACHMENT_FOR_OBJECT) without exposing
    absolute server paths.
    """
    try:
        if not is_workspace_configured():
            return {
                "successful": False,
                "data": {},
                "error": "WORKSPACE_PATH is not configured. Set WORKSPACE_PATH to enable workspace file listing.",
            }

        # Resolve base directory
        try:
            if subfolder:
                base_dir = resolve_workspace_file(subfolder, must_exist=True)
            else:
                base_dir = get_workspace()
        except Exception as e:
            return {"successful": False, "data": {}, "error": str(e)}

        if not os.path.isdir(base_dir):
            return {
                "successful": False,
                "data": {},
                "error": f"Path is not a directory in workspace: {subfolder or '.'}",
            }

        entries: List[Dict[str, Any]] = []
        limit = max_results if isinstance(max_results, int) and max_results > 0 else 200

        def add_entry(path: str, is_dir: bool) -> bool:
            """Add an entry to the list; return False if limit reached."""
            if len(entries) >= limit:
                return False
            rel = to_filename(path)
            item: Dict[str, Any] = {
                "path": rel,
                "type": "directory" if is_dir else "file",
            }
            if not is_dir:
                try:
                    item["size_bytes"] = os.path.getsize(path)
                except OSError:
                    item["size_bytes"] = None
            entries.append(item)
            return True

        if recursive:
            for dirpath, dirnames, filenames in os.walk(base_dir):
                # Sort for stable output
                dirnames.sort()
                filenames.sort()

                for d in dirnames:
                    if not add_entry(os.path.join(dirpath, d), is_dir=True):
                        break
                if len(entries) >= limit:
                    break
                for f in filenames:
                    if not add_entry(os.path.join(dirpath, f), is_dir=False):
                        break
                if len(entries) >= limit:
                    break
        else:
            try:
                names = sorted(os.listdir(base_dir))
            except OSError as e:
                return {"successful": False, "data": {}, "error": str(e)}
            for name in names:
                full_path = os.path.join(base_dir, name)
                if not add_entry(full_path, is_dir=os.path.isdir(full_path)):
                    break

        data: Dict[str, Any] = {
            "workspace_root": to_filename(base_dir),
            "entries": entries,
            "recursive": bool(recursive),
            "max_results": limit,
            "has_more": len(entries) >= limit,
        }
        return {"successful": True, "data": data}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

