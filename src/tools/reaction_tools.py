"""
Asana Reaction Tools
"""

from typing import Optional, List, Dict, Any


def get_reactions_on_object(
    client,
    target: str,
    emoji_base: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get reactions with a specific emoji base character on an object. Use when you need to retrieve user reactions (emoji responses) on a status update or story."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not target:
            return {"successful": False, "data": {}, "error": "target (object GID) is required."}
        if not emoji_base:
            return {"successful": False, "data": {}, "error": "emoji_base is required."}

        params: Dict[str, Any] = {
            "target": target,
            "emoji_base": emoji_base,
        }
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        # Note: Reactions endpoint is not yet documented in the public OpenAPI, but this follows the internal spec.
        result = client.get("/reactions", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

