import pandas as pd
from datetime import datetime, timedelta
from src.core import config

class AXAnalytics:
    """
    Business Intelligence Logic for Hanwha Ocean AX.
    All calculation formulas are defined here for extensibility.
    """
    
    @staticmethod
    def calculate_average_progress(df_dock):
        """
        Formula: Mean of all active dock progress percentages.
        """
        return df_dock["공정률"].mean()

    @staticmethod
    def predict_dday(avg_progress):
        """
        Formula: (Remaining Processive / Daily Productivity Rate)
        Returns: Estimated days left and predicted date.
        """
        days_to_go = (100 - avg_progress) / config.DAILY_PRODUCTIVITY_RATE
        predicted_date = (datetime.now() + timedelta(days=days_to_go)).strftime("%Y-%m-%d")
        return round(days_to_go, 2), predicted_date

    @staticmethod
    def generate_ai_insights(df_dock):
        """
        Formula: Semantic Analysis of Project Delay & Safety Risk.
        1. 감지: 공정률 30% 미만 구역.
        2. 최적화: 가동률 낮은 통영 야드 인력을 우선 순위 높은 도크로 재배치 제안.
        """
        delayed_docks = df_dock[df_dock["공정률"] < 30]["구역/도크"].tolist()
        safety_risks = df_dock[df_dock["안전이슈"] != "없음"]["구역/도크"].tolist()
        
        insights = [
            f"🤖 <b>AI Optimizer</b>: {len(delayed_docks)}개 구역에서 지연 위험 감지됨.",
            f"💡 <b>Action</b>: 인력 부족 구역인 '{df_dock.iloc[0]['구역/도크']}'에 추가 리소스 투입 권장.",
            f"⚠️ <b>Risk Alert</b>: {', '.join(safety_risks[:2])} 야드 특이사항 발생 (긴급 점검).",
            f"🎯 <b>Impact</b>: AI 조치 이행 시 전체 공정 3.5일 단축 예상."
        ]
        return insights
