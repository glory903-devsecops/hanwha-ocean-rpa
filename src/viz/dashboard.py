import pandas as pd
import os
import sys
import html
import datetime

# 프로젝트 루트를 path에 추가하여 src 모듈을 불러올 수 있게 함
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core import config, analytics
from src.viz import theme

class DashboardEngine:
    """
    Visualization Engine for Hanwha Ocean AX (v25.3.0 - Strategic Vector Graphic).
    STRATEGIC COMMAND & CONTROL INTERFACE:
    - [GRAPHIC HUD]: Pure SVG-based interactive shipyard map (100% Code-based Graphic).
    - [INTERACTIVE NODES]: Glowing safety nodes on a vectorized blueprint.
    - [TIERED RESPONSE]: Pinned critical response panels.
    """
    
    def __init__(self):
        self.analytics = analytics.AXAnalytics()
        self.config = config
        self.theme = theme.THEME
        self.df_dock = None
        
    def load_data(self):
        csv_path = os.path.join(self.config.DATA_DIR, "dock_status.csv")
        self.df_dock = pd.read_csv(csv_path)
        # Clean safety prefixes
        for prefix in ["[주의]", "[기상]", "[위험]", "[경고]", "[장비]"]:
            self.df_dock["안전이슈"] = self.df_dock["안전이슈"].str.replace(prefix + " ", "", regex=False)

    def generate_svg_map(self, df):
        """Generates a high-end SVG shipyard blueprint with interactive status nodes."""
        svg_nodes = ""
        # 60개 노드 조밀 배치 (XY 좌표 가상으로 분산)
        for i, row in df.iterrows():
            # 가상 좌표 (Shipyard-like grid)
            x = 200 + (i % 10) * 80
            y = 150 + (i // 10) * 100
            
            sev = str(row["안전이슈"])
            color = "#EF4444" if "위험" in sev or "경고" in sev else ("#F59E0B" if "주의" in sev else "#00F2FF")
            opacity = "0.8" if "위험" in sev else "0.3"
            stroke_width = "4" if "위험" in sev else "1"
            pulse_class = "animate-ping" if "위험" in sev else ""
            
            svg_nodes += f"""
            <g class="cursor-pointer group" @mouseenter="showGuidance('{html.escape(sev)}', $event)" @mouseleave="hideGuidance()">
                <circle cx="{x}" cy="{y}" r="12" fill="{color}" fill-opacity="{opacity}" stroke="{color}" stroke-width="{stroke_width}" class="{pulse_class}" />
                <circle cx="{x}" cy="{y}" r="6" fill="{color}" />
                <text x="{x}" y="{y-20}" text-anchor="middle" font-size="10" fill="white" font-weight="900" class="opacity-0 group-hover:opacity-100 transition-opacity uppercase tracking-widest">{html.escape(str(row['구역/도크']))}</text>
            </g>
            """
            
        return f"""
        <svg viewBox="0 0 1200 800" class="w-full h-full drop-shadow-[0_0_30px_rgba(0,163,255,0.1)]">
            <!-- BLUEPRINT GRID -->
            <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="0.5"/>
                </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
            
            <!-- SHIPYARD OUTLINE (ABSTRACT GRAPHIC) -->
            <path d="M 100 100 L 1100 100 L 1100 700 L 100 700 Z" fill="none" stroke="rgba(0, 242, 255, 0.1)" stroke-width="2" stroke-dasharray="10,10" />
            <path d="M 300 200 Q 600 50 900 200 L 900 600 Q 600 750 300 600 Z" fill="rgba(30, 41, 59, 0.2)" stroke="rgba(0, 242, 255, 0.2)" stroke-width="1" />
            
            <!-- DOCK CONNECTORS -->
            <line x1="100" y1="400" x2="1100" y2="400" stroke="rgba(255,255,255,0.05)" stroke-width="1" stroke-dasharray="5,5" />
            
            <!-- INTERACTIVE NODES -->
            {svg_nodes}
        </svg>
        """

    def render(self):
        print(f"📡 [Enterprise-AX] Rendering Interactive Vector Graphic Dashboard (v25.3.0 Strategic Blueprint)...")
        self.load_data()
        
        # 1. High-Level KPI Data
        avg_proc = self.analytics.calculate_average_progress(self.df_dock)
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        risk_index = self.analytics.calculate_executive_risk_index(self.df_dock)
        
        # 2. Logic for Tiering
        def get_severity_score(row):
            val = str(row["안전이슈"])
            if any(x in val for x in ["위험", "경고", "중단", "점검", "주의"]): 
                return 0 if "위험" in val or "경고" in val else 1
            return 2
            
        self.df_dock["sev_score"] = self.df_dock.apply(get_severity_score, axis=1)
        df_critical = self.df_dock[self.df_dock["sev_score"] == 0]
        df_standard = self.df_dock[self.df_dock["sev_score"] != 0].sort_values(["sev_score", "공정률"], ascending=[True, True])

        # 3. Generate SVG Map Component
        svg_map_html = self.generate_svg_map(self.df_dock)

        # 4. Critical List (Floating HUD)
        critical_list_html = ""
        for _, row in df_critical.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_safety = html.escape(str(row['안전이슈']))
            critical_list_html += f"""
            <div class="glass-hud p-6 rounded-3xl border-l-[12px] border-red-500 animate-pulse-slow mb-4 flex justify-between items-center bg-red-500/5">
                <div>
                    <h5 class="text-xl font-black text-white italic tracking-tighter uppercase">{e_dock}</h5>
                    <p class="text-[10px] font-black text-red-500 uppercase tracking-widest">{e_safety}</p>
                </div>
                <div class="text-3xl font-black text-white">{row['공정률']}%</div>
            </div>
            """

        # 5. Global Track List
        global_list_html = ""
        for _, row in df_standard.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            global_list_html += f"""
            <div class="flex items-center justify-between p-3 border-b border-white/5 hover:bg-white/5 transition-all text-left card-node cursor-default"
                 data-severity="{'caution' if row['sev_score']==1 else 'optimal'}" data-task="{html.escape(str(row['현재작업']))}" data-name="{e_dock.lower()}">
                <div class="text-[10px] font-black text-gray-400 uppercase tracking-tighter truncate max-w-[120px]">{e_dock}</div>
                <div class="flex items-center gap-3">
                    <span class="text-lg font-black text-white italic">{row['공정률']}%</span>
                    <div class="w-12 h-1 bg-white/10 rounded-full overflow-hidden">
                        <div class="h-full bg-cyan-500" style="width: {row['공정률']}%"></div>
                    </div>
                </div>
            </div>
            """

        # 6. Final HTML Assembly
        output_path = os.path.join(self.config.BASE_DIR, "smart_yard_dashboard.html")
        guidelines_path = os.path.join(self.config.DATA_DIR, "safety_guidelines.csv")
        guidelines_json = "[]"
        if os.path.exists(guidelines_path):
            g_df = pd.read_csv(guidelines_path)
            guidelines_json = g_df.to_json(orient="records")
            
        css_vars = theme.get_css_vars()
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한화오션 AX - 인터랙티브 블루프린트 (v25.3.0)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            {css_vars} 
        }}
        body {{ 
            background: #020617; 
            color: #fff; 
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }}
        .hud-layer {{ position: relative; z-index: 20; height: 100vh; display: flex; flex-direction: column; }}
        .glass-hud {{ background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(40px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        @keyframes pulse-slow {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.8; transform: scale(1.005); }} }}
        .animate-pulse-slow {{ animation: pulse-slow 3s infinite ease-in-out; }}
        .custom-scroll::-webkit-scrollbar {{ width: 4px; }}
        .custom-scroll::-webkit-scrollbar-thumb {{ background: rgba(0, 242, 255, 0.3); border-radius: 10px; }}
        [x-cloak] {{ display: none !important; }}
    </style>
