"""
Asana Batch API Tools
"""

from typing import Dict, Any


def submit_parallel_requests(
    client,
    data: Dict[str, Any]
) -> dict:
    """Submit multiple Asana API requests in parallel using the Batch API. The data object should contain an 'actions' array (not 'requests'). Maximum 10 actions per batch."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        # Ensure data has 'actions' key (Asana Batch API format)
        if "actions" not in data and "requests" in data:
            # Convert 'requests' to 'actions' for backward compatibility
            data = {"actions": data["requests"]}
        elif "actions" not in data:
            return {"successful": False, "data": {}, "error": "Data must contain an 'actions' array."}

        result = client.post("/batch", json={"data": data})
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

