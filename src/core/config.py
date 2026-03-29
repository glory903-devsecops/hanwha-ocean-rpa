import os

# System & Branding Configuration (v25.0.0 - Enterprise Elite)
PROJECT_NAME = "Hanwha Ocean Smart Yard AX: Ultimate Mission Control"
VERSION = "25.0.0"
AUTHOR = "Hanwha Ocean AX Advanced Development Team"

# [Branding: Hanwha Ocean Premium]
BRAND_ORANGE = "#FF6A00"
BRAND_DARK = "#0B0F12"
COLOR_BACKGROUND = BRAND_DARK
COLOR_TEXT = "#FFFFFF"
COLOR_ACCENT = "#00FFFF" # Cyan for AI Insights

# [Paths: Absolute for Reliability]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SRC_DIR = os.path.join(BASE_DIR, "src")

# [Yard Constants]
LOCATIONS = [
    "거제 제1도크 (LNG)", "거제 제2도크 (VLCC)", "거제 제3도크", "거제 제1안벽", "거제 제2안벽", 
    "디지털 생산 센터", "스마트 야드 실증 센터", "에너지 시스템 실험 센터", "스마트 시운전 센터", 
    "특수선 전용 도크", "선행 도장 공장", "자동 배선 작업장", "통영 야드 A-1", "통영 야드 B-1"
]
VESSEL_TYPES = ["LNGC (LNG 운반선)", "VLCC (초대형 원유운반선)", "Container (컨테이너선)", "Submarine (잠수함)", "Ammonia Carrier", "Corvette"]
TASKS = ["선체 용접", "도장 작업", "블록 배치", "의장 작업", "탑재 공정", "엔진 설치", "시운전", "비파괴 검사", "안전 점검"]

# [Safety Categories - Expanded for ERP]
SAFETY_CATEGORIES = [
    "화재 발생 (작업 중단)",
    "가스 누출 탐지 (대피)",
    "강풍 경보 (크레인 중단)",
    "낙하물 주의 (보호구 필수)",
    "크레인 정기 점검 중",
    "미확인",
    "안전"
]

# [Status Color Palette]
SAFETY_COLOR_MAP = {
    "화재 발생 (작업 중단)": "rgba(255, 0, 0, 0.7)", # Red-ish
    "가스 누출 탐지 (대피)": "rgba(255, 0, 0, 0.7)",
    "강풍 경보 (크레인 중단)": "rgba(255, 0, 0, 0.7)",
    "낙하물 주의 (보호구 필수)": "rgba(255, 60, 60, 0.6)", # Lighter Red
    "미확인": "rgba(100, 100, 100, 0.6)", # Gray
    "안전": "rgba(0, 0, 0, 0)" # Transparent/Dark
}

# [Business Logic / Formulas]
# DAILY_PRODUCTIVITY_RATE: The estimated progress percentage completed per day for the entire yard.
DAILY_PRODUCTIVITY_RATE = 1.8 

# UI Layout & Spatial Rhythm Constants (v4.5.0 Precision)
DASHBOARD_HEIGHT = 1200
LAYOUT_PADDING = 30 # Uniform margin/padding (20-30px range)
# [Typography: +5pt Increase as requested]
TITLE_FONT_SIZE = 37 # 32 + 5
BODY_FONT_SIZE = 23 # 18 + 5
VERTICAL_SPACING = 0.12 
ROW_HEIGHTS = [0.2, 0.8] # 2-row layout (Header + Full Chart)
GAUGE_TEXT_SIZE = 48 # Yard Progress text size stays as requested
DDAY_TEXT_SIZE = 45 # 40 + 5 approx
CHART_TICK_SIZE = 23 # 18 + 5
BAR_LABEL_SIZE = 18 # Internal bar text

# [Bilingual Labels] (localized to 한화오션)
LABELS = {
    "title": "한화오션 Smart Yard AX Command Center",
    "subtitle_overall": "야드 전체 공정률",
    "subtitle_dday": "예상 완공일",
    "subtitle_bar": "도크별 진척 현황",
    "header_progress": "공정률 (%)",
    "header_task": "현재 작업"
}
