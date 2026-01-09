"""Helper utilities."""

from typing import Any, Dict


def success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """Create a success response."""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return response


def error_response(message: str, errors: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create an error response."""
    response = {"success": False, "message": message}
    if errors:
        response["errors"] = errors
    return response

