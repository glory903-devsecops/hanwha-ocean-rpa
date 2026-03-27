import pandas as pd
import plotly.graph_objects as go
import os
from src.core import config, analytics

class DashboardEngine:
    """
    Visualization Engine for Hanwha Ocean AX (v10.0.0).
    FINAL STABILITY FIX:
    - Explicit list conversion for Bar data to prevent Plotly Type guessing.
    - Simplified Categorical Y-Axis (Combined Safety | Dock).
    - Forced Linear X-Axis.
    - Large Bar Height and Thickness.
    """
    
    def __init__(self):
        self.analytics = analytics.AXAnalytics()
        self.config = config
        
    def load_data(self):
        self.df_dock = pd.read_csv(os.path.join(self.config.DATA_DIR, "dock_status.csv"))
        for prefix in ["[주의]", "[기상]", "[위험]", "[경고]", "[장비]"]:
            self.df_dock["안전이슈"] = self.df_dock["안전이슈"].str.replace(prefix + " ", "", regex=False)
        try:
            self.df_safety = pd.read_excel(os.path.join(self.config.DATA_DIR, "safety_training_master.xlsx"))
        except:
            self.df_safety = None

    def render(self):
        print(f"🎨 [VizEngine] Rendering v11.0.0 (Tailwind Refactor)...")
        self.load_data()
        
        # Calculate Metrics
        avg_proc = self.analytics.calculate_average_progress(self.df_dock)
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        ai_insights = self.analytics.generate_ai_insights(self.df_dock)
        
        # 1. Gauge Chart (Plotly)
        fig_gauge = go.Figure(data=[go.Pie(
            values=[avg_proc, 100 - avg_proc],
            hole=0.8,
            marker_colors=[self.config.BRAND_ORANGE, "#1f2937"],
            textinfo='none', showlegend=False, hoverinfo='none'
        )])
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
            height=300, width=300, margin=dict(t=0, b=0, l=0, r=0)
        )
        gauge_html = fig_gauge.to_html(include_plotlyjs=False, full_html=False, config={'displayModeBar': False})

        # 2. Main Progress Chart (Plotly)
        df_bar = self.df_dock.copy()
        df_bar = df_bar.sort_values("공정률", ascending=True)
        
        fig_bar = go.Figure(go.Bar(
            y=df_bar["구역/도크"],
            x=df_bar["공정률"],
            orientation='h',
            marker_color=self.config.BRAND_ORANGE,
            text=[f"{p}%" for p in df_bar["공정률"]],
            textposition='inside',
            textfont=dict(color='white', weight=700)
        ))
        
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=600,
            margin=dict(l=200, r=50, t=50, b=50),
            xaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=False)
        )
        bar_html = fig_bar.to_html(include_plotlyjs=False, full_html=False, config={'displayModeBar': False})

        # 3. Table Rows Generation
        table_rows_html = ""
        for _, row in self.df_dock.iterrows():
            status_color = "bg-green-500/20 text-green-400" if row['안전이슈'] == '안전' else "bg-red-500/20 text-red-400"
            table_rows_html += f"""
            <tr class="border-b border-gray-800 hover:bg-gray-800/50 transition-colors">
                <td class="py-4 px-6 font-medium">{row['구역/도크']}</td>
                <td class="py-4 px-6">
                    <div class="w-full bg-gray-700 rounded-full h-2">
                        <div class="bg-orange-500 h-2 rounded-full" style="width: {row['공정률']}%"></div>
                    </div>
                    <span class="text-xs text-gray-400 mt-1 block">{row['공정률']}% 완료</span>
                </td>
                <td class="py-4 px-6 text-gray-300">{row['현재작업']}</td>
                <td class="py-4 px-6">
                    <span class="px-3 py-1 rounded-full text-xs font-semibold {status_color}">
                        {row['안전이슈']}
                    </span>
                </td>
                <td class="py-4 px-6 text-sm text-gray-500">{row['마지막업데이트']}</td>
            </tr>
            """

        # 4. AI Insights Generation
        insights_html = "".join([f'<li class="mb-2 flex items-start"><span class="mr-2 text-orange-500">•</span>{ins}</li>' for ins in ai_insights])

        output_path = os.path.join(self.config.BASE_DIR, "smart_yard_dashboard.html")
        
        final_html = f"""
<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한화오션 Smart Yard AX Command Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Pretendard', sans-serif; }}
        .glass {{ background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(10px); }}
    </style>
</head>
<body class="bg-[#0B0F12] text-white selection:bg-orange-500/30">
    <!-- Header -->
    <header class="border-b border-gray-800 glass sticky top-0 z-50">
        <div class="max-w-[1600px] mx-auto px-6 py-4 flex justify-between items-center">
            <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-orange-600 rounded-lg flex items-center justify-center font-bold text-xl">H</div>
                <div>
                    <h1 class="text-xl font-extrabold tracking-tighter">HANWHA OCEAN <span class="text-orange-500">AX COMMAND CENTER</span></h1>
                    <p class="text-xs text-gray-500">Smart Yard Monitoring System v{self.config.VERSION}</p>
                </div>
            </div>
            <div class="flex items-center gap-6">
                <div class="text-right">
                    <p class="text-xs text-gray-500 uppercase font-bold tracking-widest">Expected Completion</p>
                    <p class="text-lg font-bold text-orange-500">{proj_date} <span class="text-sm text-gray-400 font-normal">(D-{int(days_to_go)})</span></p>
                </div>
                <button onclick="downloadCSV()" class="bg-orange-600 hover:bg-orange-700 text-white px-5 py-2.5 rounded-xl font-bold transition-all shadow-lg shadow-orange-600/20 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                    보고서 다운로드 (CSV)
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-[1600px] mx-auto p-8 grid grid-cols-12 gap-8">
        <!-- Top Stats Overlay -->
        <div class="col-span-12 grid grid-cols-4 gap-6 mb-4">
            <div class="bg-gray-900/50 border border-gray-800 p-6 rounded-3xl">
                <p class="text-gray-500 text-sm font-semibold mb-1">전체 공정률</p>
                <p class="text-4xl font-extrabold text-white">{avg_proc:.1f}%</p>
            </div>
            <div class="bg-gray-900/50 border border-gray-800 p-6 rounded-3xl">
                <p class="text-gray-500 text-sm font-semibold mb-1">활성 도크 수</p>
                <p class="text-4xl font-extrabold text-white">{len(self.df_dock)}</p>
            </div>
            <div class="bg-gray-900/50 border border-gray-800 p-6 rounded-3xl">
                <p class="text-gray-500 text-sm font-semibold mb-1">안전 경보</p>
                <p class="text-4xl font-extrabold text-red-500">{len(self.df_dock[self.df_dock['안전이슈'] != '안전'])}건</p>
            </div>
            <div class="bg-gray-900/50 border border-gray-800 p-6 rounded-3xl">
                <p class="text-gray-500 text-sm font-semibold mb-1">생산성 지표</p>
                <p class="text-4xl font-extrabold text-emerald-500">우수</p>
            </div>
        </div>

        <!-- Left: Visualization -->
        <div class="col-span-8 flex flex-col gap-8">
            <div class="bg-gray-900/40 border border-gray-800 rounded-3xl p-8 relative overflow-hidden">
                <div class="absolute top-0 right-0 p-8 opacity-10">
                    <svg class="w-64 h-64 text-orange-500" fill="currentColor" viewBox="0 0 24 24"><path d="M13 10V3L4 14H11V21L20 10H13Z"/></svg>
                </div>
                <h3 class="text-xl font-bold mb-6 flex items-center gap-2">
                    <span class="w-2 h-6 bg-orange-500 rounded-full"></span>
                    도크별 진척 현황
                </h3>
                <div class="w-full flex justify-center">
                    {bar_html}
                </div>
            </div>

            <!-- Detailed Table -->
            <div class="bg-gray-900/40 border border-gray-800 rounded-3xl overflow-hidden">
                <div class="p-8 border-b border-gray-800 flex justify-between items-center">
                    <h3 class="text-xl font-bold flex items-center gap-2">
                        <span class="w-2 h-6 bg-orange-500 rounded-full"></span>
                        상세 작업 현황
                    </h3>
                    <span class="text-xs text-gray-500 bg-gray-800 px-3 py-1 rounded-full uppercase tracking-tighter">Live Database Connection</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left">
                        <thead class="bg-gray-800/30 text-gray-400 text-xs font-bold uppercase tracking-widest">
                            <tr>
                                <th class="py-4 px-6">구역/도크</th>
                                <th class="py-4 px-6">진척도</th>
                                <th class="py-4 px-6">현재 작업</th>
                                <th class="py-4 px-6">안전 상태</th>
                                <th class="py-4 px-6">업데이트 시간</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Right: Insights & Global Status -->
        <div class="col-span-4 flex flex-col gap-8">
            <!-- Overall Gauge -->
            <div class="bg-gray-900 border border-gray-800 rounded-3xl p-8 flex flex-col items-center">
                <h3 class="text-lg font-bold mb-4 text-gray-400 self-start">종합 공정률</h3>
                <div class="relative">
                    {gauge_html}
                    <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                        <span class="text-sm text-gray-500 font-bold uppercase tracking-widest">Total</span>
                        <span class="text-5xl font-black text-white">{avg_proc:.1f}%</span>
                    </div>
                </div>
            </div>

            <!-- AI Insights -->
            <div class="bg-orange-600/10 border border-orange-500/20 rounded-3xl p-8">
                <h3 class="text-xl font-bold mb-6 text-orange-500 flex items-center gap-2">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14H11V21L20 10H13Z"/></svg>
                    AI AX INSIGHTS
                </h3>
                <ul class="text-sm text-gray-300">
                    {insights_html}
                </ul>
                <div class="mt-6 p-4 bg-orange-600/20 rounded-2xl border border-orange-500/30 text-xs text-orange-200 leading-relaxed italic">
                    "AI 분석 결과에 따라 생산 자원을 최적 배치하고 있습니다. 추천 액션을 확인하십시오."
                </div>
            </div>

            <!-- Quick Info -->
            <div class="bg-blue-600/10 border border-blue-500/20 rounded-3xl p-8 text-blue-400">
                <h3 class="text-lg font-bold mb-4 flex items-center gap-2">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    공지사항
                </h3>
                <p class="text-sm mb-4">내일 오전 2도크에서 로봇 팔 자동 배선 작업 시연이 예정되어 있습니다.</p>
                <div class="text-xs text-blue-500/70 border-t border-blue-500/10 pt-4">© 2026 Hanwha Ocean AX Team. All rights reserved.</div>
            </div>
        </div>
    </main>

    <script>
        function downloadCSV() {{
            const rows = [
                ["구역/도크", "공정률", "현재작업", "안전이슈", "마지막업데이트"],
                // Placeholder for CSV data
            ];
            
            let csvContent = "data:text/csv;charset=utf-8,\\uFEFF";
            rows.forEach(function(rowArray) {{
                let row = rowArray.join(",");
                csvContent += row + "\\r\\n";
            }});

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "hanwha_ocean_rpa_report.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}

        window.addEventListener('resize', function() {{
            const plots = document.getElementsByClassName('plotly-graph-div');
            for (let i = 0; i < plots.length; i++) {{
                Plotly.Plots.resize(plots[i]);
            }}
        }});
    </script>
</body>
</html>
        """
        # Cleanup JSON generation for rows
        formatted_rows = ""
        for _, r in self.df_dock.iterrows():
            formatted_rows += f'["{r["구역/도크"]}", "{r["공정률"]}", "{r["현재작업"]}", "{r["안전이슈"]}", "{r["마지막업데이트"]}"],\n'
        # Replace the placeholder in the HTML with the actual formatted rows
        final_html = final_html.replace("// Placeholder for CSV data", formatted_rows.strip().rstrip(','))

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"✨ v11.0.0 Tailwind Premium UI Generated: {output_path}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
