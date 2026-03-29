# 한화오션 Smart Yard AI/RPA 시스템 유지보수 가이드 (v18.0.0)

이 문서는 한화오션 AX 미션 컨트롤 센터의 지능형 운영 가이드 및 RPA 거버넌스 시스템의 구조와 유지관리 방법을 명시합니다.

## 1. 시스템 아키텍처
본 시스템은 **Data-Driven Logic Matrix** 구조를 채택하여, 코드 수정 없이 데이터 변경만으로 AI의 판단 기준을 제어할 수 있습니다.

### 핵심 구성 요소
- **Dashboard (src/viz/dashboard.py)**: 실시간 관제 UI 및 AI Action Balloon 인터랙션 엔진.
- **API Server (src/api/server.py)**: Fast API 기반의 거버넌스 CRUD API.
- **Admin Portal (src/viz/admin_guidance.html)**: 안전 전문가용 통합 거버넌스 허브.
- **Knowledge Base (data/safety_guidelines.csv)**: AI 대응 매뉴얼 및 RPA 트리거 기준 저장소.

## 2. RPA 거버넌스 및 확장
v18.0.0부터 도입된 RPA 필드는 자동화 연동의 근거가 됩니다.

| 필드명 | 용도 | 확장 팁 |
| :--- | :--- | :--- |
| `RPA_TRIGGER` | 자동화 봇 가동 조건 | 센서 데이터(예: DUST > 50)와 논리 연산자 사용 |
| `BOT_ID` | 담당 로봇 식별자 | 현장의 물리적인 봇 ID 또는 스케줄러 ID 매핑 |

## 3. 유닛 테스트 및 품질 관리
시스템 안정성을 위해 `tests/test_guidance_system.py`를 정기적으로 실행하십시오.

### 테스트 실행 방법
```powershell
python -m pytest tests/test_guidance_system.py
```
- **Lifecycle Test**: 가이드라인의 생성-수정-삭제-데이터 무결성 검증을 수행합니다.

## 4. 커스텀 UI/UX 가이드
대시보드의 AI Balloon(Hover)은 Alpine.js를 통해 제어됩니다.
- **Balloon 위치**: `showGuidance` 함수의 `rect.right + offset` 값을 통해 조정 가능합니다.
- **폰트 및 컬러**: Tailwind CSS 클래스(`text-4xl`, `text-orange-500` 등)를 통해 브랜드 가이드에 맞춰 수정하십시오.

---
**HANWHA OCEAN AX PROPRIETARY DOCUMENT - v18.0.0**
