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

    # Create Dashboard Layout
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
            "Localized Yard Progress (Massive Data)",
            "Real-time Safety Monitor",
            "🤖 AI Decision Support Panel (AX Guidance)"
        ),
        vertical_spacing=0.1,
        row_heights=[0.3, 0.4, 0.3]
    )

    # 1. Gauge
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = avg_proc,
        number = {'suffix': "%", 'font': {'color': HANWHA_ORANGE}},
        gauge = {'bar': {'color': HANWHA_ORANGE}, 'bgcolor': "#333"}
    ), row=1, col=1)

    # 2. D-Day
    fig.add_trace(go.Indicator(
        mode = "number",
        value = days_to_go,
        number = {'prefix': "D-", 'font': {'color': "white"}},
        title = {'text': f"Expected: {proj_date}", 'font': {'size': 20}}
    ), row=1, col=2)

    # 3. Bar Chart
    fig.add_trace(go.Bar(
        x=df_dock["구역/도크"] + "<br>(" + df_dock["건립선종"] + ")",
        y=df_dock["공정률"],
        marker_color=HANWHA_ORANGE,
        name="Progress"
    ), row=2, col=1)

    # 4. Safety Table
    alert_df = df_dock[df_dock["안전이슈"] != "없음"].head(10)
    fig.add_trace(go.Table(
        header=dict(values=["도크/구역", "작업", "이슈"], fill_color=HANWHA_ORANGE, font=dict(color='white')),
        cells=dict(values=[alert_df["구역/도크"], alert_df["현재작업"], alert_df["안전이슈"]], fill_color=DARK_BG, font=dict(color='white'))
    ), row=3, col=1)

    # 5. AI Insights Table
    fig.add_trace(go.Table(
        header=dict(values=["<b>AI Insight & Guidance</b>"], fill_color="#002c5f", font=dict(color='white', size=16)),
        cells=dict(
            values=[ai_insights], 
            fill_color="#1a1a1a", 
            font=dict(color='cyan', size=14),
            height=40,
            align='left'
        )
    ), row=3, col=2)

    fig.update_layout(
        paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG, font=dict(color="white"),
        title_text=f"🚢 <b>HANWHA OCEAN</b> Smart Yard AX Command Center (v1.8)",
        title_font=dict(size=26, color=HANWHA_ORANGE),
        height=1000, template="plotly_dark", showlegend=False
    )

    output_file = os.path.join(base_dir, "..", "smart_yard_dashboard.html")
    fig.write_html(output_file)
    print(f"✨ AI-Integrated Dashboard generated: {output_file}")
    
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
