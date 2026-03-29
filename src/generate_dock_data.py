import pandas as pd
import random
import os
from datetime import datetime, timedelta

def generate_v25_data():
    """Generates 50+ enterprise-scale yard nodes for Hanwha Ocean AX v25.0.0."""
    nodes = [
        # Docks
        "거제 제1도크", "거제 제2도크", "거제 제3도크", "거제 제4도크", "제5도크 (통영분관)",
        # Special Areas
        "옥포 특수선 구역 A", "옥포 특수선 구역 B", "옥포 특수선 구역 C", "특수선 시운전 구역",
        # Yards/Workshops
        "대형 가공 1공장", "대형 가공 2공장", "배관 블록 공장", "도장 1방", "도장 2방", "의장 부두 A", "의장 부두 B",
        # Logistics
        "중량물 하역장", "강재 저장소 A", "강재 저장소 B", "RPA 로봇 충전 스테이션",
        # Offshore
        "해상풍력 구역 A", "해상풍력 구역 B", "해상 가공 플랫폼",
        # Nodes
        "North Yard Dock 1", "North Yard Dock 2", "South Yard Pier A", "South Yard Pier B",
        "Block Storage 1", "Block Storage 2", "Pipe Shop 1", "Pipe Shop 2", "Painting House 3",
        "Assembly Zone Alpha", "Assembly Zone Beta", "Assembly Zone Gamma", "Launch Way 1", "Launch Way 2",
        "Crane Track A", "Crane Track B", "Crane Track C", "E-Dock Service Area", "X-Dock Service Area",
        "Main Gate Logistics", "Export Pier Delta", "Security Block 1", "Security Block 2",
        "Strategic Resupply Zone", "AI Server Cluster Alpha", "Digital Twin Sync Hub"
    ]
    
    # Expand if not enough
    while len(nodes) < 60:
        nodes.append(f"Workshop Zone {len(nodes)-40}")

    tasks = ["설계 검토", "선체 조립", "도장 작업", "의장 작업", "배관 설치", "엔진 설치", "시운전", "최종 검사", "자재 대기", "로봇 순찰"]
    safety_issues = [
        "정상", "정상", "정상", "정상", "정상", # 50% Optimal
        "[주의] 강풍주의", "[위험] 낙하물 발생", "[주의] 분진 발생", "[위험] 크레인 오작동", "[경고] 유해가스 감지", 
        "[주의] 장비 점검", "[경고] 용접 불꽃 감지", "[주의] 화기 작업 주의"
    ]
    
    data = []
    base_time = datetime.now()
    
    for i, node in enumerate(nodes):
        progress = random.uniform(10, 95)
        # Higher index = more likely to be critical for the demo
        safety = random.choice(safety_issues) if i % 4 != 0 else "정상"
        
        # Real-time style timestamps across the last 2 hours
        timestamp = (base_time - timedelta(minutes=random.randint(0, 120))).strftime("%Y-%m-%d %H:%M:%S")
        
        data.append({
            "구역/도크": node,
            "공정률": round(progress, 1),
            "현재작업": random.choice(tasks),
            "안전이슈": safety,
            "마지막업데이트": timestamp
        })
        
    df = pd.DataFrame(data)
    
    # Ensure data directory
    if not os.path.exists("data"):
        os.makedirs("data")
        
    path = os.path.join("data", "dock_status.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"✨ v25.0.0 Enterprise Dataset Generated: {path} ({len(df)} nodes)")

if __name__ == "__main__":
    generate_v25_data()
