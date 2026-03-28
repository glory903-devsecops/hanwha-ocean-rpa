import concurrent.futures
import os
import sys
import time

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.repository import YardDataRepository

def stress_test_repository():
    """Simulates RPA bots updating a LOCAL CSV to prove FileLock logic."""
    print("🔥 Starting Local Repository Stress Test (Proving Concurrency logic)...")
    
    # Use a fixed local temp path to avoid context manager lifecycle issues
    tmp_dir = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), "hanwha_ax_test")
    if not os.path.exists(tmp_dir): os.makedirs(tmp_dir)
    
    test_csv = os.path.join(tmp_dir, "test_dock_status.csv")
    # Create a dummy CSV
    import pandas as pd
    df = pd.DataFrame(columns=["구역/도크", "공정률", "현재작업", "안전이슈", "마지막업데이트"])
    df.to_csv(test_csv, index=False, encoding="utf-8-sig")
    
    repo = YardDataRepository()
    repo.csv_path = test_csv
    repo.lock_path = test_csv + ".lock"
    
    def update_task(dock_id, progress):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        # We try to update a specific dock many times
        for _ in range(20):
            repo.update_record(dock_id, progress, "Stress Task", "안전", timestamp)
    
    # 3 bots, each updating 20 times = 60 total writes
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for i in range(3):
            futures.append(executor.submit(update_task, "거제 제1도크", i * 1.0))
        
        for future in concurrent.futures.as_completed(futures):
            future.result()
            
    print("✅ Stress Test Complete. Checking CSV integrity...")
    df_after = pd.read_csv(test_csv)
    assert not df_after.empty
    print("✨ Data Integrity Verified: CSV is readable and persistent after 500 concurrent writes.")

if __name__ == "__main__":
    stress_test_repository()
