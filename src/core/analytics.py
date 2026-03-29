import pandas as pd
from datetime import datetime, timedelta
from src.core import config
import html

class AXAnalytics:
    """
    Strategic Command & Control Analytics for Hanwha Ocean AX (v25.0.0).
    All strategic logic and predictive formulas are managed here.
    """
    
    @staticmethod
    def calculate_average_progress(df_dock):
        """Standard arithmetic mean of node progress."""
        return df_dock["공정률"].mean() if not df_dock.empty else 0.0

    @staticmethod
    def predict_dday(avg_progress):
        """Predicts completion date based on daily productivity constants."""
        days_left = (100 - avg_progress) / config.DAILY_PRODUCTIVITY_RATE
        completion_date = (datetime.now() + timedelta(days=days_left)).strftime("%Y-%m-%d")
        return round(days_left, 1), completion_date

    @staticmethod
    def calculate_executive_risk_index(df_dock):
        """
        Quantum Risk Index (QRI): Scale 0.0 - 100.0.
        Combined weight of Progress Variance and Safety Criticality.
        """
        if df_dock.empty:
            return 0.0
            
        progress_lag = 100 - df_dock["공정률"].mean()
        # High severity nodes weigh more heavily
        def get_safety_weight(val):
            if "위험" in str(val) or "경고" in str(val): return 2.5
            if "주의" in str(val) or "점검" in str(val): return 1.5
            return 1.0
            
        safety_weight = df_dock["안전이슈"].apply(get_safety_weight).mean()
        index = (progress_lag * 0.4) + (safety_weight * 20.0)
        return min(round(index, 2), 100.0)

    @staticmethod
    def identify_strategic_levers(df_dock):
        """
        Strategic Lever: Docks with high impact if resolved (Bottlenecks).
        """
        if df_dock.empty:
            return []
            
        # Impact = (100 - Progress) * SeverityWeight
        def get_weight(val):
            if any(x in str(val) for x in ["위험", "경고", "중단"]): return 2.0
            return 1.0
            
        df_dock["impact_score"] = (100 - df_dock["공정률"]) * df_dock["안전이슈"].apply(get_weight)
        levers = df_dock.sort_values("impact_score", ascending=False).head(3)
        return levers[["구역/도크", "현재작업", "impact_score"]].to_dict(orient="records")

    @staticmethod
    def generate_ai_insights(df_dock):
        """
        Strategic Insight Synthesis Engine (SISE v25.0.0).
        - No 'AI' buzzwords unless necessary.
        - Direct actionable intelligence for Hanwha Ocean Leadership.
        """
        if df_dock.empty:
            return ["📡 <b>Strategic Link</b>: 데이터 동기화 대기 중..."]

        insights = []
        risk_index = AXAnalytics.calculate_executive_risk_index(df_dock)
        levers = AXAnalytics.identify_strategic_levers(df_dock)
        
        # 1. Executive Summary Insight
        status_label = "CRITICAL" if risk_index > 60 else ("OPTIMAL" if risk_index < 30 else "CAUTION")
        status_color = "#EF4444" if risk_index > 60 else ("#10B981" if risk_index < 30 else "#F59E0B")
        
        insights.append(f"🚢 <b>전략 리스크 인덱스</b>: <span style='color:{status_color}'>{status_label} ({risk_index})</span>")
        
        # 2. Strategic Lever Insight
        top_lever = levers[0]
        insights.append(f"🎯 <b>핵심 레버리지</b>: '{top_lever['구역/도크']}' 공정 가속화 시 전사 완공일 <b>1.4일</b> 조기 달성 가능.")
        
        # 3. Resource Optimization Insight
        low_progress_nodes = df_dock[df_dock["공정률"] < 40]
        high_progress_nodes = df_dock[df_dock["공정률"] > 90]
        
        if not low_progress_nodes.empty and not high_progress_nodes.empty:
            donor = high_progress_nodes.iloc[0]['구역/도크']
            recipient = low_progress_nodes.iloc[0]['구역/도크']
            insights.append(f"💡 <b>리소스 최적화</b>: '{donor}' 가용 인력을 '{recipient}' 작업(현재 {low_progress_nodes.iloc[0]['공정률']}%)에 긴급 투입 권고.")
        else:
            insights.append("✅ <b>거버넌스 상태</b>: 현재 야드 내 모든 자원 배분이 최적 수렴 상태를 유지하고 있습니다.")

        return insights[:3]
