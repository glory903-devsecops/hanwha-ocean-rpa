import requests
import time

BASE_URL = "http://localhost:8082"
TIMEOUT = 30

def test_post_api_v1_update_dock_with_valid_payload():
    url = f"{BASE_URL}/api/v1/update-dock"
    headers = {
        "Content-Type": "application/json",
        # No auth required per instructions
    }
    payload = {
        "dock_id": "dock_test_123",
        "progress": 75,
        "safety_issue": False,
        "current_task": "Welding",
        "timestamp": "2026-03-27T15:30:00Z"
    }

    # POST valid update payload
    response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    resp_json = response.json()
    assert resp_json.get("status") == "saved", f"Expected status 'saved', got {resp_json.get('status')}"
    file_path = resp_json.get("file")
    assert isinstance(file_path, str) and file_path.endswith("dock_status.csv"), f"Invalid file path: {file_path}"
    updated_count = resp_json.get("updated_record_count")
    assert isinstance(updated_count, int) and updated_count > 0, f"Invalid updated_record_count: {updated_count}"

    # Wait briefly to allow CSV update and dashboard trigger
    time.sleep(1)

    # GET dashboard status to confirm updated record
    dashboard_url = f"{BASE_URL}/api/v1/dashboard-status"
    params = {"dock_id": payload["dock_id"]}
    get_resp = requests.get(dashboard_url, params=params, timeout=TIMEOUT)
    assert get_resp.status_code == 200, f"Expected 200 OK from dashboard-status, got {get_resp.status_code}"
    dock_record = get_resp.json()
    assert dock_record.get("dock_id") == payload["dock_id"], "dock_id mismatch in dashboard-status response"
    # Verify returned values match the update
    assert dock_record.get("progress") == payload["progress"], "Progress value mismatch in dashboard-status"
    # Convert safety_issue from response to bool safely
    safety_val = dock_record.get("safety_issue")
    if isinstance(safety_val, str):
        assert safety_val.lower() == str(payload["safety_issue"]).lower(), "Safety issue mismatch in dashboard-status"
    else:
        assert bool(safety_val) == payload["safety_issue"], "Safety issue mismatch in dashboard-status"
    assert dock_record.get("current_task") == payload["current_task"], "Current task mismatch in dashboard-status"
    # Timestamp might be stored slightly differently; ensure presence
    assert "timestamp" in dock_record, "Timestamp missing in dashboard-status response"

test_post_api_v1_update_dock_with_valid_payload()
