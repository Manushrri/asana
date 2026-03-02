"""
Asana MCP Server - Main Entry Point
"""

import importlib
import inspect
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastmcp import FastMCP
from fastmcp.tools.tool import FunctionTool
from dotenv import load_dotenv

# Load .env from project root so WORKSPACE_PATH and other vars are set even when
# the server is started from another directory (e.g. by Cursor MCP).
_project_root = Path(__file__).resolve().parents[1]
load_dotenv(_project_root / ".env", verbose=True)

from src.config import settings
from src.client import AsanaClient

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger("asana-mcp")

# Root path for manifest loading
ROOT_DIR = Path(__file__).resolve().parents[1]

# Server State
state: Dict[str, Any] = {}

mcp = FastMCP("asana-mcp")


def get_client() -> AsanaClient:
    """Get or create the singleton AsanaClient."""
    if "client" not in state:
        logger.info("Initializing AsanaClient...")
        try:
            state["client"] = AsanaClient()
            
            # Check authentication
            if not state["client"].is_authenticated():
                logger.info("Authentication required. Starting interactive OAuth2 flow...")
                state["client"].authenticate_interactive()
                
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            raise
    return state["client"]


def inject_default_context(client: AsanaClient, kwargs: dict) -> None:
    """
    Fill in workspace/user IDs from the current session when not provided, so the user
    doesn't have to enter them every time.

    Applies both to top-level parameters (e.g. workspace, workspace_gid, assignee, user_gid)
    and to common nested \"data\" objects used by many tools (e.g. CREATE_A_TASK payload).
    """
    empty_values = (None, "")
    default_ws = getattr(client, "default_workspace_gid", None)
    current_user = getattr(client, "current_user_gid", None)

    def _fill_context(target: dict) -> None:
        if not isinstance(target, dict):
            return
        if "workspace_gid" in target and target.get("workspace_gid") in empty_values and default_ws:
            target["workspace_gid"] = default_ws
        if "workspace" in target and target.get("workspace") in empty_values and default_ws:
            target["workspace"] = default_ws
        if "assignee" in target and target.get("assignee") in empty_values and current_user:
            target["assignee"] = current_user
        if "assignee_gid" in target and target.get("assignee_gid") in empty_values and current_user:
            target["assignee_gid"] = current_user
        if "user_gid" in target and target.get("user_gid") in empty_values and current_user:
            target["user_gid"] = current_user

    # Apply to top-level kwargs
    _fill_context(kwargs)

    # Also apply to common nested payloads, e.g. CREATE_A_TASK.data
    data = kwargs.get("data")
    if isinstance(data, dict):
        _fill_context(data)


def remove_null_from_schema(schema):
    """Remove null types from schema to prevent MCP Inspector trim() errors."""
    if isinstance(schema, dict):
        new_schema = {}
        for key, value in schema.items():
            if key == "anyOf" and isinstance(value, list):
                filtered = [v for v in value if not (isinstance(v, dict) and v.get("type") == "null")]
                if filtered:
                    if len(filtered) == 1:
                        new_schema.update(filtered[0])
                    else:
                        new_schema[key] = filtered
            elif key == "type" and isinstance(value, list) and "null" in value:
                filtered = [v for v in value if v != "null"]
                if len(filtered) == 1:
                    new_schema["type"] = filtered[0]
                else:
                    new_schema["type"] = filtered
            elif key == "type" and value == "null":
                continue
            elif key == "default" and value is None:
                continue
            else:
                new_schema[key] = remove_null_from_schema(value) if isinstance(value, (dict, list)) else value
        return new_schema
    elif isinstance(schema, list):
        return [remove_null_from_schema(item) for item in schema]
    else:
        return schema


def register_tools():
    """Register tools from tools_manifest.json dynamically."""
    manifest_path = ROOT_DIR / "tools_manifest.json"
    if not manifest_path.exists():
        logger.error(f"Manifest not found at {manifest_path}")
        return

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load manifest: {e}")
        return

    logger.info(f"Loading tools from manifest...")
    
    tools_registered = 0
    for entry in manifest.get("tools", []):
        tool_id = entry.get("id")
        target = entry.get("target")
        description = entry.get("description")
        input_schema = entry.get("input_schema")
        
        if not tool_id or not target:
            continue

        try:
            module_name, func_name = target.split(":")
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
        except Exception as e:
            logger.error(f"Failed to import {target}: {e}")
            continue

        try:
            wrapper = create_dynamic_wrapper(func, description, tool_id)
            
            tool = FunctionTool.from_function(
                wrapper,
                name=tool_id,
                description=description
            )
            
            if input_schema:
                cleaned_schema = remove_null_from_schema(input_schema)
                tool.parameters = cleaned_schema
            
            mcp.add_tool(tool)
            tools_registered += 1
            logger.info(f"Registered tool: {tool_id}")
            
        except Exception as e:
            logger.error(f"Failed to wrap/register {tool_id}: {e}")

    logger.info(f"Total tools registered: {tools_registered}")


def create_dynamic_wrapper(func, description, tool_id=None):
    """
    Creates a wrapper function that matches the signature of `func` (minus 'client')
    and injects the client instance.
    """
    sig = inspect.signature(func)
    params = [p for p in sig.parameters.values() if p.name != "client"]
    
    decl_parts = []
    names = []
    for p in params:
        if p.default is inspect._empty:
            decl_parts.append(p.name)
        else:
            decl_parts.append(f"{p.name}={repr(p.default)}")
        names.append(p.name)
    
    decl = ", ".join(decl_parts)
    
    normalize_kwargs = []
    for n in names:
        param = next((p for p in params if p.name == n), None)
        if param and param.default is not inspect._empty:
            normalize_kwargs.append(f"{n!r}: None if ({n} == '' or (isinstance({n}, dict) and len({n}) == 0)) else {n}")
        else:
            normalize_kwargs.append(f"{n!r}: {n}")
    
    src = (
        f"def wrapper({decl}):\n"
        f"    kwargs = {{{', '.join(normalize_kwargs)}}}\n"
        f"    client = __get_client()\n"
        f"    __inject_default_context(client, kwargs)\n"
        f"    return __func(client=client, **kwargs)\n"
    )

    local_ns = {}
    global_ns = {
        "__func": func,
        "__get_client": get_client,
        "__inject_default_context": inject_default_context,
    }
    
    exec(src, global_ns, local_ns)
    wrapper = local_ns["wrapper"]
    
    wrapper.__name__ = tool_id if tool_id else func.__name__
    wrapper.__doc__ = description or func.__doc__
    
    if hasattr(func, "__annotations__"):
        ann = dict(func.__annotations__)
        ann.pop("client", None)
        wrapper.__annotations__ = ann
        
    return wrapper


def main():
    """Main entry point."""
    register_tools()
    mcp.run()


if __name__ == "__main__":
    main()
