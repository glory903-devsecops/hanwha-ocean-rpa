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
# 한화오션 RPA 루트 폴더에서 실행
./venv/bin/python3 src/auto_dashboard.py
```

## 3. 대시보드 해석 가이드
- **Overall Yard Process**: 현재 야드 전체의 평균 진척도입니다. 50% 미만 시 주황색 주의 단계입니다.
- **Projected Completion Date**: 현재 조업 속도를 유지할 때 100% 완료가 예상되는 지점입니다. (D-Day 인디케이터 제공)
- **Real-time Safety Alert**: '안전이슈' 탭에 경고가 뜬 도크는 즉시 현장 점검이 필요합니다.

## 4. Power BI (Windows) 활용 가이드
윈도우 환경에서 `data/` 폴더의 데이터를 활용해 실무용 BI 리포트를 구축하는 방법입니다.

### 4.1 데이터 로드 (Import)
1.  **Power BI Desktop** 실행.
2.  **데이터 가져오기** -> **텍스트/CSV** 선택.
3.  `hanwha-ocean-rpa/data/dock_status.csv` 파일을 선택합니다.
4.  **데이터 변환** 클릭 후, '공정률' 컬럼의 데이터 형식이 '십진수'인지 확인합니다.

### 4.2 실시간 새로고침 설정
- 데이터 소스 설정 시 **상대 경로**가 아닌 **절대 경로**로 지정하면, RPA가 로컬 파일을 갱신할 때마다 Power BI에서 '새로고침' 버튼만 눌러 최신 지표를 반영할 수 있습니다.

### 4.3 권장 시각화 개체
- **게이지(Gauge)**: 야드 전체 평균 공정률 표기.
- **누적 가로 막대형 차트**: 도크별/선종별 진척도 비교.

## 5. 트러블슈팅
- **Browser Error**: Chrome 브라우저 미설치 시 Selenium 작동이 중단될 수 있습니다.
- **Path Error**: 구글 드라이브 동기화 경로가 다를 경우 `os.path.abspath` 참조를 확인하십시오.
