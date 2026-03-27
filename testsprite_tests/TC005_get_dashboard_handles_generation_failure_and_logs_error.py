import requests
import time

BASE_URL = "http://localhost:8082"
API_KEY = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {
    "Authorization": f"ApiKey {API_KEY}",
    "Content-Type": "application/json"
}
TIMEOUT = 30

def test_get_dashboard_generation_failure_and_log_error():
    dock_payload = {
        "dock_id": "test-dock-999",
        "progress": 70,
        "safety_issue": False,
        "current_task": "Loading containers",
        "timestamp": "2026-03-27T12:00:00Z"
    }

    resource_created = False
    try:
        # POST to /api/v1/update-dock to trigger dashboard re-rendering
        update_resp = requests.post(
            f"{BASE_URL}/api/v1/update-dock",
            headers=HEADERS,
            json=dock_payload,
            timeout=TIMEOUT
        )
        assert update_resp.status_code == 200, f"Expected 200 OK but got {update_resp.status_code}"
        update_json = update_resp.json()
        assert update_json.get("status") == "saved", f"Unexpected status: {update_json.get('status')}"
        assert "file" in update_json and update_json["file"].endswith("dock_status.csv"), "CSV file path missing or invalid"
        assert update_json.get("updated_record_count", 0) >= 1, "No records updated"

        resource_created = True

        # Wait briefly to allow dashboard generation process to proceed (simulate async process)
        time.sleep(3)

        # GET /dashboard expecting a 500 Internal Server Error due to generation failure
        dashboard_resp = requests.get(
            f"{BASE_URL}/dashboard",
            headers={},  # no auth required
            timeout=TIMEOUT
        )
        assert dashboard_resp.status_code == 500, f"Expected 500 Internal Server Error but got {dashboard_resp.status_code}"
        content = dashboard_resp.text.lower()
        assert "generation failure" in content or "error" in content, "Error page content not found in dashboard response"

        # GET logs for dashboard-generate source to confirm error logs
        logs_resp = requests.get(
            f"{BASE_URL}/api/v1/logs",
            headers={},  # no auth required
            params={"source": "dashboard-generate"},
            timeout=TIMEOUT
        )
        assert logs_resp.status_code == 200, f"Expected 200 OK from logs endpoint but got {logs_resp.status_code}"
        logs_json = logs_resp.json()
        assert isinstance(logs_json, list) and len(logs_json) > 0, "Logs list is empty"
        # Check the logs contain error details mentioning generation failure
        found_generation_error = any(
            ("generation" in log.get("message", "").lower() and "fail" in log.get("message", "").lower())
            or ("error" in log.get("message", "").lower())
            for log in logs_json
        )
        assert found_generation_error, "No log entry describing the generation failure found"

    finally:
        if resource_created:
            # Attempt to delete the dock record to clean up; assuming DELETE endpoint is /api/v1/update-dock/{dock_id}
            try:
                requests.delete(
                    f"{BASE_URL}/api/v1/update-dock/{dock_payload['dock_id']}",
                    headers=HEADERS,
                    timeout=TIMEOUT
                )
            except Exception:
                # Suppress exceptions in cleanup
                pass

test_get_dashboard_generation_failure_and_log_error()