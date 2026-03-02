"""
Asana Time Tracking Tools
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


def get_time_tracking_entries(
    client,
    workspace: Optional[str] = None,
    task: Optional[str] = None,
    user: Optional[str] = None,
    portfolio: Optional[str] = None,
    attributable_to: Optional[str] = None,
    entered_on_start_date: Optional[str] = None,
    entered_on_end_date: Optional[str] = None,
    timesheet_approval_status: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get multiple time tracking entries across workspace, tasks, or projects. Use when you need to retrieve time tracking information for filtering by workspace, task, portfolio, user, or date range. Asana requires at least one date; if omitted, last 30 days is used."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}

        params: Dict[str, Any] = {}
        if workspace:
            params["workspace"] = workspace
        if task:
            params["task"] = task
        if user:
            params["user"] = user
        if portfolio:
            params["portfolio"] = portfolio
        if attributable_to:
            params["attributable_to"] = attributable_to
        # Asana returns [] unless at least one of task, user, portfolio, attributable_to is set; default to current user
        if not any([task, user, portfolio, attributable_to]):
            current_user = getattr(client, "current_user_gid", None)
            if current_user:
                params["user"] = current_user
        # Asana API requires at least one of entered_on_start_date or entered_on_end_date; default to last 30 days
        if entered_on_start_date or entered_on_end_date:
            if entered_on_start_date:
                params["entered_on_start_date"] = entered_on_start_date
            if entered_on_end_date:
                params["entered_on_end_date"] = entered_on_end_date
        else:
            end = datetime.utcnow().date()
            start = end - timedelta(days=30)
            params["entered_on_start_date"] = start.isoformat()
            params["entered_on_end_date"] = end.isoformat()
        if timesheet_approval_status:
            params["timesheet_approval_status"] = timesheet_approval_status
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.get("/time_tracking_entries", params=params)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def get_time_tracking_entries_for_task(
    client,
    task_gid: str,
    limit: Optional[int] = None,
    offset: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Get time tracking entries for a task. Use when you need to retrieve time tracking information recorded on a specific task."""
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

        result = client.get(f"/tasks/{task_gid}/time_tracking_entries", params=params if params else None)
        return {"successful": True, "data": result.get("data", [])}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}


def create_time_tracking_entry(
    client,
    task_gid: str,
    duration_minutes: int,
    entered_on: str,
    attributable_to: Optional[str] = None,
    description: Optional[str] = None,
    approval_status: Optional[str] = None,
    billable_status: Optional[str] = None,
    opt_fields: Optional[List[str]] = None,
    opt_pretty: Optional[bool] = None
) -> dict:
    """Create a time tracking entry on a task. Use when you need to log time spent on a task. Get task_gid from GET_MULTIPLE_TASKS or GET_TASKS_FROM_A_PROJECT. entered_on is the date the time was logged (YYYY-MM-DD). attributable_to is the project GID to count the time toward (optional; use when the task is in multiple projects)."""
    try:
        if not client.is_authenticated():
            return {"successful": False, "data": {}, "error": "Not authenticated."}
        if not task_gid:
            return {"successful": False, "data": {}, "error": "task_gid is required."}
        if duration_minutes is None or duration_minutes < 0:
            return {"successful": False, "data": {}, "error": "duration_minutes is required and must be >= 0."}
        if not entered_on:
            return {"successful": False, "data": {}, "error": "entered_on is required (YYYY-MM-DD)."}

        data: Dict[str, Any] = {
            "duration_minutes": duration_minutes,
            "entered_on": entered_on,
        }
        if attributable_to:
            data["attributable_to"] = attributable_to
        if description is not None:
            data["description"] = description
        if approval_status:
            data["approval_status"] = approval_status  # APPROVED, DRAFT, REJECTED, SUBMITTED
        if billable_status:
            data["billable_status"] = billable_status  # billable, nonBillable, notApplicable

        params: Dict[str, Any] = {}
        if opt_fields:
            params["opt_fields"] = ",".join(opt_fields)
        if opt_pretty is not None:
            params["opt_pretty"] = str(opt_pretty).lower()

        result = client.post(
            f"/tasks/{task_gid}/time_tracking_entries",
            json={"data": data},
            params=params if params else None,
        )
        return {"successful": True, "data": result.get("data", {})}
    except Exception as e:
        return {"successful": False, "data": {}, "error": str(e)}
