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
        
        # Layout Setup: 3-Row Grid System (v4.4.0)
        fig = make_subplots(
            rows=3, cols=2,
            specs=[
                [{"type": "indicator"}, {"type": "indicator"}], # Gauge (L) / Padding (R)
                [{"colspan": 2}, None],                         # Pro Bar Chart (Center)
                [{"type": "table"}, {"type": "table"}]          # Bimodal Analysis (L/R)
            ],
            vertical_spacing=self.config.VERTICAL_SPACING,
            row_heights=self.config.ROW_HEIGHTS
        )

        # Traces using Configured Branding & Integrated Design (v4.5.0 Centralized)
        # Row 1 Center: Overall Yard Progress Gauge (Horizontally Centered)
        fig.add_trace(go.Indicator(
            mode="gauge+number", value=avg_proc,
            number={'suffix': "%", 'font': {'color': self.config.COLOR_ORANGE, 'size': self.config.GAUGE_TEXT_SIZE}},
            gauge={'bar': {'color': self.config.COLOR_ORANGE}, 'bgcolor': "#333", 'axis': {'range': [0, 100], 'visible': False}},
            title={'text': f"{self.config.LABELS['subtitle_overall']}", 'font': {'size': 22, 'color': self.config.COLOR_ORANGE, 'weight': 700}, 'align': 'center'},
            domain={'y': [0.1, 0.9], 'x': [0.35, 0.65]} # Perfectly Centered
        ), row=1, col=1)

        # Header Center (Annotation for D-Day): Grouped with Title
        fig.add_annotation(
            text=f"<b>{self.config.LABELS['subtitle_dday']}</b> | Expected: {proj_date} | <span style='color:white; font-weight:900'>D-{int(days_to_go)}</span>",
            xref="paper", yref="paper",
            x=0.5, y=1.04, # Positioned below title area in the margin
            xanchor="center", yanchor="bottom",
            showarrow=False,
            font=dict(size=18, color="#aaa", family="Noto Sans KR")
        )

        # Refactored to Horizontal Bar Chart with 'Inside-End' numeric labels (v4.3)
        df_bar = self.df_dock.head(14)
        
        fig.add_trace(go.Bar(
            y=df_bar["구역/도크"] + " (" + df_bar["건립선종"] + ")",
            x=df_bar["공정률"],
            orientation='h',
            marker_color=self.config.COLOR_ORANGE,
            text=df_bar["공정률"], 
            textposition='inside',
            insidetextanchor='end',
            textfont=dict(size=16, color='white', family="Noto Sans KR", weight=900), # Unified bold look
            width=0.7 # Bolder bars
        ), row=2, col=1)

        # Tables
        alert_df = self.df_dock[self.df_dock["안전이슈"] != "없음"].head(8)
        fig.add_trace(go.Table(
            header=dict(values=["도크/구역", "작업", "이슈"], fill_color=self.config.COLOR_ORANGE, font=dict(color='white')),
            cells=dict(values=[alert_df["구역/도크"], alert_df["현재작업"], alert_df["안전이슈"]], fill_color=self.config.COLOR_BACKGROUND, font=dict(color='white'))
        ), row=3, col=1)

        fig.add_trace(go.Table(
            header=dict(values=[self.config.LABELS["header_ai_insight"]], fill_color=self.config.COLOR_NAVY, font=dict(color='white')),
            cells=dict(values=[ai_insights], fill_color="#1a1a1a", font=dict(color=self.config.COLOR_ACCENT, size=13), align='left', height=40)
        ), row=3, col=2)

        # Spatial Rhythm & Title Layout (v4.5.0 Perfect Symmetric)
        fig.add_annotation(text=self.config.LABELS["subtitle_bar"], xref="paper", yref="paper", x=0.5, xanchor='center', y=0.88, showarrow=False, font=dict(size=26, color=self.config.COLOR_ORANGE, family="Noto Sans KR", weight=700))
        fig.add_annotation(text=self.config.LABELS["subtitle_safety"], xref="paper", yref="paper", x=0.25, xanchor='center', y=0.35, showarrow=False, font=dict(size=22, color=self.config.COLOR_ORANGE, family="Noto Sans KR", weight=700))
        fig.add_annotation(text=self.config.LABELS["subtitle_ai"], xref="paper", yref="paper", x=0.75, xanchor='center', y=0.35, showarrow=False, font=dict(size=22, color=self.config.COLOR_ORANGE, family="Noto Sans KR", weight=700))

        fig.update_layout(
            paper_bgcolor=self.config.COLOR_BACKGROUND, plot_bgcolor=self.config.COLOR_BACKGROUND, 
            font=dict(color=self.config.COLOR_TEXT, size=18, family="Noto Sans KR"), # Min size 18px baseline
            title_text=f"<b>{self.config.LABELS['title']}</b>",
            title_font=dict(size=self.config.TITLE_FONT_SIZE + 6, color=self.config.COLOR_ORANGE, family="Noto Sans KR"),
            title_x=0.5, title_y=0.98,
            height=self.config.DASHBOARD_HEIGHT + 200, 
            autosize=True,
            template="plotly_dark", showlegend=False,
            margin=dict(t=160, b=80, l=80, r=80) # Symmetric margins (30px range)
        )

        # Branding: Logo Removed per User Request (v4.5.0)
        
        # Golden Ratio Center Alignment (v4.5 Precision)
        fig.update_xaxes(
            range=[0, 150], domain=[0.20, 0.80], row=2, col=1, # Widened for central importance
            tickfont=dict(size=18, color='white', family="Noto Sans KR")
        ) 
        fig.update_yaxes(
            tickfont=dict(size=18, color='white', family="Noto Sans KR"),
            row=2, col=1, autorange="reversed"
        ) 

        output_path = os.path.join(self.config.BASE_DIR, "smart_yard_dashboard.html")
        
        # Selection Fix (CSS Injection v4.5.0 Responsive)
        html_content = fig.to_html(include_plotlyjs='cdn', full_html=True)
        css_enterprise_premium = """
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap" rel="stylesheet">
        <style>
            * { user-select: text !important; -webkit-user-select: text !important; letter-spacing: -0.01em; }
            html, body { 
                margin: 0; padding: 0; overflow-x: hidden; background-color: #121212; 
                font-family: 'Noto Sans KR', sans-serif !important;
                font-size: clamp(18px, 1.2vw, 24px) !important; /* Responsive scaling with 18px min */
            }
            .modebar { display: none !important; }
            .plotly-graph-div { width: 100vw !important; margin: 0 auto; }
            /* Enterprise Grid Rhythm */
            .js-plotly-plot .plotly .main-svg { border-radius: 12px; }
            /* Automatic Scaling for Mobile */
            @media (max-width: 1024px) {
                .main-svg { transform: scale(0.95); transform-origin: top center; }
            }
            @media (max-width: 768px) {
                .main-svg { transform: scale(0.85); transform-origin: top center; }
            }
        </style>
        """
        html_content = html_content.replace("</head>", f"{css_enterprise_premium}</head>")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✨ Professionally Refactored Dashboard: {output_path}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
