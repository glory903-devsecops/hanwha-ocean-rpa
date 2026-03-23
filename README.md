# 🚢 Hanwha Ocean Smart Yard AX Portfolio

이 프로젝트는 한화오션의 **AX(AI Transformation) 전략**에 맞추어, 조선소 현장의 자율 주행 데이터 수집(RPA)과 인공지능 기반 공정 예측 시각화 시스템을 구축한 포트폴리오 프로젝트입니다.

## 🌟 주요 특징 (Key Features)

### 1. "One-Click" 하이엔드 대시보드 (`auto_dashboard.py`)
- **Premium UI**: 기업 브랜딩(Hanwha Orange) 및 사용자 경험을 극대화한 다크 모드 인터페이스.
- **Predictive AX**: 현재 공정률 데이터를 기반으로 실시간 완공 예정(D-Day)을 시뮬레이션하고 시각화합니다.
- **Interactive Graphs**: Plotly를 사용하여 각 도크별 상세 조업 현황을 탐색할 수 있습니다.

### 2. 하이브리드 데이터 수집 파이프라인
- **RPA 모듈 (`rpa_bot.py`)**: Selenium을 활용하여 가상 공정 포털에서 실시간 공정 현황을 자동으로 수집(Scraping)합니다.
- **샘플 데이터 생성기 (`generate_pbi_data.py`)**: 대규모 야드 환경을 시뮬레이션하기 위해 10개 이상의 도크 데이터를 대량 생성합니다.

### 3. 무결성 검증 및 DAX 최적화
- **Verification (`test_pbi_ready.py`)**: 수집된 데이터가 분석 시스템(Power BI 등)에 적합한지 자동으로 사전 검증합니다.
- **DAX 레시피**: Power BI Desktop 활용 시 즉시 적용 가능한 고급 수식(`DAX_SNIPPETS.md`)을 제공합니다.

## 🛠 기술 스택 (Tech Stack)

- **Language**: Python 3.x
- **Automation**: Selenium, Webdriver-manager
- **Data Analysis**: Pandas, Numpy
- **Visualization**: Plotly (Interactive HTML)
- **Business Intelligence**: Power BI Desktop (DAX Integration)

## 🚀 시작하기 (Quick Start)

가상 환경(venv)이 설정된 상태에서 아래 명령어를 실행하면 데이터 생성부터 대시보드 브라우저 출력까지 한 번에 완료됩니다.

```bash
cd hanwha-ocean-rpa
./venv/bin/python3 auto_dashboard.py
```

## 📂 프로젝트 구조

```text
├── hanwha-ocean-rpa/
│   ├── data/                 # 수집 및 생성된 데이터 (CSV, Excel)
│   ├── rpa_bot.py           # RPA 봇 스크립트
│   ├── auto_dashboard.py    # 통합 자동화 대시보드 엔진
│   ├── generate_pbi_data.py # 샘플 데이터 생성기
│   ├── test_pbi_ready.py    # 데이터 무결성 검증 스크립트
│   ├── DAX_SNIPPETS.md      # Power BI용 DAX 수식 가이드
│   └── README.md            # 프로젝트 가이드
└── CONVERSATION_HISTORY.md   # 전체 대화 및 개발 히스토리 요약
```

---
*Developed as part of the Hanwha Ocean IT Systems Development Portfolio.*
