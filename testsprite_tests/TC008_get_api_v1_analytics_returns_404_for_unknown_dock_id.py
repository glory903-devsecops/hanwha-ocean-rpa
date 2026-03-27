import requests

BASE_URL = "http://localhost:8082"
API_KEY = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {"Authorization": f"ApiKey {API_KEY}"}

def test_get_api_v1_analytics_returns_404_for_unknown_dock_id():
    unknown_dock_id = "unknown-nonexistent-dock-id-12345"
    url = f"{BASE_URL}/api/v1/analytics"
    params = {"dock_id": unknown_dock_id}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"

    try:
        json_response = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "error" in json_response, "Response JSON does not contain 'error' key"
    assert json_response["error"].lower() == "dock not found", f"Expected error message 'dock not found' but got '{json_response['error']}'"

test_get_api_v1_analytics_returns_404_for_unknown_dock_id()