</head>
<body x-data="axDashboard()">
    
    <div class="hud-layer p-10">
        <!-- TOP STRATEGIC HUD -->
        <header class="flex justify-between items-center mb-10 w-full">
            <div class="flex items-center gap-8">
                <div class="w-16 h-16 bg-gradient-to-tr from-orange-600 to-orange-400 rounded-2xl flex items-center justify-center text-3xl font-black italic">H</div>
                <div class="flex flex-col">
                    <h1 class="text-4xl lg:text-5xl font-black tracking-tighter uppercase italic leading-none">
                        VECTOR <span class="text-[#00F2FF]">BLUEPRINT</span>
                    </h1>
                    <p class="text-[8px] font-black text-[#FF6B00] uppercase tracking-[1em] mt-2">v25.3.0 그래픽 관제 가동 중</p>
                </div>
            </div>

            <div class="flex gap-4">
                <div class="glass-hud p-6 rounded-3xl min-w-[200px] border-l-4 border-[#00F2FF]">
                    <p class="text-[7px] font-bold text-gray-500 uppercase tracking-widest mb-1">RISK INDEX</p>
                    <p class="text-4xl font-black text-white italic tabular-nums">{risk_index}</p>
                </div>
                <div class="glass-hud p-6 rounded-3xl min-w-[200px] border-l-4 border-[#FF6B00]">
                    <p class="text-[7px] font-bold text-gray-500 uppercase tracking-widest mb-1">YARD PROGRESS</p>
                    <p class="text-4xl font-black text-[#FF6B00] italic tabular-nums">{avg_proc:.1f}%</p>
                </div>
            </div>
        </header>

        <!-- MAIN VIEWPORT (SVG MAP HERO) -->
        <div class="flex-1 flex gap-8 overflow-hidden relative">
            
            <!-- LEFT: CRITICAL FLOATING HUD -->
            <div class="w-[380px] flex flex-col z-50">
                <h2 class="text-xl font-black italic uppercase tracking-tighter text-white mb-6">Critical Nodes</h2>
                <div class="flex-1 overflow-y-auto custom-scroll pr-4 space-y-4">
                    {critical_list_html or '<div class="opacity-20 text-xs text-center border-2 border-dashed border-white/5 py-10 rounded-3xl">Stabilized</div>'}
                </div>
                <div class="glass-hud p-8 rounded-[3rem] mt-10">
                    <p class="text-[8px] font-black text-emerald-500 uppercase tracking-widest mb-2">Completion Prediction</p>
                    <p class="text-4xl font-black text-white italic">D-{days_to_go:.0f}</p>
                </div>
            </div>

            <!-- CENTER GRAPHIC: THE SVG SHIPYARD BLUEPRINT -->
            <div class="flex-1 glass-hud rounded-[4rem] relative overflow-hidden flex items-center justify-center p-10 border border-white/5">
                <div class="absolute top-8 right-12 z-50">
                    <span class="text-[8px] font-black text-[#00F2FF] uppercase tracking-[1em]">Shipyard Virtual Layout Active</span>
                </div>
                <!-- THE SVG STARTS HERE -->
                {svg_map_html}
            </div>

            <!-- RIGHT: COMPACT GLOBAL TRACKER -->
            <div class="w-[320px] flex flex-col z-50 pt-[10vh]">
                <div class="glass-hud flex-1 flex flex-col rounded-[3rem] overflow-hidden shadow-2xl">
                    <div class="p-6 border-b border-white/5 bg-white/5">
                        <h3 class="text-xs font-black uppercase italic tracking-widest text-[#00F2FF]">Global Asset Tracker</h3>
                    </div>
                    <div class="p-3">
                        <input type="text" x-model="search" placeholder="Filter..." class="w-full bg-white/5 border border-white/10 rounded-xl py-2 px-4 text-xs font-black focus:outline-none focus:border-[#00F2FF]">
                    </div>
                    <div class="flex-1 overflow-y-auto custom-scroll">
                        {global_list_html}
                    </div>
                </div>
            </div>
        </div>

        <footer class="mt-8 flex justify-between items-center opacity-30 py-6 border-t border-white/5 w-full">
            <p class="text-[8px] font-black uppercase tracking-[1em]">Hanwha Ocean AX Vector Engine V25.3.0</p>
        </footer>
    </div>

    <!-- AI SISE OVERLAY -->
    <div x-show="guidance.show" x-cloak class="fixed pointer-events-none z-[3000] glass-hud p-8 max-w-xs border-[#FF6B00]/40 rounded-[2rem]" :style="`left: ${{guidance.x}}px; top: ${{guidance.y}}px;`" x-transition>
        <p class="text-sm font-bold text-white leading-relaxed" x-text="guidance.text"></p>
    </div>

    <script>
        function axDashboard() {{
            return {{
                filter: 'all', search: '', guidelines: {guidelines_json}, guidance: {{ show: false, text: '', x: 0, y: 0 }},
                applyFilters() {{
                    const cards = document.querySelectorAll('.card-node');
                    cards.forEach(card => {{
                        const name = card.dataset.name;
                        const task = card.dataset.task;
                        const matchesSearch = name.includes(this.search.toLowerCase()) || task.includes(this.search.toLowerCase());
                        card.style.display = matchesSearch ? 'flex' : 'none';
                    }});
                }},
                showGuidance(issue, event) {{
                    const match = this.guidelines.find(g => issue.includes(g.ISSUE));
                    this.guidance.text = match ? match.GUIDANCE : 'Monitoring State.';
                    this.guidance.x = event.clientX + 20;
                    this.guidance.y = event.clientY + 20;
                    this.guidance.show = true;
                }},
                hideGuidance() {{ this.guidance.show = false; }},
                init() {{
                    this.$watch('search', () => this.applyFilters());
                }}
            }}
        }}
    </script>
</body>
</html>
            """)
        print(f"✨ Strategic Vector Blueprint Dashboard (v25.3.0) Generated: {{output_path}}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
