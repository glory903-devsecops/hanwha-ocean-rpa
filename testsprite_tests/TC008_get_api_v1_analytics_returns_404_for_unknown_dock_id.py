import requests

BASE_URL = "http://localhost:8082"
API_KEY = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {
    "Authorization": f"ApiKey {API_KEY}",
    "Accept": "application/json"
}

def test_get_api_v1_analytics_returns_404_for_unknown_dock_id():
    unknown_dock_id = "unknown-dock-id-12345"
    url = f"{BASE_URL}/api/v1/analytics"
    params = {"dock_id": unknown_dock_id}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
    
    try:
        json_resp = response.json()
    except ValueError:
        assert False, "Response is not a valid JSON"

    assert "error" in json_resp, "Response JSON does not contain 'error' key"
    assert isinstance(json_resp["error"], str), "'error' key value is not a string"
    assert "dock not found" in json_resp["error"].lower(), f"Error message does not indicate dock not found: {json_resp['error']}"

test_get_api_v1_analytics_returns_404_for_unknown_dock_id()