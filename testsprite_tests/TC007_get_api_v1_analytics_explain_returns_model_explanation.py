import requests
import uuid

BASE_URL = "http://localhost:8082"
HEADERS = {
    "Content-Type": "application/json",
    "Antigravity": "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
}
TIMEOUT = 30


def test_get_api_v1_analytics_explain_returns_model_explanation():
    dock_id = str(uuid.uuid4())
    update_payload = {
        "dock_id": dock_id,
        "progress": 50,
        "safety_issue": False,
        "current_task": "Loading cargo",
        "timestamp": "2026-03-27T12:00:00Z"
    }

    # Create a dock record to ensure dock_id exists
    try:
        update_resp = requests.post(
            f"{BASE_URL}/api/v1/update-dock",
            json=update_payload,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        assert update_resp.status_code == 200, f"Failed to create dock record: {update_resp.text}"
        json_update = update_resp.json()
        assert json_update.get("status") == "saved"
        assert json_update.get("file") == "data/dock_status.csv"
        assert isinstance(json_update.get("updated_record_count"), int)

        # Call the analytics explain endpoint
        explain_resp = requests.get(
            f"{BASE_URL}/api/v1/analytics/explain",
            params={"dock_id": dock_id},
            timeout=TIMEOUT,
        )
        assert explain_resp.status_code == 200, f"Unexpected status code: {explain_resp.status_code}, body: {explain_resp.text}"
        explain_json = explain_resp.json()
        assert isinstance(explain_json, dict)
        # Check dock_id matches
        assert explain_json.get("dock_id") == dock_id, f"Response dock_id mismatch: {explain_json}"

    finally:
        # No cleanup endpoint provided
        pass


test_get_api_v1_analytics_explain_returns_model_explanation()
