"""
Asana Event Tools
"""

import requests
from typing import Optional, List


def get_events(
    client,
    resource_gid: str,
    sync: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Retrieve events on a resource to monitor changes. Use to track activity or changes related to a specific Asana resource like a task, project, or tag."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params = {"resource": resource_gid}
        if sync:
            params["sync"] = sync
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        # Events API needs special handling: 412 returns a sync token (not a real error)
        url = f"{client.API_BASE_URL}/events"
        headers = client.get_headers()
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 412:
            # This is normal for the first call — returns a sync token to use next time
            data = response.json()
            sync_token = data.get("sync", "")
            return {
                "successful": True,
                "data": {
                    "sync": sync_token,
                    "message": "Initial sync token obtained. Pass this sync token in the next call to get new events.",
                    "events": []
                }
            }

        if not response.ok:
            error_data = response.json() if response.content else {}
            error_msg = f"{response.status_code} Error: {response.reason}"
            if "errors" in error_data:
                for err in error_data["errors"]:
                    if "message" in err:
                        error_msg += f" - {err['message']}"
            raise Exception(error_msg)

        result = response.json()
        return {"successful": True, "data": result}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}

