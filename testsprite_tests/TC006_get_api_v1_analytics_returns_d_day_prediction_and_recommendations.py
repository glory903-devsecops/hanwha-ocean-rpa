import requests
import datetime

BASE_URL = "http://localhost:8082"
API_KEY_NAME = "Antigravity"
API_KEY_VALUE = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {API_KEY_NAME: API_KEY_VALUE, "Content-Type": "application/json"}

def test_get_api_v1_analytics_returns_d_day_prediction_and_recommendations():
    # Step 1: Create a new dock record to ensure a valid dock_id exists for analytics
    create_payload = {
        "dock_id": "test-dock-tc006-" + datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"),
        "progress": 50,
        "safety_issue": False,
        "current_task": "Loading",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    dock_id = create_payload["dock_id"]
    try:
        # POST /api/v1/update-dock to create/update dock status
        response_create = requests.post(
            f"{BASE_URL}/api/v1/update-dock",
            headers=HEADERS,
            json=create_payload,
            timeout=30
        )
        response_create.raise_for_status()
        assert response_create.status_code == 200, f"Unexpected status code on create: {response_create.status_code}"
        json_create = response_create.json()
        assert json_create.get("status") == "saved"
        assert "file" in json_create and json_create["file"].endswith("dock_status.csv")
        assert isinstance(json_create.get("updated_record_count"), int) and json_create["updated_record_count"] > 0

        # Step 2: Call GET /api/v1/analytics?dock_id={dock_id} without auth headers
        params = {"dock_id": dock_id}
        response_analytics = requests.get(
            f"{BASE_URL}/api/v1/analytics",
            params=params,
            timeout=30
        )
        response_analytics.raise_for_status()
        assert response_analytics.status_code == 200, f"Unexpected status code on analytics: {response_analytics.status_code}"

        json_analytics = response_analytics.json()
        # Validate required fields presence and types
        assert "dock_id" in json_analytics and json_analytics["dock_id"] == dock_id
        assert "d_day" in json_analytics
        # d_day should be a date string YYYY-MM-DD - verify format
        d_day = json_analytics["d_day"]
        try:
            datetime.datetime.strptime(d_day, "%Y-%m-%d")
        except Exception:
            assert False, f"d_day value '{d_day}' is not a valid date string YYYY-MM-DD"

        assert "daily_rate" in json_analytics and isinstance(json_analytics["daily_rate"], (int, float))
        assert "risk_level" in json_analytics and json_analytics["risk_level"] in ("low", "medium", "high")
        assert "recommendations" in json_analytics and isinstance(json_analytics["recommendations"], list)

    finally:
        # Cleanup: delete the dock record if supported (not defined in PRD, so ignore)
        pass

test_get_api_v1_analytics_returns_d_day_prediction_and_recommendations()
