import requests
import os
import pandas as pd
import time

def test_integration():
    url_base = "http://localhost:8081"
    
    print("📡 [TEST] Starting API Integration Verification...")
    
    # 1. Update Dock
    dock_data = {
        "dock": "🧪 테스트 부두 99",
        "progress": 88.8,
        "task": "최종 검증 중",
        "safety": "정상"
    }
    r = requests.post(f"{url_base}/api/update_dock", json=dock_data)
    if r.status_code != 200:
        print(f"❌ Failed to update dock: {r.text}")
        return
    assert r.json()["status"] == "success"
    print("✅ [Dock API] Update Successful.")
    
    # 2. Update Guideline
    guide_data = {
        "issue": "테스트 위험 상황",
        "guidance": "즉시 대피 및 상층부 보고 요망 (자동 검증)"
    }
    r = requests.post(f"{url_base}/api/update_guideline", json=guide_data)
    if r.status_code != 200:
        print(f"❌ Failed to update guideline: {r.text}")
        return
    assert r.json()["status"] == "success"
    print("✅ [Guideline API] Update Successful.")
    
    # 3. Check CSV
    df = pd.read_csv("data/dock_status.csv")
    if "🧪 테스트 부두 99" not in df["구역/도크"].values:
        print("❌ Dock not found in CSV.")
        return
    print("✅ [Storage] CSV Data Integrity Verified.")
    
    # 4. Check HTML
    # We wait a bit for the rendering to finish (though it's synchronous in our API)
    r = requests.get(f"{url_base}/smart_yard_dashboard.html")
    if "🧪 테스트 부두 99" not in r.text:
        print("❌ Dock not found in Dashboard HTML.")
        return
    print("✅ [Viz] Dashboard Hot-Reload Verified.")
    
    print("\n" + "="*50)
    print("🚀 ALL API INTEGRATION TESTS PASSED (v26.3.0)")
    print("="*50)

if __name__ == "__main__":
    try:
        test_integration()
    except Exception as e:
        print(f"❌ Critical Error during test: {e}")
