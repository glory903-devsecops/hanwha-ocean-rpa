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
    update_dock_url = f"{BASE_URL}/api/v1/update-dock"
    dashboard_url = f"{BASE_URL}/dashboard"
    
    # Prepare a valid dock update payload
    dock_id = "test-dock-001"
    update_payload = {
        "dock_id": dock_id,
        "progress": 75,
        "safety_issue": False,
        "current_task": "Loading containers",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    
    try:
        # Step 1: POST to /api/v1/update-dock to update dock data
        update_response = requests.post(update_dock_url, json=update_payload, headers=HEADERS, timeout=30)
        assert update_response.status_code == 200, f"Expected 200 OK, got {update_response.status_code}"
        update_json = update_response.json()
        assert update_json.get("status") == "saved", f"Expected status 'saved', got {update_json.get('status')}"
        assert "file" in update_json and update_json["file"].endswith("dock_status.csv"), "CSV file path missing or incorrect"
        assert isinstance(update_json.get("updated_record_count"), int) and update_json["updated_record_count"] > 0, "Updated record count invalid"
        
        # Wait briefly to allow dashboard regeneration
        time.sleep(2)
        
        # Step 2: GET /dashboard to verify updated Tailwind HTML with metrics and timestamp
        dashboard_response = requests.get(dashboard_url, headers=HEADERS, timeout=30)
        assert dashboard_response.status_code == 200, f"Expected 200 OK from /dashboard, got {dashboard_response.status_code}"
        html_content = dashboard_response.text
        
        # Validate presence of key updated metrics from payload in the HTML
        assert str(update_payload["progress"]) in html_content, "Progress metric not found in dashboard HTML"
        assert update_payload["current_task"] in html_content, "Current task not found in dashboard HTML"
        
        # Validate presence of recent generation timestamp indicating dashboard regeneration
        # Instead of looking for specific keywords, look for ISO datetime pattern and check recency
        import re
        iso_datetime_match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", html_content)
        assert iso_datetime_match, "ISO 8601 generation timestamp not found in dashboard HTML"
        gen_time_str = iso_datetime_match.group(0)
        try:
            gen_time = datetime.datetime.fromisoformat(gen_time_str.replace("Z", "+00:00"))
            now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            delta = now - gen_time
            assert delta.total_seconds() < 300, "Generation timestamp is not recent"
        except Exception as e:
            assert False, f"Failed to parse or validate generation timestamp: {e}"
        
    finally:
        # Cleanup: POST to update dock with a reset or empty payload if needed (optional)
        # Not required by instructions, so no cleanup
        pass

test_get_dashboard_serves_updated_tailwind_html()
