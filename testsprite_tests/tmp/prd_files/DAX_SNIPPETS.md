# Power BI DAX Snippets & Data Import Guide (Windows)

이 문서는 파워 BI 데스크톱(Power BI Desktop)에서 한화오션 스마트 야드 대시보드를 구축할 때 필요한 주요 수식과 데이터 연결 방법을 안내합니다.

## 1. 데이터 가져오기 (Data Import)

현재 이 PC의 로컬 경로에 있는 데이터를 다음과 같이 연결하세요.

1. **실시간 도크 현황 (`dock_status.csv`)**
   - `데이터 가져오기` -> `텍스트/CSV` 선택
   - 경로: `G:\내 드라이브\99.Develop\한화오션\hanwha-ocean-rpa\data\dock_status.csv`
   - **Tip**: RPA가 파일을 업데이트할 때마다 파워 BI의 `새로 고침` 버튼을 누르면 실시간 반영됩니다.

2. **안전 교육 마스터 (`safety_training_master.xlsx`)**
   - `데이터 가져오기` -> `Excel 통합 문서` 선택
   - 경로: `G:\내 드라이브\99.Develop\한화오션\hanwha-ocean-rpa\data\safety_training_master.xlsx`

---

## 2. 주요 DAX 측정값 (Measures)

파워 BI의 `새 측정값` 기능을 사용하여 아래 수식들을 입력하세요.

### A. 야드 전체 평균 공정률
모든 도크의 공정 진행 상태를 백분율로 나타냅니다.
```dax
Overall Avg Process = AVERAGE('dock_status'[공정률]) / 100
```
*(파워 BI 상단에서 '백분율(%)' 형식을 지정하세요)*

### B. 안전 경보 발생 건수
'안전이슈'가 '없음'이 아닌 모든 항목의 개수를 셉니다.
```dax
Safety Alert Count = 
CALCULATE(
    COUNTROWS('dock_status'),
    'dock_status'[안전이슈] <> "없음"
)
```

### C. 교육 이수율 (Compliance Rate)
안전 교육 마스터 데이터를 기반으로 한 이수율 계산 예시입니다.
```dax
Training Compliance % = 
DIVIDE(
    CALCULATE(COUNTROWS('safety_training_master'), 'safety_training_master'[이수여부] = "이수"),
    COUNTROWS('safety_training_master'),
    0
)
```

---

## 3. 시각화 추천 구성
- **게이지(Gauge)**: `Overall Avg Process`를 사용하여 전체 야드 가동률 표시.
- **카드(Card)**: `Safety Alert Count`를 사용하여 현재 위험 요소 개수 강조.
- **누적 가로 막대형 차트**: '도크'별 '공정률' 시각화.

---
---

## 4. 고급 분석 (Advanced Analytics)

대시보드에 심도 있는 인사이트를 더하기 위한 고급 DAX 수식입니다.

### D. 예상 완공일 (Projected Completion Date)
현재 공정률과 업데이트 날짜를 기반으로 100% 달성 시점을 예측합니다 (단순 선형 예측).
```dax
Projected Completion = 
VAR CurrentProgress = AVERAGE('dock_status'[공정률]) / 100
VAR ProgressPerDay = 0.02 -- 일일 평균 진행률 가정 (데이터에 따라 조정 가능)
RETURN
IF(
    CurrentProgress < 1,
    TODAY() + ( (1 - CurrentProgress) / ProgressPerDay ),
    "완료"
)
```

### E. 안전 위험 지수 (Safety Risk Index)
도크별 안전 이슈의 심각도를 점수화합니다 (위험=10, 주의=5, 없음=0).
```dax
Safety Risk Index = 
SUMX(
    'dock_status',
    SWITCH(
        'dock_status'[안전이슈],
        "강풍 경보", 10,
        "고온 작업 주의", 5,
        "낙하물 주의", 8,
        "미세먼지 주의", 3,
        0
    )
)
```

---
*마지막 업데이트: 2026-03-23 (v1.1 - 고급 DAX 추가)*

