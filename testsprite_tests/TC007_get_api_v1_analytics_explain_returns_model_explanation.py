import requests
import uuid
import time

BASE_URL = "http://localhost:8082"
API_KEY = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {
    "Content-Type": "application/json",
    "Antigravity": API_KEY,
}

def test_get_api_v1_analytics_explain_returns_model_explanation():
    # Since dock_id is not provided, create a new dock record first to get a valid dock_id
    dock_id = f"test-dock-{uuid.uuid4()}"
    iso_timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    update_payload = {
        "dock_id": dock_id,
        "progress": 50,
        "safety_issue": False,
        "current_task": "Loading",
        "timestamp": iso_timestamp
    }

    try:
        # Create a dock record (POST /api/v1/update-dock)
        update_response = requests.post(
            f"{BASE_URL}/api/v1/update-dock",
            headers=HEADERS,
            json=update_payload,
            timeout=30
        )
        assert update_response.status_code == 200, f"Update dock failed: {update_response.text}"
        update_json = update_response.json()
        assert update_json.get("status") == "saved"
        assert "file" in update_json and update_json["file"].endswith("dock_status.csv")
        assert isinstance(update_json.get("updated_record_count"), int) and update_json["updated_record_count"] > 0

        # Allow some time for the analytics to be processed
        time.sleep(1)

        # Get analytics explanation for the dock_id (GET /api/v1/analytics/explain) - no auth headers per PRD
        explain_response = requests.get(
            f"{BASE_URL}/api/v1/analytics/explain",
            params={"dock_id": dock_id},
            timeout=30
        )
        assert explain_response.status_code == 200, f"Analytics explain failed: {explain_response.text}"
        explain_json = explain_response.json()
        # Validate the JSON response contains explanation keys (model factors and rule-based decisions)
        # We expect at least one key that describes explanation content. We check for typical keys.
        has_model_factors = any(
            key for key in explain_json if "model" in key.lower() or "factor" in key.lower() or "rule" in key.lower() or "explanation" in key.lower()
        )
        assert has_model_factors, "Response JSON does not contain model explanation or rule-based decision details."

    finally:
        # Cleanup: Remove the created dock record by setting progress to 0 or a known invalid state if deletion not supported
        # No explicit delete endpoint defined, so optionally update with empty or zero progress if needed
        # Here we just attempt reset progress to 0 to prevent side effects
        try:
            cleanup_payload = {
                "dock_id": dock_id,
                "progress": 0,
                "safety_issue": False,
                "current_task": "Cleanup",
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            }
            requests.post(
                f"{BASE_URL}/api/v1/update-dock",
                headers=HEADERS,
                json=cleanup_payload,
                timeout=30
            )
        except Exception:
            pass

test_get_api_v1_analytics_explain_returns_model_explanation()
