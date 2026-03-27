import requests
import time

BASE_URL = "http://localhost:8082"
API_KEY = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {
    "Authorization": f"ApiKey {API_KEY}",
    "Content-Type": "application/json"
}

def test_get_dashboard_handles_generation_failure_and_logs_error():
    # Prepare dock update payload that triggers dashboard generation failure
    payload = {
        "dock_id": "test-dock-fail",
        "progress": 50,
        "safety_issue": False,
        "current_task": "Loading",
        "timestamp": "2026-03-27T12:00:00Z"
    }

    # POST /api/v1/update-dock to update CSV and trigger dashboard regeneration
    response_update = requests.post(f"{BASE_URL}/api/v1/update-dock", json=payload, headers=HEADERS, timeout=30)
    assert response_update.status_code == 200, f"Expected 200 OK for update-dock, got {response_update.status_code}"
    update_body = response_update.json()
    assert update_body.get("status") == "saved", "Update dock response status not 'saved'"
    assert "file" in update_body and update_body["file"].endswith("dock_status.csv"), "dock_status.csv not confirmed updated"
    assert type(update_body.get("updated_record_count")) is int and update_body["updated_record_count"] > 0, "updated_record_count invalid"

    # Allow some time for the dashboard regeneration attempt to complete
    time.sleep(5)

    # GET /dashboard - expect 500 Internal Server Error due to generation failure
    response_dashboard = requests.get(f"{BASE_URL}/dashboard", timeout=30)
    assert response_dashboard.status_code == 500, f"Expected 500 Internal Server Error, got {response_dashboard.status_code}"
    # Check for presence of generation failure text in HTML page
    assert "generation failure" in response_dashboard.text.lower() or "error" in response_dashboard.text.lower(), "Generation failure page content missing"

    # GET /api/v1/logs?source=dashboard-generate to confirm error logs presence
    response_logs = requests.get(f"{BASE_URL}/api/v1/logs", params={"source": "dashboard-generate"}, timeout=30)
    assert response_logs.status_code == 200, f"Expected 200 OK for logs endpoint, got {response_logs.status_code}"
    logs_json = response_logs.json()
    assert isinstance(logs_json, list), "Logs response is not a list"
    # Check that at least one log entry describes generation failure
    generation_failure_logged = any(
        ("generation" in (entry.get("message") or "").lower() and "fail" in (entry.get("message") or "").lower())
        or ("error" in (entry.get("level") or "").lower() and "dashboard" in (entry.get("message") or "").lower())
        for entry in logs_json
    )
    assert generation_failure_logged, "No dashboard generation failure log entry found"

test_get_dashboard_handles_generation_failure_and_logs_error()