import os

# [Project Identity]
PROJECT_NAME = "Hanwha Ocean Smart Yard AX"
VERSION = "4.0.0"
AUTHOR = "한화오션 Smart Yard AX Team"

# [Branding: Hanwha CI]
COLOR_ORANGE = "#eb6e00"
COLOR_NAVY = "#002c5f"
COLOR_BACKGROUND = "#121212"
COLOR_TEXT = "#FFFFFF"
COLOR_ACCENT = "#00FFFF" # Cyan for AI Insights

# [Paths: Absolute for Reliability]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SRC_DIR = os.path.join(BASE_DIR, "src")

# [Yard Constants]
LOCATIONS = ["거제 제1도크", "거제 제2도크", "거제 제3도크", "통영 야드 A", "통영 야드 B", "옥포 특수선 구역"]
VESSEL_TYPES = ["LNGC (LNG 운반선)", "VLCC (초대형 원유운반선)", "Container (컨테이너선)", "Submarine (잠수함)", "Ammonia Carrier"]
TASKS = ["선체 용접", "엔진 설치", "도장 작업", "시운전 준비", "의장 작업", "탑재 공정", "설계 검토"]

# [Business Logic / Formulas]
# DAILY_PRODUCTIVITY_RATE: The estimated progress percentage completed per day for the entire yard.
DAILY_PRODUCTIVITY_RATE = 1.8 

# [Dashboard UI Config]
DASHBOARD_HEIGHT = 1200
VERTICAL_SPACING = 0.12 # v3.1 Fine-tuned for multi-device readability
ROW_HEIGHTS = [0.22, 0.45, 0.33]
GAUGE_TEXT_SIZE = 34
DDAY_TEXT_SIZE = 48
CHART_TICK_SIZE = 16 # v3.1 Extra Large for massive visibility

# [Bilingual Labels] (v3.0 Rebranded)
LABELS = {
    "title": "🚢 한화오션 Smart Yard AX Command Center (v3.0)",
    "subtitle_overall": "Overall Yard Process (야드 전체 공정률)",
    "subtitle_dday": "Projected Completion D-Day (예상 완공일)",
    "subtitle_bar": "Localized Yard Progress Status (도크별 진척 현황)",
    "subtitle_safety": "Real-time Safety Alert Monitor (실시간 안전 감시)",
    "subtitle_ai": "🤖 AI Decision Support Panel (AI 의사결정 지원)",
    "header_ai_insight": "<b>AI Insight & Guidance (분석 결과 및 권장 조치)</b>"
}
