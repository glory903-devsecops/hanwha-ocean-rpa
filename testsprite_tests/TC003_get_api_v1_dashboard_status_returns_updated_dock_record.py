import requests
import uuid
import time

BASE_URL = "http://localhost:8082"
HEADERS = {"Content-Type": "application/json"}

def test_get_api_v1_dashboard_status_returns_updated_dock_record():
    dock_id = str(uuid.uuid4())
    update_payload = {
        "dock_id": dock_id,
        "progress": 75,
        "safety_issue": False,
        "current_task": "loading",
        "timestamp": str(int(time.time()))
    }

    # Step 1: POST /api/v1/update-dock to update dock record
    try:
        post_resp = requests.post(
            f"{BASE_URL}/api/v1/update-dock",
            json=update_payload,
            headers=HEADERS,
            timeout=30
        )
        assert post_resp.status_code == 200, f"POST update-dock failed: {post_resp.text}"
        post_json = post_resp.json()
        assert post_json.get("status") == "saved", "Update dock status not 'saved'"
        assert "file" in post_json and post_json["file"].endswith("dock_status.csv"), "CSV file path missing or incorrect"
        assert isinstance(post_json.get("updated_record_count"), int) and post_json["updated_record_count"] > 0, "updated_record_count invalid or zero"
        
        # Step 2: GET /api/v1/dashboard-status with dock_id to verify updated record
        get_resp = requests.get(
            f"{BASE_URL}/api/v1/dashboard-status",
            params={"dock_id": dock_id},
            headers=HEADERS,
            timeout=30
        )
        assert get_resp.status_code == 200, f"GET dashboard-status failed: {get_resp.text}"
        get_json = get_resp.json()
        assert isinstance(get_json, dict), "Dashboard status response is not a JSON object"
        # Verify dock_id matches and contents reflect the update
        assert get_json.get("dock_id") == dock_id, "dock_id in response does not match updated dock_id"
        assert get_json.get("progress") == update_payload["progress"], "Progress value mismatch"
        # Compare boolean equivalently for safety_issue
        assert bool(get_json.get("safety_issue")) == update_payload["safety_issue"], "Safety issue value mismatch"
        assert get_json.get("current_task") == update_payload["current_task"], "Current task value mismatch"
        # Timestamp may have some formatting or type differences, just check presence and numeric
        resp_timestamp = get_json.get("timestamp")
        assert isinstance(resp_timestamp, (int, float)) or (isinstance(resp_timestamp, str) and resp_timestamp.isdigit()), "Timestamp missing or invalid"
    finally:
        # Clean up by resetting dock record through POST with empty or default values might not be supported
        # Since no delete API is specified, no cleanup is conducted here
        pass

test_get_api_v1_dashboard_status_returns_updated_dock_record()
