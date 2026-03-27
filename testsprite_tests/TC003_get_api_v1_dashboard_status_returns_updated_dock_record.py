import requests
import uuid
import time

BASE_URL = "http://localhost:8082"
TIMEOUT = 30
HEADERS = {
    "Content-Type": "application/json"
}


def test_get_api_v1_dashboard_status_returns_updated_dock_record():
    # Generate unique dock_id for test isolation
    dock_id = f"test-dock-{uuid.uuid4()}"
    update_payload = {
        "dock_id": dock_id,
        "progress": 72.0,
        "safety_issue": False,
        "current_task": "Loading containers",
        "timestamp": int(time.time())
    }
    update_url = f"{BASE_URL}/api/v1/update-dock"
    dashboard_status_url = f"{BASE_URL}/api/v1/dashboard-status"

    # Step 1: POST to update-dock endpoint
    try:
        resp_update = requests.post(update_url, headers=HEADERS, json=update_payload, timeout=TIMEOUT)
    except Exception as e:
        assert False, f"POST /api/v1/update-dock request failed: {e}"

    assert resp_update.status_code == 200, f"Expected 200 OK from update-dock but got {resp_update.status_code}"

    json_resp = resp_update.json()
    assert "status" in json_resp and json_resp["status"] == "saved", f"Update response missing or invalid status: {json_resp}"
    assert "file" in json_resp and json_resp["file"].endswith("dock_status.csv"), f"Update response missing or invalid file path: {json_resp}"
    assert "updated_record_count" in json_resp and isinstance(json_resp["updated_record_count"], int) and json_resp["updated_record_count"] > 0, f"Update response missing or invalid updated_record_count: {json_resp}"

    # Step 2: GET to dashboard-status endpoint with dock_id
    params = {"dock_id": dock_id}
    try:
        resp_dashboard = requests.get(dashboard_status_url, params=params, timeout=TIMEOUT)
    except Exception as e:
        assert False, f"GET /api/v1/dashboard-status request failed: {e}"

    assert resp_dashboard.status_code == 200, f"Expected 200 OK from dashboard-status but got {resp_dashboard.status_code}"

    dashboard_json = resp_dashboard.json()
    # Validate that returned record matches the updated data
    assert isinstance(dashboard_json, dict), f"Dashboard status response is not a JSON object: {dashboard_json}"
    assert dashboard_json.get("dock_id") == dock_id, f"Dashboard dock_id mismatch: expected {dock_id}, got {dashboard_json.get('dock_id')}"
    assert dashboard_json.get("progress") == update_payload["progress"], f"Progress mismatch: expected {update_payload['progress']}, got {dashboard_json.get('progress')}"
    assert dashboard_json.get("safety_issue") == update_payload["safety_issue"], f"Safety issue mismatch: expected {update_payload['safety_issue']}, got {dashboard_json.get('safety_issue')}"
    assert dashboard_json.get("current_task") == update_payload["current_task"], f"Current task mismatch: expected {update_payload['current_task']}, got {dashboard_json.get('current_task')}"
    # timestamp may be returned as int or string; just assert presence and reasonable range
    returned_timestamp = dashboard_json.get("timestamp")
    assert isinstance(returned_timestamp, int), f"Timestamp missing or not int: {returned_timestamp}"
    assert abs(returned_timestamp - update_payload["timestamp"]) < 60, f"Timestamp mismatch: expected near {update_payload['timestamp']}, got {returned_timestamp}"


test_get_api_v1_dashboard_status_returns_updated_dock_record()
