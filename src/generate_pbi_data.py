import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_dock_status():
    docks = [f"제{i}도크" for i in range(1, 11)]
    processes = [85.5, 42.0, 12.3, 95.0, 60.5, 33.2, 77.8, 15.0, 50.0, 5.5]
    tasks = ["선체 조립", "도장 작업", "블록 배치", "시운전 준비", "의장 작업", "용접 공정", "엔진 설치", "강재 절단", "탑재 작업", "설계 검토"]
    safety_issues = ["없음", "미세먼지 주의", "없음", "강풍 경보", "없음", "낙하물 주의", "없음", "없음", "고온 작업 주의", "없음"]
    
    data = {
        "도크": docks,
        "공정률": processes,
        "현재작업": tasks,
        "안전이슈": safety_issues,
        "마지막업데이트": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * 10
    }
    
    df = pd.DataFrame(data)
    # Get base directory (project root) relative to this script in src/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "dock_status.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ Created {output_path} with 10 rows.")

def generate_safety_training():
    names = ["김철수", "이영희", "박지민", "최동석", "정수아", "홍길동", "강현우", "윤미래", "조세호", "임지연"]
    teams = ["선체1팀", "도장A팀", "의장2팀", "품질관리", "안전보건"] * 2
    status = ["이수", "이수", "미이수", "이수", "이수", "미이수", "이수", "이수", "이수", "미이수"]
    dates = [(datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime("%Y-%m-%d") for _ in range(10)]
    
    data = {
        "이름": names,
        "팀": teams,
        "이수여부": status,
        "교육일자": dates
    }
    
    df = pd.DataFrame(data)
    df.to_excel("data/safety_training_master.xlsx", index=False, sheet_name="safety_training_master")
    print("✅ Created data/safety_training_master.xlsx with 10 rows (Sheet: safety_training_master).")

if __name__ == "__main__":
    print("📊 Generating realistic sample data for Power BI...")
    generate_dock_status()
    generate_safety_training()
    print("✨ Data generation complete.")
