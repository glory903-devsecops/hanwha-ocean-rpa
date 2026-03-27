import requests
import json
import time

BASE_URL = "http://localhost:8082"
HEADERS = {
    "Content-Type": "application/json"
}
TIMEOUT = 30

def test_post_api_v1_update_dock_missing_required_fields():
    # Step 1: Create a valid dock record to compare for unchanged data after invalid update attempt
    valid_payload = {
        "dock_id": "dock-tc002-test",
        "progress": 50.0,
        "safety_issue": False,
        "current_task": "loading",
        "timestamp": int(time.time())
    }
    try:
        # Create valid record
        resp_create = requests.post(
            f"{BASE_URL}/api/v1/update-dock",
            headers=HEADERS,
            json=valid_payload,
            timeout=TIMEOUT,
        )
        assert resp_create.status_code == 200, f"Setup failed: Expected 200, got {resp_create.status_code}"
        create_response_json = resp_create.json()
        assert (
            create_response_json.get("status") == "saved"
        ), "Setup failed: status is not 'saved'."
        # Step 2: Attempt to post with missing required "progress" field (invalid payload)
        invalid_payload = {
            "dock_id": valid_payload["dock_id"],
            # "progress" field missing intentionally
            "safety_issue": True,
            "current_task": "unloading",
            "timestamp": int(time.time()),
        }
        resp_invalid = requests.post(
            f"{BASE_URL}/api/v1/update-dock",
            headers=HEADERS,
            json=invalid_payload,
            timeout=TIMEOUT,
        )
        # Step 3: Verify 400 Bad Request with validation error details in response body
        assert resp_invalid.status_code == 400, f"Expected 400 Bad Request, got {resp_invalid.status_code}"
        try:
            error_response = resp_invalid.json()
        except json.JSONDecodeError:
            assert False, "Response body is not valid JSON."
        # The error response should contain validation error details: could be 'error' or 'detail' or similar
        validation_error_found = False
        if isinstance(error_response, dict):
            # Common FastAPI validation error response has 'detail' key with list of errors
            if "detail" in error_response and isinstance(error_response["detail"], list):
                validation_error_found = any(
                    "progress" in str(item).lower() for item in error_response["detail"]
                )
            elif "error" in error_response:
                validation_error_found = "progress" in error_response["error"].lower()
        assert validation_error_found, "Validation error details for missing 'progress' field not found in response."

        # Step 4: Verify dock_status.csv file remains unchanged by checking GET /api/v1/dashboard-status?dock_id=<dock_id>
        resp_dashboard = requests.get(
            f"{BASE_URL}/api/v1/dashboard-status",
            params={"dock_id": valid_payload["dock_id"]},
            timeout=TIMEOUT,
        )
        assert resp_dashboard.status_code == 200, f"Expected 200 OK from dashboard-status, got {resp_dashboard.status_code}"
        dashboard_data = resp_dashboard.json()
        # The dashboard data should reflect the original valid payload 'progress' value, not updated invalid payload
        assert (
            "progress" in dashboard_data and dashboard_data["progress"] == valid_payload["progress"]
        ), "Dock progress changed despite invalid update attempt."
        # Optionally verify other fields were not altered to an invalid state
    finally:
        # Cleanup: delete the created dock record if API supports delete (not described in PRD)
        # Since no endpoint described for deletion, skip this step.
        pass

test_post_api_v1_update_dock_missing_required_fields()
