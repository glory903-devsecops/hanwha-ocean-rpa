import pandas as pd
import os
import json
import datetime
import sys

# 프로젝트 루트 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.viz.dashboard import DashboardEngine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCK_CSV = os.path.join(DATA_DIR, "dock_status.csv")
GUIDE_CSV = os.path.join(DATA_DIR, "safety_guidelines.csv")

def verify_integration():
    """Verify core cross-site logic (CSV to Dashboard) manually via asserts."""
    print("🧪 Starting Hanwha Ocean AX v26.0.0 Manual Integration Test...")
    
    # 1. Update Mock Data
    test_dock = "거제 제1도크"
    test_progress = 97.7
    test_task = "최종 점검 완료"
    test_safety = "정상"
    
    df = pd.read_csv(DOCK_CSV)
    mask = df["구역/도크"] == test_dock
    df.loc[mask, "공정률"] = test_progress
    df.loc[mask, "현재작업"] = test_task
    df.loc[mask, "안전이슈"] = test_safety
    df.to_csv(DOCK_CSV, index=False)
    print(f"✅ CSV updated for: {test_dock}")
    
    # 2. Trigger Re-render
    engine = DashboardEngine()
    engine.render()
    print("✅ Dashboard Re-rendered.")
    
    # 3. Verify HTML output
    with open(os.path.join(BASE_DIR, "smart_yard_dashboard.html"), "r", encoding="utf-8") as f:
        content = f.read()
        assert test_dock in content
        assert str(test_progress) in content
    print("✅ Dashboard HTML contains updated data.")
    
    print("\n" + "="*50)
    print("🚀 ALL INTEGRATION TESTS PASSED (v26.0.0)")
    print("="*50)

if __name__ == "__main__":
    try:
        verify_integration()
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        sys.exit(1)
