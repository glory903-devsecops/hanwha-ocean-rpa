import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

def generate_dock_status():
    locations = ["거제 제1도크", "거제 제2도크", "거제 제3도크", "통영 야드 A", "통영 야드 B", "옥포 특수선 구역"]
    vessel_types = ["LNGC (LNG 운반선)", "VLCC (초대형 원유운반선)", "Container (컨테이너선)", "Submarine (잠수함)", "Ammonia Carrier"]
    tasks = ["선체 용접", "엔진 설치", "도장 작업", "시운전 준비", "의장 작업", "탑재 공정", "설계 검토"]
    safety_issues = ["없음", "없음", "없음", "없음", "강풍 경보", "미세먼지 주의", "낙하물 주의", "고온 작업 주의"]
    
    data = []
    # Generate 35 records for a "massive" feel
    for i in range(1, 36):
        loc = random.choice(locations)
        vessel = random.choice(vessel_types)
        progress = round(random.uniform(10.0, 98.0), 1)
        data.append({
            "ID": f"H-OS-{i:03d}",
            "구역/도크": loc,
            "건립선종": vessel,
            "공정률": progress,
            "현재작업": random.choice(tasks),
            "안전이슈": random.choice(safety_issues),
            "마지막업데이트": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    df = pd.DataFrame(data)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "dock_status.csv")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ Created {output_path} with {len(df)} rows of localized data.")

def generate_safety_training():
    names = ["김철수", "이영희", "박지민", "최동석", "정수아", "홍길동", "강현우", "윤미래", "조세호", "임지연", 
             "박상면", "한소희", "이상혁", "김연경", "손흥민", "봉준호", "송강호", "배수지", "남주혁", "아이유"]
    teams = ["선체조립1팀", "엔진기술팀", "도장설비팀", "시운전팀", "의장지원팀", "특수선설계팀"]
    
    data = []
    for name in names:
        data.append({
            "이름": name,
            "팀": random.choice(teams),
            "이수여부": random.choice(["이수", "이수", "이수", "미이수"]), # 75% compliance
            "교육일자": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        })
    
    df = pd.DataFrame(data)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "..", "data")
    output_path = os.path.join(output_dir, "safety_training_master.xlsx")
    df.to_excel(output_path, index=False, sheet_name="safety_training_master")
    print(f"✅ Created {output_path} with {len(df)} employee records.")

if __name__ == "__main__":
    print("📊 Generating localized massive dataset for Hanwha Ocean...")
    generate_dock_status()
    generate_safety_training()
    print("✨ Comprehensive AX Data Generation Complete.")
