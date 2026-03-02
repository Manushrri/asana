"""
Workspace Path Security Utilities for Asana MCP Server.

Provides secure file access within a configured WORKSPACE_PATH directory.
Prevents path traversal attacks and restricts all file I/O to the workspace.

Security Features:
- Only filenames or relative paths within workspace are accepted
- Absolute paths are BLOCKED
- Path traversal (..) is BLOCKED
- Symlinks escaping workspace are BLOCKED
"""

import os
import logging
from typing import Optional

_logger = logging.getLogger(__name__)

# Asana attachment max size (100 MB per API docs)
ASANA_ATTACHMENT_MAX_BYTES = 100 * 1024 * 1024


def get_workspace() -> str:
    """
    Return resolved workspace path from WORKSPACE_PATH (config or environment).

    Raises:
        PermissionError: If WORKSPACE_PATH is not configured.
    """
    workspace = os.environ.get("WORKSPACE_PATH") or ""
    if not workspace:
        try:
            from src.config import settings
            workspace = getattr(settings, "workspace_path", None) or ""
        except Exception:
            pass
    if not workspace:
        raise PermissionError(
            "Server Configuration Error: WORKSPACE_PATH environment variable is not set. "
            "File attachment upload from workspace is disabled. Set WORKSPACE_PATH to enable."
        )
    resolved = os.path.realpath(os.path.expanduser(workspace))
    if not os.path.isdir(resolved):
        raise PermissionError(
            f"Server Configuration Error: WORKSPACE_PATH '{workspace}' does not exist or is not a directory."
        )
    return resolved


def resolve_workspace_file(filename: str, must_exist: bool = False) -> str:
    """
    Securely resolve a filename to an absolute path inside WORKSPACE_PATH.

    Rules:
    - Only filenames or relative paths within workspace are accepted.
    - Absolute paths are BLOCKED (users must not know/provide full paths).
    - Path traversal (.. or symlinks escaping workspace) is BLOCKED.
    - Returns the resolved absolute path for internal use.

    Args:
        filename: The filename or relative path to resolve.
        must_exist: If True, raises FileNotFoundError if file doesn't exist.

    Returns:
        The resolved absolute path inside the workspace.

    Raises:
        ValueError: If filename is empty.
        PermissionError: If path escapes workspace or is absolute.
        FileNotFoundError: If must_exist=True and file doesn't exist.
    """
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty.")

    ws_real = get_workspace()

    # Block absolute paths — users should only provide filenames
    if os.path.isabs(filename):
        raise PermissionError(
            "Access denied: Absolute paths are not allowed. "
            "Provide just the filename or a relative path within the workspace (e.g., 'image.jpg' or 'docs/report.pdf')."
        )

    # Block obvious traversal attempts
    # Normalize to catch tricks like "foo/../../etc/passwd"
    normalized = os.path.normpath(filename)
    if normalized.startswith("..") or os.sep + ".." in normalized:
        raise PermissionError("Access denied: Path traversal is not allowed.")

    # Resolve to full path inside workspace
    abs_path = os.path.realpath(os.path.join(ws_real, normalized))

    # Final containment check: resolved path must be under workspace
    try:
        common = os.path.commonpath([abs_path, ws_real])
    except ValueError:
        raise PermissionError("Access denied: File is on a different drive than workspace.")

    if common != ws_real:
        raise PermissionError("Access denied: File resolves outside the workspace.")

    if must_exist and not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found in workspace: {filename}")

    return abs_path


def to_filename(abs_path: str) -> str:
    """
    Strip workspace prefix from an absolute path, returning only the relative filename.
    Used to sanitize all paths in tool responses so full server paths are never exposed.

    Args:
        abs_path: Absolute path to convert.

    Returns:
        Relative path from workspace root, or basename if conversion fails.
    """
    if not abs_path:
        return abs_path
    try:
        ws_real = get_workspace()
        rel = os.path.relpath(abs_path, ws_real)
        # If relpath went outside workspace (starts with ..), just return basename
        if rel.startswith(".."):
            return os.path.basename(abs_path)
        return rel
    except Exception:
        return os.path.basename(abs_path)


def is_workspace_configured() -> bool:
    """Check if WORKSPACE_PATH is configured and valid."""
    try:
        get_workspace()
        return True
    except PermissionError:
        return False


def validate_attachment_file(filename: str) -> dict:
    """
    Validate a file in the workspace for use as an Asana attachment.
    Ensures the path is inside the workspace (no path traversal) and meets size limits.

    Args:
        filename: The filename or relative path within the workspace.

    Returns:
        Dict with:
        - valid (bool): True if the file is safe to use.
        - error (str): Present if valid is False.
        - file_path (str): Resolved absolute path (only if valid).
        - size_bytes (int): File size (only if valid).
    """
    try:
        file_path = resolve_workspace_file(filename, must_exist=True)
    except (ValueError, PermissionError, FileNotFoundError) as e:
        return {"valid": False, "error": str(e)}

    if not os.path.isfile(file_path):
        return {"valid": False, "error": f"Path is not a file: {filename}"}

    size = os.path.getsize(file_path)
    if size == 0:
        return {"valid": False, "error": "File is empty (0 bytes)"}
    if size > ASANA_ATTACHMENT_MAX_BYTES:
        max_mb = ASANA_ATTACHMENT_MAX_BYTES / (1024 * 1024)
        actual_mb = size / (1024 * 1024)
        return {
            "valid": False,
            "error": f"File too large ({actual_mb:.1f} MB). Asana maximum: {max_mb:.0f} MB",
        }

    return {
        "valid": True,
        "file_path": file_path,
        "filename": filename,
        "size_bytes": size,
    }
