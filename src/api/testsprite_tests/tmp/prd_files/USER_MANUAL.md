# [USER MANUAL] Hanwha Ocean AX Dashboard Operation

본 문서는 개발자 및 운영자가 시스템을 구동하고 결과를 해석하는 방법을 안내합니다.

## 1. 환경 설정 (Setup)
- **Python 설치**: 3.9 버전 이상 권장.
- **의존성 설치**: 가상 환경 활성화 후 아래 명령 실행.
  ```bash
  pip install pandas numpy selenium plotly webdriver-manager openpyxl
  ```

## 2. 시스템 구동 (Execution)
통합 자동화 스크립트를 통해 한 번에 실행 가능합니다.

```bash
# 1. 데이터 파이프라인 엔진 구동
python src/main.py

# 2. 독립 웹 서버 실행 (Port 8081)
python run_server.py
```
*자산 모니터링 시스템(8000)과 다른 별도의 실행 환경입니다.*

## 3. 대시보드 해석 가이드 (Bilingual Support)
- **Overall Yard Process (야드 전체 공정률)**: 현재 야드 전체의 평균 진척도입니다. 50% 미만 시 주황색 주의 단계입니다.
- **Projected Completion Date (예상 완공일)**: 현재 조업 속도를 유지할 때 100% 완료가 예상되는 지점입니다. (D-Day 인디케이터 제공)
- **Real-time Safety Alert (실시간 안전 감시)**: '안전이슈' 탭에 경고가 뜬 도크는 즉시 현장 점검이 필요합니다.

## 4. Power BI (Windows) 데이터 관리 가이드
윈도우 환경에서 `data/` 폴더의 데이터를 활용해 실규모 BI 리포트를 구축하고 관리하는 심화 방법입니다.

### 4.1 데이터 로드 및 관계 설정 (Data Relationship)
1.  **데이터 가져오기**: `dock_status.csv`와 `safety_training_master.xlsx`를 모두 로드합니다.
2.  **모델 뷰**: 두 테이블 간에 관련 필드가 있을 경우(예: 구역 ID 등) 관계를 설정하여 통합 분석이 가능하게 합니다.

### 4.2 주요 BI 지표 연산 (DAX Metrics)
Power BI 내에서 '새 측정값'을 생성하여 아래 수식을 적용하면 동적인 분석이 가능합니다.

*   **평균 공정률**: `Avg_Progress = AVERAGE('dock_status'[공정률])`
*   **위험 구역 개수**: `Risk_Count = CALCULATE(COUNT('dock_status'[ID]), 'dock_status'[공정률] < 30)`
*   **안전 미이수자 현황**: `Uncertified_Staff = CALCULATE(COUNT('safety_master'[이름]), 'safety_master'[이수여부] = "미이수")`

### 4.3 자동 새로고침 및 데이터 관리 (Automation)
- **로컬 데이터 원본**: 데이터 소스 설정(Data Source Settings)에서 파일 경로를 `C:\Users\...` 식의 **절대 경로**로 고정하십시오.
- **새로고침**: RPA 봇(`src/main.py`)이 실행되어 CSV가 갱신되면, Power BI 상단의 **[새로고침]** 버튼 클릭 시 모든 가구가 즉시 업데이트됩니다.

### 4.4 데이터 거버넌스 (Data Governance)
- **히스토리 관리**: `data/` 폴더의 CSV는 실행 시마다 덮어쓰기됩니다. 과거 데이터를 보관하려면 RPA 코드 내에서 날짜별 백업 로직을 활성화하여 `data/archive/` 폴더에 누적 관리하는 것을 권장합니다.

## 5. 트러블슈팅
- **Browser Error**: Chrome 브라우저 미설치 시 Selenium 작동이 중단될 수 있습니다.
- **Path Error**: 구글 드라이브 동기화 경로가 다를 경우 `os.path.abspath` 참조를 확인하십시오. (상대 경로 `/src/core/config.py` 참조)
- **Browser Error**: Chrome 브라우저 미설치 시 Selenium 작동이 중단될 수 있습니다.
- **Path Error**: 구글 드라이브 동기화 경로가 다를 경우 `os.path.abspath` 참조를 확인하십시오.
