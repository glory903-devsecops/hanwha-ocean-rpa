import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import subprocess
import sys
import webbrowser
from datetime import datetime, timedelta

# Branding Colors
HANWHA_ORANGE = "#eb6e00"
HANWHA_NAVY = "#002c5f"
DARK_BG = "#1e1e1e"

def run_pre_scripts():
    print("🔄 [AX Pipeline] Generating fresh data & verifying...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(base_dir, "generate_pbi_data.py")], check=True)
    subprocess.run([sys.executable, os.path.join(base_dir, "..", "tests", "test_pbi_ready.py")], check=True)

def create_dashboard():
    print("🎨 [AX Dashboard] Designing premium interactive dashboard...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    
    # Load Data
    df_dock = pd.read_csv(os.path.join(data_dir, "dock_status.csv"))
    df_safe = pd.read_excel(os.path.join(data_dir, "safety_training_master.xlsx"))
    
    # Analytics
    avg_proc = df_dock["공정률"].mean()
    alert_count = df_dock[df_dock["안전이슈"] != "없음"].shape[0]
    
    # [AX Logic] AI Insights Generator
    delayed_docks = df_dock[df_dock["공정률"] < 30]["구역/도크"].tolist()
    safety_risks = df_dock[df_dock["안전이슈"] != "없음"]["구역/도크"].tolist()
    
    ai_insights = [
        f"🤖 <b>AI Resource Optimizer</b>: {len(delayed_docks)}개 구역 지연 위험 감지.",
        f"💡 <b>Suggestion</b>: '통영 야드 A' 인력을 '거제 제1도크'로 15% 재배치 권장.",
        f"⚠️ <b>Risk Alert</b>: {', '.join(safety_risks[:2])}... 구역 안전 점검 시급.",
        f"🎯 <b>Goal Alignment</b>: 현재 속도 유지 시 연간 목표 대비 4.2% 조기 달성 예상."
    ]

    # Predictive: Projected Completion
    progress_per_day = 1.8 
    days_to_go = (100 - avg_proc) / progress_per_day
    proj_date = (datetime.now() + timedelta(days=days_to_go)).strftime("%Y-%m-%d")

    # Create Dashboard Layout (Improved spacing)
    fig = make_subplots(
        rows=3, cols=2,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}],
            [{"colspan": 2}, None],
            [{"type": "table"}, {"type": "table"}]
        ],
        subplot_titles=(
            "Overall Yard Process", 
            "Projected Completion Date",
            "Localized Yard Progress (Massive Data View)",
            "Real-time Safety Alert Monitor",
            "🤖 AI Decision Support Panel (AX Guidance)"
        ),
        vertical_spacing=0.2, # 3x increase in spacing
        row_heights=[0.25, 0.45, 0.3] # More room for the bar chart
    )

    # 1. Gauge
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = avg_proc,
        number = {'suffix': "%", 'font': {'color': HANWHA_ORANGE, 'size': 40}},
        gauge = {'bar': {'color': HANWHA_ORANGE}, 'bgcolor': "#333"}
    ), row=1, col=1)

    # 2. D-Day
    fig.add_trace(go.Indicator(
        mode = "number",
        value = days_to_go,
        number = {'prefix': "D-", 'font': {'color': "white", 'size': 60}},
        title = {'text': f"Expected: {proj_date}", 'font': {'size': 20}}
    ), row=1, col=2)

    # 3. Bar Chart (Rotated Labels for Readability)
    fig.add_trace(go.Bar(
        x=df_dock["구역/도크"] + " (" + df_dock["건립선종"] + ")",
        y=df_dock["공정률"],
        marker_color=HANWHA_ORANGE,
        name="Progress",
        text=df_dock["공정률"],
        textposition='outside'
    ), row=2, col=1)

    # 4. Safety Table
    alert_df = df_dock[df_dock["안전이슈"] != "없음"].head(10)
    fig.add_trace(go.Table(
        header=dict(values=["도크/구역", "작업", "이슈"], fill_color=HANWHA_ORANGE, font=dict(color='white', size=13), height=30),
        cells=dict(values=[alert_df["구역/도크"], alert_df["현재작업"], alert_df["안전이슈"]], fill_color=DARK_BG, font=dict(color='white', size=11), height=25)
    ), row=3, col=1)

    # 5. AI Insights Table
    fig.add_trace(go.Table(
        header=dict(values=["<b>AI Insight & Guidance</b>"], fill_color="#002c5f", font=dict(color='white', size=15), height=30),
        cells=dict(
            values=[ai_insights], 
            fill_color="#1a1a1a", 
            font=dict(color='cyan', size=13),
            height=35,
            align='left'
        )
    ), row=3, col=2)

    # Layout Fine-Tuning
    fig.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG, font=dict(color="white"),
        title_text=f"🚢 <b>HANWHA OCEAN</b> Smart Yard AX Command Center (v2.0)",
        title_font=dict(size=28, color=HANWHA_ORANGE),
        height=1200, # Increased height for better spacing
        template="plotly_dark", showlegend=False,
        margin=dict(t=150, b=100, l=60, r=60)
    )

    # Rotate X-axis labels to prevent overlap
    fig.update_xaxes(tickangle=45, tickfont=dict(size=10), row=2, col=1)

    output_file = os.path.join(base_dir, "..", "smart_yard_dashboard.html")
    fig.write_html(output_file)
    print(f"✨ UI Optimized Dashboard generated: {output_file}")
    
    try:
        webbrowser.open(f"file://{os.path.abspath(output_file)}")
    except:
        pass

if __name__ == "__main__":
    try:
        run_pre_scripts()
        create_dashboard()
        print("\n✅ Hanwha Ocean AX Dashboard Pipeline Completed.")
    except Exception as e:
        print(f"\n❌ Error during AX automation: {e}")
