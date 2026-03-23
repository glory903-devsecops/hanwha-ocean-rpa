import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from src.core import config, analytics

class DashboardEngine:
    """
    Visualization Engine for Hanwha Ocean AX.
    Decoupled from data generation and business logic.
    """
    
    def __init__(self):
        self.analytics = analytics.AXAnalytics()
        self.config = config
        
    def load_data(self):
        self.df_dock = pd.read_csv(os.path.join(self.config.DATA_DIR, "dock_status.csv"))
        self.df_safety = pd.read_excel(os.path.join(self.config.DATA_DIR, "safety_training_master.xlsx"))

    def render(self):
        print(f"🎨 [VizEngine] Rendering Bilingual AX Dashboard (v{self.config.VERSION})...")
        self.load_data()
        
        # Calculate Metrics via Core Analytics
        avg_proc = self.analytics.calculate_average_progress(self.df_dock)
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        ai_insights = self.analytics.generate_ai_insights(self.df_dock)
        
        # Layout Setup (Manual Title Management for Absolute Control)
        fig = make_subplots(
            rows=3, cols=2,
            specs=[
                [{"type": "indicator"}, {"type": "indicator"}],
                [{"colspan": 2}, None],
                [{"type": "table"}, {"type": "table"}]
            ],
            vertical_spacing=self.config.VERTICAL_SPACING,
            row_heights=self.config.ROW_HEIGHTS
        )

        # Traces using Configured Branding & Minimalist Sizing (v2.5.5)
        fig.add_trace(go.Indicator(
            mode="gauge+number", value=avg_proc,
            number={'suffix': "%", 'font': {'color': self.config.COLOR_ORANGE, 'size': self.config.GAUGE_TEXT_SIZE}},
            gauge={'bar': {'color': self.config.COLOR_ORANGE}, 'bgcolor': "#333", 'axis': {'range': [0, 100]}},
            domain={'y': [0.1, 0.8], 'x': [0.1, 0.9]} 
        ), row=1, col=1)

        fig.add_trace(go.Indicator(
            mode="number", value=days_to_go,
            number={'prefix': "D-", 'font': {'color': self.config.COLOR_TEXT, 'size': self.config.DDAY_TEXT_SIZE}},
            title={'text': f"<br><span style='font-size:14px; color:#aaa'>Expected: {proj_date}</span>", 'font': {'size': 14}},
            domain={'y': [0.1, 0.8], 'x': [0.1, 0.9]}
        ), row=1, col=2)

        fig.add_trace(go.Bar(
            x=self.df_dock["구역/도크"] + "<br>(" + self.df_dock["건립선종"] + ")",
            y=self.df_dock["공정률"],
            marker_color=self.config.COLOR_ORANGE,
            text=self.df_dock["공정률"], textposition='outside'
        ), row=2, col=1)

        # Tables
        alert_df = self.df_dock[self.df_dock["안전이슈"] != "없음"].head(10)
        fig.add_trace(go.Table(
            header=dict(values=["도크/구역", "작업", "이슈"], fill_color=self.config.COLOR_ORANGE, font=dict(color='white')),
            cells=dict(values=[alert_df["구역/도크"], alert_df["현재작업"], alert_df["안전이슈"]], fill_color=self.config.COLOR_BACKGROUND, font=dict(color='white'))
        ), row=3, col=1)

        fig.add_trace(go.Table(
            header=dict(values=[self.config.LABELS["header_ai_insight"]], fill_color=self.config.COLOR_NAVY, font=dict(color='white')),
            cells=dict(values=[ai_insights], fill_color="#1a1a1a", font=dict(color=self.config.COLOR_ACCENT, size=13), align='left', height=40)
        ), row=3, col=2)

        # Hand-Tuned Professional Annotations (Zero Overlap)
        # Row 1 Titles
        fig.add_annotation(text=self.config.LABELS["subtitle_overall"], xref="paper", yref="paper", x=0.23, xanchor='center', y=1.0, showarrow=False, font=dict(size=17, color=self.config.COLOR_ORANGE))
        fig.add_annotation(text=self.config.LABELS["subtitle_dday"], xref="paper", yref="paper", x=0.77, xanchor='center', y=1.0, showarrow=False, font=dict(size=17, color=self.config.COLOR_ORANGE))
        # Row 2 Title
        fig.add_annotation(text=self.config.LABELS["subtitle_bar"], xref="paper", yref="paper", x=0.5, xanchor='center', y=0.71, showarrow=False, font=dict(size=17, color=self.config.COLOR_ORANGE))
        # Row 3 Titles
        fig.add_annotation(text=self.config.LABELS["subtitle_safety"], xref="paper", yref="paper", x=0.23, xanchor='center', y=0.34, showarrow=False, font=dict(size=17, color=self.config.COLOR_ORANGE))
        fig.add_annotation(text=self.config.LABELS["subtitle_ai"], xref="paper", yref="paper", x=0.77, xanchor='center', y=0.34, showarrow=False, font=dict(size=17, color=self.config.COLOR_ORANGE))

        fig.update_layout(
            paper_bgcolor=self.config.COLOR_BACKGROUND, plot_bgcolor=self.config.COLOR_BACKGROUND, 
            font=dict(color=self.config.COLOR_TEXT),
            title_text=self.config.LABELS["title"],
            title_font=dict(size=26, color=self.config.COLOR_ORANGE),
            title_x=0.5, title_y=0.97, # High and center
            height=self.config.DASHBOARD_HEIGHT, template="plotly_dark", showlegend=False,
            margin=dict(t=180, b=60, l=60, r=60) 
        )
        
        fig.update_xaxes(tickangle=45, tickfont=dict(size=9), row=2, col=1)

        output_path = os.path.join(self.config.BASE_DIR, "smart_yard_dashboard.html")
        fig.write_html(output_path)
        print(f"✨ Professionally Refactored Dashboard: {output_path}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
