import requests
import time
from datetime import datetime, timezone

BASE_URL = "http://localhost:8082"
TIMEOUT = 30

def test_post_api_v1_update_dock_with_valid_payload():
    url = f"{BASE_URL}/api/v1/update-dock"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "dock_id": "dock-123",
        "progress": 75,
        "safety_issue": False,
        "current_task": "loading",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        response_json = response.json()
        assert response_json.get("status") == "saved", f"Expected status 'saved', got {response_json.get('status')}"
        file_path = response_json.get("file")
        updated_record_count = response_json.get("updated_record_count")
        assert file_path.endswith("data/dock_status.csv"), f"Expected file path to end with 'data/dock_status.csv', got {file_path}"
        assert isinstance(updated_record_count, int) and updated_record_count > 0, \
            f"Expected updated_record_count to be positive int, got {updated_record_count}"

        # Verify that dock_status.csv is updated with this dock_id by querying dashboard-status
        get_status_url = f"{BASE_URL}/api/v1/dashboard-status"
        params = {"dock_id": payload["dock_id"]}
        get_response = requests.get(get_status_url, params=params, timeout=TIMEOUT)
        assert get_response.status_code == 200, f"Expected status code 200 on dashboard-status, got {get_response.status_code}"
        dock_record = get_response.json()
        # Check fields to ensure updated data received matches posted payload
        assert dock_record.get("dock_id") == payload["dock_id"], "dock_id mismatch in dashboard status"
        assert dock_record.get("progress") == payload["progress"], "progress mismatch in dashboard status"
        assert dock_record.get("safety_issue") == payload["safety_issue"], "safety_issue mismatch in dashboard status"
        assert dock_record.get("current_task") == payload["current_task"], "current_task mismatch in dashboard status"

    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_post_api_v1_update_dock_with_valid_payload()
