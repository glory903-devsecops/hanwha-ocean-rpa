import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8082"

def test_get_api_v1_export_report_returns_csv_data():
    since_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

    url = f"{BASE_URL}/api/v1/export-report"
    params = {"format": "csv", "since": since_date}

    try:
        response = requests.get(url, params=params, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request to export-report failed: {e}"

    assert response.status_code in (200, 204), f"Expected status 200 or 204 but got {response.status_code}"

    if response.status_code == 204:
        assert response.text.strip() == "", "Expected empty body for 204 No Content"
    else:
        content_type = response.headers.get("Content-Type", "").lower()
        assert content_type.split(';')[0].strip() == "text/csv", f"Expected Content-Type text/csv but got {response.headers.get('Content-Type')}"

        content = response.text
        assert content.strip(), "Response CSV payload is empty"
        lines = content.splitlines()
        assert len(lines) > 1, "CSV payload should have header and at least one data line"
        assert all("," in line for line in lines), "CSV lines should contain commas"


test_get_api_v1_export_report_returns_csv_data()
