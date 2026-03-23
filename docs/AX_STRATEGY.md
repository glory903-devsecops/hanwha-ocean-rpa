# 🧠 Hanwha Ocean AX Strategy & Roadmap (v2.5)

한화오션의 AX(AI Transformation) 전략을 기반으로 한 스마트 야드 구축 로직 및 중장기 로드맵을 정의합니다.

## 1. Vision & Goal
- **Vision**: "데이터 기반의 자율 지능형 야드 구축 (Autonomous Intelligent Yard)"
- **Goal**: 조업 데이터의 자동 수집(RPA), 지표 분석(AI), 직관적 의사결정(Dashboard) 환경 완성.

## 2. AX Architecture
본 프로젝트는 확장성을 고려하여 3계층 아키텍처로 설계되었습니다.

1.  **Data Engine Layer**: 포털 및 DB에서 데이터를 획득하고 정제하는 엔진.
2.  **Analytics Layer**: 수집된 원천 데이터를 비즈니스 지표(공정률, D-Day, 안전지수)로 변환하는 분석 엔진.
3.  **Visualization Layer**: 하이엔드 인터랙티브 시각화를 통해 통찰력(AI Insight)을 전달하는 계층.

## 3. Implementation Roadmap
- **Phase 1 (v1.x)**: "Smart Data Acquisition" - RPA 기반 데이터 자동화 및 기초 대시보드. (완료)
- **Phase 2 (v2.x)**: "Predictive Analytics" - AI 기반 D-Day 예측 및 의사결정 지원 가이드. (현재)
- **Phase 3 (v3.x)**: "Total Digital Twin" - 3D 모델 및 IoT 센서 실시간 연동 고도화. (계획)

## 4. Scalability Note 
모든 코드는 모듈화(`src/core`, `src/viz`)되어 있어, 향후 실제 DB(Oracle/SAP) 커넥터나 강화학습 기반 리소스 최적화 AI 모델을 추가할 때 핵심 아키텍처의 변경 없이 확장이 가능합니다.
