import requests
from datetime import datetime

BASE_URL = "http://localhost:8082"

def test_get_api_v1_export_report_unsupported_format_and_no_content():
    timeout = 30

    # Test unsupported format (xml)
    params_unsupported = {
        "format": "xml"
    }
    try:
        response1 = requests.get(f"{BASE_URL}/api/v1/export-report", params=params_unsupported, timeout=timeout)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response1.status_code == 400, f"Expected 400 Bad Request for unsupported format but got {response1.status_code}"
    try:
        json_resp = response1.json()
    except ValueError:
        assert False, "Response is not valid JSON for unsupported format error"
    assert "error" in json_resp, "Error message not found in response for unsupported format"
    assert "unsupported format" in json_resp["error"].lower(), "Error message does not indicate unsupported format"

    # Test format=csv with since date that matches no records
    # Use a very recent future date to ensure no records match
    future_date = (datetime.now().date().replace(year=datetime.now().year+10)).isoformat()
    params_no_content = {
        "format": "csv",
        "since": future_date
    }
    try:
        response2 = requests.get(f"{BASE_URL}/api/v1/export-report", params=params_no_content, timeout=timeout)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response2.status_code == 204, f"Expected 204 No Content for no matching records but got {response2.status_code}"


test_get_api_v1_export_report_unsupported_format_and_no_content()
