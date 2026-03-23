import pandas as pd
import os

# 디렉토리 생성
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 가상의 협력사 및 직원 데이터 생성
data = {
    "협력사명": ["한화테크", "오션마린", "그린공업", "블루조선", "화이트물류"],
    "직원명": ["김철수", "이영희", "박지민", "최두식", "한소룡"],
    "직무": ["용접", "도장", "배관", "설계", "검사"],
    "안전교육만료일": ["2026-04-15", "2026-03-30", "2026-05-20", "2026-03-25", "2026-06-10"],
    "연락처": ["test1@example.com", "test2@example.com", "test3@example.com", "test4@example.com", "test5@example.com"]
}

df = pd.DataFrame(data)
file_path = os.path.join(data_dir, "safety_training_master.xlsx")
df.to_excel(file_path, index=False)

print(f"✅ 가상 안전 교육 마스터 데이터 출력 완료: {file_path}")
