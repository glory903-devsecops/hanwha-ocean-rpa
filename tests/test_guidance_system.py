import pytest
import requests
import os
import pandas as pd

BASE_URL = "http://localhost:8082"
DATA_DIR = "g:/내 드라이브/99.Develop/한화오션/hanwha-ocean-rpa/data"
GUIDELINES_PATH = os.path.join(DATA_DIR, "safety_guidelines.csv")

@pytest.fixture
def sample_guideline():
    return {
        "issue": "TEST_ISSUE_99",
        "guidance": "AI TEST GUIDANCE: AUTOMATED VERIFICATION",
        "severity": "CRITICAL",
        "rpa_trigger": "SENSOR_VAL > 100",
        "bot_id": "TEST_BOT_01"
    }

def test_api_health():
    """Verify that the API server is reachable."""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/guidelines")
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running on localhost:8082")

def test_create_and_read_guideline(sample_guideline):
    """Test Create and Read operations for safety guidelines."""
    # 1. Create
    response = requests.post(f"{BASE_URL}/api/v1/update-guideline", json=sample_guideline)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

    # 2. Read and Verify Integration
    response = requests.get(f"{BASE_URL}/api/v1/guidelines")
    assert response.status_code == 200
    data = response.json()
    
    match = next((item for item in data if item["ISSUE"] == sample_guideline["issue"]), None)
    assert match is not None
    assert match["GUIDANCE"] == sample_guideline["guidance"]
    assert match["RPA_TRIGGER"] == sample_guideline["rpa_trigger"]
    assert match["BOT_ID"] == sample_guideline["bot_id"]

def test_update_guideline(sample_guideline):
    """Test Update operation for an existing guideline."""
    updated_data = sample_guideline.copy()
    updated_data["guidance"] = "UPDATED AI GUIDANCE"
    
    response = requests.post(f"{BASE_URL}/api/v1/update-guideline", json=updated_data)
    assert response.status_code == 200
    
    # Verify Update in CSV
    df = pd.read_csv(GUIDELINES_PATH)
    row = df[df["ISSUE"] == sample_guideline["issue"]]
    assert row["GUIDANCE"].iloc[0] == "UPDATED AI GUIDANCE"

def test_delete_guideline(sample_guideline):
    """Test Delete operation for a guideline."""
    delete_payload = {
        "issue": sample_guideline["issue"],
        "guidance": "delete_request",
        "delete": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/update-guideline", json=delete_payload)
    assert response.status_code == 200
    
    # Verify deletion in CSV
    df = pd.read_csv(GUIDELINES_PATH)
    assert sample_guideline["issue"] not in df["ISSUE"].values

if __name__ == "__main__":
    pytest.main([__file__])
