import pandas as pd
import random
import os
from datetime import datetime, timedelta
from src.core import config

def generate_enterprise_datasets():
    print(f"📦 [DataEngine] Generating Massive Enterprise Datasets (v{config.VERSION})...")
    
    # 1. Dock Progress Data
    data = []
    for i in range(1, 41): # 40 records for "Massive" scale
        loc = random.choice(config.LOCATIONS)
        vessel = random.choice(config.VESSEL_TYPES)
        # Weighted simulation formula: random base + block variance
        progress = round(random.uniform(15.0, 96.0), 1)
        data.append({
            "ID": f"H-OS-{i:03d}",
            "구역/도크": loc,
            "건립선종": vessel,
            "공정률": progress,
            "현재작업": random.choice(config.TASKS),
            "안전이슈": random.choice(["없음", "없음", "없음", "낙하물 주의", "강풍 경보", "없음"]),
            "마지막업데이트": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    df_dock = pd.DataFrame(data)
    os.makedirs(config.DATA_DIR, exist_ok=True)
    df_dock.to_csv(os.path.join(config.DATA_DIR, "dock_status.csv"), index=False, encoding="utf-8-sig")
    
    # 2. Safety Training Data
    names = ["김철수", "이영희", "박지민", "최동석", "정수아", "홍길동", "배수지", "남주혁", "아이유", "손흥민"]
    safety_data = []
    for name in names:
        safety_data.append({
            "이름": name,
            "팀": "한화오션 공정관리팀",
            "이수여부": random.choice(["이수", "이수", "미이수"]),
            "교육일자": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        })
    
    df_safety = pd.DataFrame(safety_data)
    df_safety.to_excel(os.path.join(config.DATA_DIR, "safety_training_master.xlsx"), index=False)
    
    print(f"✅ Created massive datasets in: {config.DATA_DIR}")

if __name__ == "__main__":
    generate_enterprise_datasets()
