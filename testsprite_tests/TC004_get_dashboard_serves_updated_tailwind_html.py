import requests
import datetime
import time

BASE_URL = "http://localhost:8082"
API_KEY = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {
    "Content-Type": "application/json",
    "Antigravity": API_KEY
}

def test_get_dashboard_serves_updated_tailwind_html():
    # Prepare valid dock update payload
    dock_id = "test-dock-001"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    update_payload = {
        "dock_id": dock_id,
        "progress": 75,
        "safety_issue": False,
        "current_task": "Loading containers",
        "timestamp": timestamp
    }

    try:
        # Step 1: POST /api/v1/update-dock to update dock data
        update_resp = requests.post(
            f"{BASE_URL}/api/v1/update-dock",
            headers=HEADERS,
            json=update_payload,
            timeout=30
        )
        assert update_resp.status_code == 200, f"Update dock failed, status code {update_resp.status_code}"
        update_json = update_resp.json()
        assert update_json.get("status") == "saved", "Dock update response missing 'saved' status"
        assert "file" in update_json and update_json["file"].endswith("dock_status.csv"), "Response file path invalid"
        assert isinstance(update_json.get("updated_record_count"), int) and update_json["updated_record_count"] > 0, "Invalid updated_record_count"

        # Wait briefly to allow dashboard regeneration
        time.sleep(3)

        # Step 2: GET /dashboard to fetch updated dashboard HTML
        dashboard_resp = requests.get(
            f"{BASE_URL}/dashboard",
            timeout=30
        )
        assert dashboard_resp.status_code == 200, f"Dashboard fetch failed, status code {dashboard_resp.status_code}"
        dashboard_html = dashboard_resp.text

        # Verify updated metrics appear in the HTML (e.g. the progress value and dock id)
        assert str(update_payload["progress"]) in dashboard_html, "Updated progress not found in dashboard HTML"
        assert dock_id in dashboard_html, "Dock ID not found in dashboard HTML"
        
        # Verify presence of a recent generation timestamp in the dashboard HTML
        # Naive approach: look for ISO date substring close to now (within 5 minutes)
        now = datetime.datetime.utcnow()
        found_timestamp = False
        for line in dashboard_html.splitlines():
            # Example timestamp formats could vary, so look for recent ISO 8601 datetime substring
            if "timestamp" in line.lower() or "generated" in line.lower() or "last updated" in line.lower():
                # Try extract something that looks like ISO datetime
                import re
                iso_dates = re.findall(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", line)
                for iso_date in iso_dates:
                    try:
                        gen_time = datetime.datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ")
                        delta = now - gen_time
                        if delta.total_seconds() >= 0 and delta.total_seconds() < 300:
                            found_timestamp = True
                            break
                    except Exception:
                        continue
            if found_timestamp:
                break
        assert found_timestamp, "Recent generation timestamp not found or not recent in dashboard HTML"

    except requests.RequestException as e:
        assert False, f"HTTP request failed: {e}"

test_get_dashboard_serves_updated_tailwind_html()