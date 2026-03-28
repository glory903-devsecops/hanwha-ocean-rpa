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
        print(f"🎨 [VizEngine] Rendering v13.0.0 (Premium Stack Refactor)...")
        self.load_data()
        
        # 1. Custom Sorting Logic
        def get_priority(row):
            val = str(row["안전이슈"])
            if any(x in val for x in ["위험", "주의", "경고", "강풍"]): return 0
            if val == "안전": return 2
            return 1
            
        self.df_dock["priority"] = self.df_dock.apply(get_priority, axis=1)
        df_sorted = self.df_dock.sort_values(["priority", "구역/도크"], ascending=[True, True])
        
        # 2. Plotly Horizontal Bar Chart
        y_labels = [f"{row['구역/도크']} <br><span style='font-size:10px; color:#9ca3af'>{row['현재작업']}</span>" for _, row in df_sorted.iterrows()]
        
        colors = []
        for _, row in df_sorted.iterrows():
            p = get_priority(row)
            if p == 0: colors.append("#ef4444") # Red
            elif p == 1: colors.append("#f59e0b") # Amber
            else: colors.append("#f97316") # Orange
            
        fig_bar = go.Figure(go.Bar(
            y=y_labels,
            x=df_sorted["공정률"],
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(255,255,255,0.1)', width=1)
            ),
            text=[f"<b>{p}%</b>" for p in df_sorted["공정률"]],
            textposition='inside',
            textfont=dict(color='white', size=14),
            width=0.7,
            hovertemplate="도크: %{y}<br>공정률: %{x}%<extra></extra>"
        ))
        
        # Add Dividers as Shapes
        shapes = []
        last_p = -1
        for i, (_, row) in enumerate(df_sorted.iterrows()):
            curr_p = get_priority(row)
            if last_p != -1 and last_p != curr_p:
                shapes.append(dict(
                    type="line", x0=0, x1=100, y0=i-0.5, y1=i-0.5,
                    line=dict(color="rgba(249,115,22,0.3)", width=2, dash="dash")
                ))
            last_p = curr_p

        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Pretendard'),
            height=max(600, len(df_sorted) * 90),
            margin=dict(l=280, r=50, t=100, b=50),
            xaxis=dict(
                range=[0, 105], showgrid=True, gridcolor='rgba(255,255,255,0.05)', 
                side='top', ticksuffix="%", tickfont=dict(size=12, color="#9ca3af")
            ),
            yaxis=dict(showgrid=False, autorange="reversed", tickfont=dict(size=13, color="white")),
            shapes=shapes,
            showlegend=False,
            autosize=True,
            bargap=0.15
        )
        bar_html = fig_bar.to_html(include_plotlyjs=False, full_html=False, config={'displayModeBar': False, 'responsive': True})

        # 3. Table and Stats
        avg_proc = df_sorted["공정률"].mean() if not df_sorted.empty else 0
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        
        table_rows_html = ""
        last_priority = -1
        for _, row in df_sorted.iterrows():
            curr_priority = get_priority(row)
            if last_priority != -1 and last_priority != curr_priority:
                table_rows_html += '<tr class="bg-orange-500/5"><td colspan="4" class="py-1 px-8"><div class="h-px bg-orange-500/20 w-full"></div></td></tr>'
            
            status_color = "text-emerald-400" if row['안전이슈'] == '안전' else ("text-red-400 font-bold" if curr_priority == 0 else "text-amber-400")
            status_bg = "bg-emerald-500/10" if row['안전이슈'] == '안전' else ("bg-red-500/10" if curr_priority == 0 else "bg-amber-500/10")
            
            table_rows_html += f"""
            <tr class="border-b border-white/5 hover:bg-white/5 transition-all group">
                <td class="py-6 px-8">
                    <div class="font-bold text-gray-100 group-hover:text-orange-400 transition-colors">{row['구역/도크']}</div>
                    <div class="text-[10px] text-gray-500 font-mono mt-1">{row['마지막업데이트']}</div>
                </td>
                <td class="py-6 px-8">
                    <div class="flex items-center gap-4">
                        <div class="flex-1 bg-gray-800/50 rounded-full h-2.5 overflow-hidden">
                            <div class="bg-gradient-to-r from-orange-600 to-orange-400 h-full rounded-full shadow-[0_0_15px_rgba(249,115,22,0.4)]" style="width: {row['공정률']}%"></div>
                        </div>
                        <span class="text-sm font-black text-white min-w-[3rem] text-right">{row['공정률']}%</span>
                    </div>
                </td>
                <td class="py-6 px-8 text-gray-300 font-medium">{row['현재작업']}</td>
                <td class="py-6 px-8">
                    <span class="px-4 py-1.5 rounded-lg text-xs font-black uppercase tracking-widest {status_bg} {status_color} border border-current/20">
                        {row['안전이슈']}
                    </span>
                </td>
            </tr>
            """
            last_priority = curr_priority

        # CSV Data
        formatted_rows_js = ""
        for _, r in df_sorted.iterrows():
            formatted_rows_js += f'["{r["구역/도크"]}", "{r["공정률"]}", "{r["현재작업"]}", "{r["안전이슈"]}", "{r["마지막업데이트"]}"],\n'
        
        output_path = os.path.join(self.config.BASE_DIR, "smart_yard_dashboard.html")
        
        final_html = f"""
<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hanwha Ocean AX Mission Control</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Pretendard', sans-serif; background-color: #080B0D; }}
        .glass-card {{ 
            background: linear-gradient(145deg, rgba(20, 25, 30, 0.9), rgba(10, 15, 20, 0.95));
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}
        .hero-gradient {{
            background: radial-gradient(circle at 50% -20%, rgba(249, 115, 22, 0.15), transparent 70%);
        }}
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: #080B0D; }}
        ::-webkit-scrollbar-thumb {{ background: #1f2937; border-radius: 10px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #f97316; }}
    </style>
</head>
<body class="text-white selection:bg-orange-500/30 hero-gradient">
    <!-- Super Header -->
    <header class="border-b border-white/5 backdrop-blur-xl sticky top-0 z-50 bg-[#080B0D]/80">
        <div class="max-w-[1500px] mx-auto px-10 py-6 flex justify-between items-end">
            <div class="flex items-center gap-6">
                <div class="w-14 h-14 bg-gradient-to-tr from-orange-600 to-orange-400 rounded-2xl flex items-center justify-center font-black text-3xl shadow-2xl shadow-orange-600/30">H</div>
                <div>
                    <h1 class="text-3xl font-black italic tracking-tighter uppercase whitespace-nowrap">
                        AX <span class="text-orange-500">Mission Control</span>
                    </h1>
                    <div class="flex items-center gap-2 mt-1">
                        <span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
                        <span class="text-[10px] text-gray-500 font-black uppercase tracking-[0.3em] leading-none">Live Intelligent Shipyard System</span>
                    </div>
                </div>
            </div>
            
            <div class="flex items-center gap-12">
                <div class="grid grid-cols-2 gap-10">
                    <div>
                        <p class="text-[9px] text-gray-500 font-black uppercase tracking-widest mb-1.5 opacity-60">Fleet Efficiency</p>
                        <p class="text-3xl font-black font-mono">{avg_proc:.1f}<span class="text-sm text-gray-500 ml-1">%</span></p>
                    </div>
                    <div>
                        <p class="text-[9px] text-gray-500 font-black uppercase tracking-widest mb-1.5 opacity-60">Optimized D-Day</p>
                        <p class="text-3xl font-black text-orange-500 font-mono">{proj_date} <span class="text-xs font-bold text-gray-400 ml-1">D-{int(days_to_go)}</span></p>
                    </div>
                </div>
                <button onclick="downloadCSV()" class="h-14 px-8 bg-white/5 hover:bg-orange-600 hover:text-white border border-white/10 rounded-2xl font-black transition-all flex items-center gap-3 active:scale-95 group">
                    <svg class="w-5 h-5 group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                    EXPORT REPORT
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-[1500px] mx-auto p-12 space-y-16">
        <!-- Visualization Area -->
        <section class="space-y-10">
            <div class="flex items-center justify-between px-2">
                <div class="space-y-1">
                    <h2 class="text-4xl font-black uppercase italic leading-none">Resource Performance</h2>
                    <p class="text-xs text-gray-500 font-medium tracking-wide">Real-time task synchronization across all active docks</p>
                </div>
                <div class="flex gap-3">
                    <div class="px-5 py-2 bg-red-500/5 border border-red-500/20 rounded-xl flex items-center gap-3">
                        <span class="w-1.5 h-1.5 rounded-full bg-red-500 shadow-[0_0_8px_red]"></span>
                        <span class="text-[10px] font-black text-red-500 uppercase tracking-widest">Critical</span>
                    </div>
                    <div class="px-5 py-2 bg-amber-500/5 border border-amber-500/20 rounded-xl flex items-center gap-3">
                        <span class="w-1.5 h-1.5 rounded-full bg-amber-500 shadow-[0_0_8px_amber]"></span>
                        <span class="text-[10px] font-black text-amber-500 uppercase tracking-widest">Caution</span>
                    </div>
                </div>
            </div>

            <!-- Plotly Container -->
            <div class="glass-card rounded-[3rem] p-12 min-h-[600px] relative overflow-hidden">
                <div class="absolute top-0 right-0 w-[50%] h-full bg-orange-600/5 pointer-events-none skew-x-[-20deg] translate-x-32"></div>
                {bar_html}
            </div>
        </section>

        <!-- Monitoring Area -->
        <section class="space-y-10">
            <div class="flex items-center gap-4 px-2">
                <div class="w-1.5 h-8 bg-orange-500 rounded-full"></div>
                <h3 class="text-3xl font-black uppercase italic">Risk Management Ledger</h3>
            </div>

            <div class="glass-card rounded-[3rem] overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left">
                        <thead>
                            <tr class="bg-white/[0.02] text-[10px] text-gray-500 font-black uppercase tracking-[0.25em] border-b border-white/5">
                                <th class="py-7 px-10">Asset / Node ID</th>
                                <th class="py-7 px-10 min-w-[350px]">Efficiency Index</th>
                                <th class="py-7 px-10">Current Operation</th>
                                <th class="py-7 px-10 text-right">Sanctity Check</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-white/[0.03]">
                            {table_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- Global Footer -->
        <footer class="pt-20 pb-10 flex justify-between items-center opacity-30">
            <div class="flex items-center gap-6">
                <span class="text-[10px] font-black uppercase tracking-[0.4em]">Hanwha Ocean AX Core</span>
                <span class="text-[10px] font-black uppercase tracking-[0.4em]">Node-82 Secure</span>
            </div>
            <p class="text-[9px] font-bold uppercase tracking-widest">Proprietary Technology · Hanwha Ocean AX Command Center v13.0</p>
        </footer>
    </main>

    <script>
        function downloadCSV() {{
            const rows = [
                ["구역/도크", "공정률", "현재작업", "안전이슈", "마지막업데이트"],
                {formatted_rows_js.strip().rstrip(',')}
            ];
            let csvContent = "data:text/csv;charset=utf-8,\\uFEFF";
            rows.forEach(function(rowArray) {{
                let row = rowArray.map(v => '"' + v + '"').join(",");
                csvContent += row + "\\r\\n";
            }});
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `hanwha_ax_report_${{new Date().toISOString().split('T')[0]}}.csv`);
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
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"✨ v13.0.0 Premium Stack UI Generated: {output_path}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
