# 📏 Hanwha Ocean AX Data Dictionary & Metrics (v2.5)

본 프로젝트에서 사용되는 핵심 데이터 필드와 AI 연산 공식(Formula)을 상세히 기술합니다.

## 1. Data Dictionary

| 필드명 (Field) | 타입 | 설명 | 비고 |
| :--- | :--- | :--- | :--- |
| **구역/도크** | String | 조업이 진행 중인 사업장 명칭 | 거제/통영/옥포 야드 포함 |
| **공정률** | Float | 해당 구역의 누적 진척도 (%) | 0.0 ~ 100.0 |
| **안전이슈** | String | 현장 센서 및 보고를 통해 감지된 위험 요소 | "없음", "낙하물", "강풍" 등 |
| **현재작업** | String | 현재 진행 중인 주력 작업 공종 | 용접, 도장, 시운전 등 |

## 2. Calculation Formulas (Business Logic)

### 📊 통합 공정률 (Overall Yard Process)
한화오션 전체 야드의 평균적인 진행 상태를 나타냅니다.
- **Formula**: `Avg(Progress_All_Docks)`
- **Logic**: 모든 도크의 공정률 합계를 전체 도크 수로 나눈 산술 평균값.

### 🔮 예상 완공일 예측 (Projected D-Day)
현재와 같은 생산성이 유지될 때의 완공 시점을 AI가 시뮬레이션합니다.
- **Formula**: `D-Day = (100 - Current_Progress) / Daily_Productivity_Rate`
- **Constant**: `Daily_Productivity_Rate` = 1.8% (과거 실적 기반 가중치 적용)
- **Result**: 오늘 날짜 + `D-Day` = 예상 완공일(Expected Date)

### 🤖 AI 의사결정 지원 (AI Insights)
데이터 패턴 분석을 통해 최적의 조치 사항을 제안합니다.
- **Logic 1 (Optimization)**: `If Progress < 30% AND Resource == Low THEN Suggest(Reallocation)`
- **Logic 2 (Safety)**: `If Weather == Alert OR Safety_Issue != None THEN Suggest(Immediate_Check)`

## 3. DB Integration Reference
Power BI 연동 시 데이터 형식(Data Type)이 불일치할 경우 수식이 오류가 날 수 있으므로, CSV 로드 시 공정률은 반드시 **'십진수(Decimal Number)'**로 설정해야 합니다.
