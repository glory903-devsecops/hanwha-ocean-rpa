import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8082"
API_KEY = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {"Authorization": f"ApiKey {API_KEY}"}
TIMEOUT = 30


def test_get_api_v1_export_report_handles_unsupported_format_and_no_content():
    # Test unsupported format 'xml'
    try:
        params_xml = {"format": "xml"}
        response_xml = requests.get(f"{BASE_URL}/api/v1/export-report", headers=HEADERS, params=params_xml, timeout=TIMEOUT)
        assert response_xml.status_code == 400, f"Expected status 400 for unsupported format, got {response_xml.status_code}"
        json_resp = response_xml.json()
        assert "error" in json_resp, "Response JSON must contain 'error' key for unsupported format"
        assert "unsupported format" in json_resp["error"].lower(), f"Error message must mention unsupported format, got: {json_resp['error']}"
    except requests.RequestException as e:
        assert False, f"Request failed for unsupported format test: {e}"

    # Test with format=csv and since date with no matching records
    try:
        # Use a future date range assumed to have no records
        future_date = (datetime.utcnow() + timedelta(days=365)).strftime("%Y-%m-%d")
        params_csv = {"format": "csv", "since": future_date}
        response_csv = requests.get(f"{BASE_URL}/api/v1/export-report", headers=HEADERS, params=params_csv, timeout=TIMEOUT)
        assert response_csv.status_code == 204, f"Expected status 204 No Content for no matching records, got {response_csv.status_code}"
        assert response_csv.text == "", "Expected empty body on 204 No Content response"
    except requests.RequestException as e:
        assert False, f"Request failed for no content csv export test: {e}"


test_get_api_v1_export_report_handles_unsupported_format_and_no_content()