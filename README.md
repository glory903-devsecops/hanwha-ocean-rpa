# 한화오션 Smart Yard AX: Operational Command Center (v16.0.0)

한화오션 야드 내 **20개 이상의 실전급 자산**을 실시간으로 분석하고, 심각도 및 작업 종류별로 관리할 수 있는 **엔터프라이즈 모빌리티 커맨드 센터**입니다.

---

## 🎥 차세대 운영 경험 (v16.0.0 Showroom)

본 버전에서는 대규모 야드 관제 효율성을 극대화하기 위해 **지능형 필터링 엔진**과 **확장된 타이포그래피**를 도입했습니다.

### [실시간 지능형 필터링]
![Filtering Demo](C:\Users\glory\AppData\Local\Temp\hanwha_ax_test\dashboard_risk_filter_applied_1774675392621.png)
*상태별 필터(ALL/위험/주의/정상) 및 실시간 검색을 통해 수십 개의 작업 노드 중 필요한 정보만 즉시 노출합니다.*

### [고해상도 다국어 지원 UI]
````carousel
![Full Asset Grid (20+ Nodes)](C:\Users\glory\AppData\Local\Temp\hanwha_ax_test\dashboard_top_v14_1_0_1774674800783.png)
<!-- slide -->
![Filtering in Action](C:\Users\glory\AppData\Local\Temp\hanwha_ax_test\dashboard_risk_filter_applied_1774675392621.png)
<!-- slide -->
![Stage 3: Video Walkthrough](C:\Users\glory\.gemini\antigravity\brain\93a8b5d7-60a2-4cde-bf05-a7b32dc1b02a\ax_v16_enterprise_demo_1774675353814.webp)
````

---

## 🚀 v16.0.0 핵심 고도화 기능

### 1. 실전급 야드 자산 확장 (Scale-Up)
- **20+ 전문 자산**: 제1~5도크, 의장안벽 A~E, 가공/조립/도장/선단/배관 공장 등 실제 조선소 규모의 20개 이상의 노드를 관리합니다.
- **데이터 정제**: 테스트용 GUID 및 더미 데이터를 제거하고 직관적인 한글 자산명을 부여했습니다.

### 2. 지능형 필터링 및 검색 엔진
- **Alpine.js 기반 필터**: 페이지 새로고침 없는 즉각적인 상태별 필터링(위험/주의/정상)을 지원합니다.
- **실시간 검색**: 작업 종류(예: '도장', '용접')나 구역명으로 노드를 즉시 검색하여 관제 피로도를 낮췄습니다.

### 3. 고시인성 타이포그래피 & 한글화
- **K-Shipyard 로컬라이징**: "Efficiency → 공정 도달율", "Task → 현재 작업" 등 전 UI를 현업 피드백을 반영한 한국어로 개편했습니다.
- **폰트 가독성**: 수치 외 모든 텍스트의 폰트 크기를 20% 확대하여 야드 관제 스크린에서도 시원하게 보이도록 최적화했습니다.

---

## 🛡️ 신뢰도 및 보안 인증 (QA Log)

- **Security (`test_security.py`)**: `PASSED` - 완벽한 XSS 방어 및 데이터 무결성 확보.
- **Concurrency (`test_concurrency.py`)**: `PASSED` - `SoftFileLock`을 통한 안정적인 멀티 봇 동시 작업 지원.

---

## 🧭 운영 블루프린트 (Document Links)

1.  **[현업 실효성 및 ROI 보고서](docs/PROJECT_FEASIBILITY_REPORT.md)**: 사업 비전 및 기대효과.
2.  **[디자이너 협업 가이드](docs/DASHBOARD_DESIGN_GUIDE.md)**: UI 테마(`theme.py`) 커스터마이징 매뉴얼.
3.  **[시스템 설계 사양서(SDD)](docs/SDD.md)**: 아키텍처 및 ETL 흐름도.

---

## 🛠️ 실행 가이드 (Quick Start)

본 프로젝트는 브라우저 보안 정책에 따라 **로컬 웹 서버** 구동을 권장합니다.
```bash
# 1. 의존성 설치
pip install pandas fastapi uvicorn filelock plotly pytest

# 2. 커맨드 센터 데이터 생성
python src/viz/dashboard.py

# 3. 로컬 서버 가동 (권장)
python -m http.server 8000
```
- **대시보드 접속**: [http://localhost:8000/smart_yard_dashboard.html](http://localhost:8000/smart_yard_dashboard.html)

---
*Developed by Hanwha Ocean AX High-End Portfolio Project (v16.0.0).*
