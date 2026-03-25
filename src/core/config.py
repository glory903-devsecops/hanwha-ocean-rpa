import os

# System & Branding Configuration (v4.5.0)
PROJECT_NAME = "Hanwha Ocean Smart Yard AX"
VERSION = "4.5.0"
AUTHOR = "Hanwha Ocean AX Team"

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

# UI Layout & Spatial Rhythm Constants (v4.5.0 Precision)
DASHBOARD_HEIGHT = 1200
LAYOUT_PADDING = 30 # Uniform margin/padding (20-30px range)
TITLE_FONT_SIZE = 28
VERTICAL_SPACING = 0.12 # Increased for "breathable" design
ROW_HEIGHTS = [0.2, 0.5, 0.3] # Optimized for vertical scanning
GAUGE_TEXT_SIZE = 48
DDAY_TEXT_SIZE = 50
CHART_TICK_SIZE = 18 # v4.4.0 Higher visibility

# [Bilingual Labels] (v4.3 Logo Branding)
LABELS = {
    "title": "한화오션 Smart Yard AX Command Center",
    "subtitle_overall": "야드 전체 공정률",
    "subtitle_dday": "예상 완공일",
    "subtitle_bar": "도크별 진척 현황",
    "subtitle_safety": "실시간 안전 감시",
    "subtitle_ai": "🤖 AI 의사결정 지원",
    "header_ai_insight": "<b>AI 분석 결과 및 권장 조치</b>"
}
