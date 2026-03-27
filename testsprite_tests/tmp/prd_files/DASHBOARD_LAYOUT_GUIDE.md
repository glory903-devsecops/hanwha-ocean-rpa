# 🎨 Hanwha Ocean AX Dashboard Layout Customization Guide

본 문서는 `DashboardEngine`의 레이아웃을 직접 수정하고자 하는 사용자를 위한 가이드입니다. 시각적 요소의 배치와 간격은 주로 두 개의 파일에서 관리됩니다.

## 1. 핵심 설정 파일 (`src/core/config.py`)

대시보드의 전체적인 비율과 간격은 `config.py`에서 전역 상수로 관리됩니다.

```python
# [Dashboard UI Config]
DASHBOARD_HEIGHT = 1200          # 전체 높이 (픽셀)
VERTICAL_SPACING = 0.08          # 행(Row) 사이의 수직 간격 비율 (0.0~1.0)
ROW_HEIGHTS = [0.22, 0.40, 0.30] # 각 행의 높이 비율 (합계가 1.0에 가까워야 함)
```

- **ROW_HEIGHTS**: 순서대로 **상단(지표), 중단(막대그래프), 하단(테이블/AI)**의 높이 비율입니다. 
- **VERTICAL_SPACING**: 행 간의 물리적 거리가 너무 가깝거나 멀 때 이 값을 조정하세요.

---

## 2. 엔진 로직 파일 (`src/viz/dashboard.py`)

개별 요소의 정밀한 좌표(Annotation)와 데이터 개수는 `dashboard.py`에서 관리됩니다.

### 2.1 요소 배치 (Subplots)
`render()` 메서드 내의 `make_subplots` 설정이 전체 구조를 결정합니다.
```python
fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}], # 1행: 게이지, D-Day
        [{"colspan": 2}, None],                         # 2행: 막대그래프 (2칸 차지)
        [{"type": "table"}, {"type": "table"}]          # 3행: 안전 테이블, AI Insight
    ],
    ...
)
```

### 2.2 타이틀 및 캡션 좌표 (`add_annotation`)
사용자 피드백에 따라 가장 자주 수정하게 될 부분입니다. `y` 좌표를 통해 위아래 위치를 조정합니다.
```python
# y=1.0 (상단 끝) ~ y=0.0 (하단 끝)
fig.add_annotation(..., y=0.92, ...) # 상단 타이틀
fig.add_annotation(..., y=0.31, ...) # 하단 테이블 타이틀
```

### 2.3 데이터 표시 개수
막대그래프가 너무 촘촘하여 겹쳐 보인다면 표시 개수를 줄일 수 있습니다.
```python
df_bar = self.df_dock.head(14) # 상위 14개 구역만 표시 (기존 18개에서 축소됨)
```

---

## 3. 수정 프로세스
1. `config.py` 또는 `dashboard.py`의 수치를 변경합니다.
2. 터미널에서 파이프라인을 재실행합니다:
   ```bash
   ./venv/bin/python3 src/main.py
   ```
3. 생성된 `smart_yard_dashboard.html` 파일을 브라우저에서 열어 결과를 확인합니다.
