import os
import requests


def get_base_url() -> str:
    # Use env var if provided, otherwise default to local FastAPI server
    return os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def api_request(method: str, path: str, token: str = None, payload: dict = None):
    # Simple wrapper around requests with consistent error handling
    url = get_base_url().rstrip("/") + path
    headers = {}

    if token:
        headers["Authorization"] = "Bearer " + token

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=headers, timeout=10)
        elif method == "PATCH":
            response = requests.patch(url, json=payload, headers=headers, timeout=10)
        else:
            return False, None, "Unsupported method"
    except Exception as exc:
        return False, None, str(exc)

    if 200 <= response.status_code < 300:
        if response.text:
            return True, response.json(), None
        return True, None, None

    error_message = "Request failed"
    try:
        error_data = response.json()
        if "detail" in error_data:
            error_message = error_data["detail"]
    except Exception:
        pass

    return False, None, error_message
