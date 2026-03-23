from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

# 설정
options = Options()
options.add_argument("--headless")  # 화면 없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. 가상 포털 접속 (로컬 파일)
    file_path = "file://" + os.path.abspath("mock_portal.html")
    print(f"🌐 가상 포털 접속 중: {file_path}")
    driver.get(file_path)
    time.sleep(2)  # 로딩 대기

    # 2. 데이터 추출 (테이블 읽기)
    table = driver.find_element(By.TAG_NAME, "table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    data = []
    # 첫 번째 줄(헤더) 제외하고 데이터 수집
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 0:
            data.append({
                "도크": cols[0].text,
                "공정률": float(cols[1].text),
                "현재작업": cols[2].text,
                "안전이슈": cols[3].text
            })

    # 3. 데이터 저장 (CSV)
    df = pd.DataFrame(data)
    output_path = "data/dock_status.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"📊 데이터 수집 완료 및 저장: {output_path}")
    print(df)

finally:
    driver.quit()
    print("🔚 RPA 작업을 종료합니다.")
