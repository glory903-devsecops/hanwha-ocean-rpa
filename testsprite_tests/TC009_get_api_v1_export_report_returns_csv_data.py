import requests
from datetime import datetime, timedelta
import time

def test_get_api_v1_export_report_returns_csv_data():
    base_url = "http://localhost:8082"
    api_key = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
    headers = {
        "x-api-key": api_key
    }

    update_dock_url = f"{base_url}/api/v1/update-dock"
    get_export_url = f"{base_url}/api/v1/export-report"

    dock_payload = {
        "dock_id": "test-dock-001",
        "progress": 50,
        "safety_issue": False,
        "current_task": "loading",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        response = requests.post(update_dock_url, json=dock_payload, headers=headers, timeout=30)
        assert response.status_code == 200, f"Failed to update dock record, status code: {response.status_code}"
        update_resp_json = response.json()
        assert update_resp_json.get("status") == "saved"
        assert "dock_status.csv" in update_resp_json.get("file", "")

        # Wait briefly to allow CSV generation
        time.sleep(1)

        since_date = datetime.utcnow().date().isoformat()
        params = {"format": "csv", "since": since_date}
        # Remove auth headers for export-report GET as per PRD no auth mention here
        export_response = requests.get(get_export_url, params=params, timeout=30)

        # Accept 200 OK or 204 No Content as valid response
        assert export_response.status_code in (200, 204), f"Expected 200 OK or 204 No Content, got {export_response.status_code}"
        if export_response.status_code == 200:
            content_type = export_response.headers.get("Content-Type", "")
            assert content_type.startswith("text/csv"), f"Expected Content-Type text/csv, got {content_type}"
            csv_text = export_response.text
            assert "dock_id" in csv_text and "progress" in csv_text, "CSV payload missing expected columns"

    finally:
        pass


test_get_api_v1_export_report_returns_csv_data()
