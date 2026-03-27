import requests
import json

BASE_URL = "http://localhost:8082"
API_KEY = "sk-user-7NjWyvWwmm8tAk2EOdjilY9H30jLc64qrMxvkVREmN8p_FLprSCbzgvceeFYWu21Ja4jvOwI2PwOQrFH-ybWkMq4JqYnRO_Y-zfOb8UjDS3NWSm2R11ai859htR_iFkKuCc"
HEADERS = {
    "Content-Type": "application/json",
    "Antigravity": API_KEY
}

def test_post_update_dock_missing_required_fields():
    # Step 1: Create a valid dock record to compare file state after failed update
    valid_payload = {
        "dock_id": "dock-test-002",
        "progress": 50,
        "safety_issue": False,
        "current_task": "Loading cargo",
        "timestamp": "2026-03-27T12:34:56Z"
    }

    # Create valid dock record
    create_response = requests.post(
        f"{BASE_URL}/api/v1/update-dock",
        headers=HEADERS,
        data=json.dumps(valid_payload),
        timeout=30
    )
    assert create_response.status_code == 200, f"Setup failed: {create_response.text}"

    # Fetch the dock status after setup
    fetch_response_before = requests.get(
        f"{BASE_URL}/api/v1/dashboard-status",
        params={"dock_id": valid_payload["dock_id"]},
        timeout=30
    )
    assert fetch_response_before.status_code == 200, f"Setup fetch failed: {fetch_response_before.text}"
    dock_record_before = fetch_response_before.json()

    # Step 2: Attempt to POST update missing required 'progress' field
    invalid_payload = {
        "dock_id": "dock-test-002",
        # "progress" is intentionally missing
        "safety_issue": True,
        "current_task": "Inspecting",
        "timestamp": "2026-03-27T13:00:00Z"
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/update-dock",
        headers=HEADERS,
        data=json.dumps(invalid_payload),
        timeout=30
    )

    # Validate response: status code 422 and validation error details
    assert response.status_code == 422, f"Expected 422 Unprocessable Entity but got {response.status_code}"
    try:
        error_body = response.json()
    except json.JSONDecodeError:
        assert False, "Response is not valid JSON"
    assert "detail" in error_body, "Response body missing validation error details"

    # Step 3: Verify dock_status.csv remains unchanged by fetching current dock record
    fetch_response_after = requests.get(
        f"{BASE_URL}/api/v1/dashboard-status",
        params={"dock_id": valid_payload["dock_id"]},
        timeout=30
    )
    assert fetch_response_after.status_code == 200, f"Failed to fetch dock status after failed update: {fetch_response_after.text}"
    dock_record_after = fetch_response_after.json()

    # Assert the dock record before and after are equal (no changes)
    assert dock_record_after == dock_record_before, "dock_status.csv changed despite failed update"

test_post_update_dock_missing_required_fields()
