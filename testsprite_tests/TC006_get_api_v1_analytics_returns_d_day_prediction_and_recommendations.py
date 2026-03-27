import requests
import uuid
import datetime

BASE_URL = "http://localhost:8082"
HEADERS = {"Authorization": "ApiKey sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"}
TIMEOUT = 30

def test_get_api_v1_analytics_returns_d_day_prediction_and_recommendations():
    dock_id = f"test-dock-{uuid.uuid4()}"
    update_payload = {
        "dock_id": dock_id,
        "progress": 50,
        "safety_issue": False,
        "current_task": "installing",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    try:
        # Create dock data first via update-dock endpoint
        update_resp = requests.post(
            f"{BASE_URL}/api/v1/update-dock", json=update_payload, headers=HEADERS, timeout=TIMEOUT
        )
        assert update_resp.status_code == 200, f"Update dock failed: {update_resp.text}"
        update_json = update_resp.json()
        assert update_json.get("status") == "saved", "Update dock response status not saved"
        assert "file" in update_json and update_json["file"].endswith("dock_status.csv"), "Update dock response missing correct file path"
        assert isinstance(update_json.get("updated_record_count"), int) and update_json["updated_record_count"] > 0, "No records updated"

        # Now call the analytics endpoint without headers (no auth required as per PRD)
        params = {"dock_id": dock_id}
        analytics_resp = requests.get(
            f"{BASE_URL}/api/v1/analytics", params=params, timeout=TIMEOUT
        )
        assert analytics_resp.status_code == 200, f"Analytics request failed: {analytics_resp.text}"
        analytics_json = analytics_resp.json()

        # Validate required fields in response JSON
        assert "dock_id" in analytics_json and isinstance(analytics_json["dock_id"], str), "dock_id missing or not a string in analytics response"
        
        d_day = analytics_json.get("d_day")
        assert isinstance(d_day, str), "d_day is missing or not a string"
        # Validate d_day is a valid date string YYYY-MM-DD
        try:
            datetime.datetime.strptime(d_day, "%Y-%m-%d")
        except Exception:
            assert False, f"d_day is not a valid date string: {d_day}"

        daily_rate = analytics_json.get("daily_rate")
        assert isinstance(daily_rate, (float, int)), "daily_rate is missing or not a number"

        risk_level = analytics_json.get("risk_level")
        assert risk_level in {"low", "medium", "high"}, f"risk_level unexpected value: {risk_level}"

        recommendations = analytics_json.get("recommendations")
        assert isinstance(recommendations, list), "recommendations is missing or not a list"
    finally:
        # Clean up: delete the dock record - no explicit delete endpoint, so skip cleanup
        pass

test_get_api_v1_analytics_returns_d_day_prediction_and_recommendations()
