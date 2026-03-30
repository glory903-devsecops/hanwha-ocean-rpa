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
    Visualization Engine for Hanwha Ocean AX (v25.2.1 - True Digital Twin).
    STRATEGIC COMMAND & CONTROL INTERFACE:
    - [MAIN FOCUS]: 3D Isometric Yard Image is the central hero.
    - [RESPONSE LAYER]: Critical Focus cards on the left.
    - [TRACKING LAYER]: Side-panel list on the right-bottom.
    - [UI]: Clean HUD overlay with minimal background dimming.
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

    def render(self):
        print(f"📡 [Enterprise-AX] Rendering True Digital Twin Dashboard (v25.2.1 Focus Hero)...")
        self.load_data()
        
        # 1. High-Level KPI Data
        avg_proc = self.analytics.calculate_average_progress(self.df_dock)
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        risk_index = self.analytics.calculate_executive_risk_index(self.df_dock)
        
        # 2. Sorting & Tiering Logic
        def get_severity_score(row):
            val = str(row["안전이슈"])
            if any(x in val for x in ["위험", "경고", "중단", "점검", "주의"]): 
                return 0 if "위험" in val or "경고" in val else 1
            return 2
            
        self.df_dock["sev_score"] = self.df_dock.apply(get_severity_score, axis=1)
        
        # [Tiering]
        df_critical = self.df_dock[self.df_dock["sev_score"] == 0].sort_values("공정률")
        df_standard = self.df_dock[self.df_dock["sev_score"] != 0].sort_values(["sev_score", "공정률"], ascending=[True, True])

        # 3. Component Generation: Priority HUD (Floating Left)
        priority_cards_html = ""
        for _, row in df_critical.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_task = html.escape(str(row['현재작업']))
            e_safety = html.escape(str(row['안전이슈']))
            
            priority_cards_html += f"""
            <div class="glass-hud p-6 rounded-[2rem] border-l-8 border-red-500 animate-pulse-slow mb-6 backdrop-blur-3xl">
                <div class="flex justify-between items-center mb-3">
                    <span class="text-[10px] font-black text-red-500 uppercase tracking-widest border border-red-500/20 px-3 py-0.5 rounded-full">URGENT</span>
                    <span class="text-2xl font-black text-white italic">{row['공정률']}%</span>
                </div>
                <h4 class="text-2xl font-black text-white uppercase tracking-tighter mb-2">{e_dock}</h4>
                <div class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-4">{e_task}</div>
                <div class="p-3 bg-red-500/20 rounded-xl border border-red-500/30 text-xs font-black text-white text-center cursor-help"
                     @mouseenter="showGuidance('{e_safety}', $event)" @mouseleave="hideGuidance()">🆘 {e_safety}</div>
            </div>
            """

        # 4. Component Generation: Compact Tracking List (Right Panel)
        standard_list_html = ""
        for _, row in df_standard.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_task = html.escape(str(row['현재작업']))
            e_safety = html.escape(str(row['안전이슈']))
            
            sev = row['sev_score']
            accent = {1: "#F59E0B", 2: "#10B981"}.get(sev, "#64748b")
            
            standard_list_html += f"""
            <div class="flex items-center justify-between p-4 border-b border-white/5 hover:bg-white/5 transition-all text-left card-node cursor-default"
                 data-severity="{'caution' if sev==1 else 'optimal'}" data-task="{e_task.lower()}" data-name="{e_dock.lower()}">
                <div class="flex-1">
                    <div class="text-[10px] font-black text-white uppercase tracking-tighter">{e_dock}</div>
                    <div class="text-[8px] text-gray-500 uppercase tracking-widest">{e_task}</div>
                </div>
                <div class="text-right min-w-[80px]">
                    <div class="text-xl font-black text-white italic">{row['공정률']}<span class="text-[10px] ml-1">%</span></div>
                    <div class="h-1 w-full bg-white/5 mt-1 rounded-full overflow-hidden">
                        <div class="h-full bg-[#FF6B00]" style="width: {row['공정률']}%"></div>
                    </div>
                </div>
            </div>
            """

        # 5. Final HTML Assembly
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
    <title>한화오션 AX - 리얼 디지털 트윈 (v25.2.1)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            {css_vars} 
        }}
        body {{ 
            background: #000 url('docs/images/final_dashboard_sample.png') no-repeat center center fixed;
            background-size: cover;
            color: #fff; 
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            min-height: 100vh;
            margin: 0;
            overflow: hidden;
        }}
        .dimmer {{ background: rgba(2, 6, 23, 0.4); min-height: 100vh; width: 100vw; position: fixed; top: 0; left: 0; pointer-events: none; z-index: 10; }}
        .hud-layer {{ position: relative; z-index: 20; height: 100vh; width: 100vw; box-sizing: border-box; display: flex; flex-direction: column; overflow: hidden; }}
        .glass-hud {{ background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(50px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        @keyframes pulse-slow {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.8; transform: scale(1.005); }} }}
        .animate-pulse-slow {{ animation: pulse-slow 3s infinite ease-in-out; }}
        [x-cloak] {{ display: none !important; }}
        ::-webkit-scrollbar {{ width: 4px; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(0, 242, 255, 0.3); border-radius: 10px; }}
    </style>
</head>
<body x-data="axDashboard()">
    
    <div class="dimmer"></div>

    <div class="hud-layer p-10">
        <!-- TOP HEADER HUD (Minimal) -->
        <header class="flex justify-between items-start mb-10 w-full">
            <div class="space-y-4">
                <div class="flex items-center gap-6">
                    <div class="w-16 h-16 bg-gradient-to-tr from-orange-600 to-orange-400 rounded-2xl flex items-center justify-center text-3xl font-black italic shadow-2xl">H</div>
                    <h1 class="text-5xl lg:text-6xl font-black tracking-tighter uppercase italic leading-none">
                        STRATEGIC <span class="text-[#FF6B00]">AX ENGINE</span>
                    </h1>
                </div>
                <div class="flex items-center gap-4">
                    <span class="w-10 h-[1px] bg-[#FF6B00]"></span>
                    <p class="text-[8px] font-black text-[#00F2FF] uppercase tracking-[1em]">v25.2.1 리얼 디지털 트윈 활성</p>
                </div>
            </div>

            <div class="flex gap-4">
                <div class="glass-hud p-4 rounded-2xl min-w-[180px] border-t-2 border-[#00F2FF]">
                    <p class="text-[7px] font-black text-gray-500 uppercase tracking-widest mb-1">RISK INDEX</p>
                    <p class="text-3xl font-black text-white italic tabular-nums">{risk_index}</p>
                </div>
                <div class="glass-hud p-4 rounded-2xl min-w-[180px] border-t-2 border-[#FF6B00]">
                    <p class="text-[7px] font-black text-gray-500 uppercase tracking-widest mb-1">AVG PROGRESS</p>
                    <p class="text-3xl font-black text-[#FF6B00] italic tabular-nums">{avg_proc:.1f}%</p>
                </div>
            </div>
        </header>

        <!-- MAIN VIEWPORT (Flexible Center) -->
        <div class="flex-1 flex gap-10 overflow-hidden">
            <!-- LEFT: CRITICAL RESPONSE HUD -->
            <div class="w-[400px] flex flex-col pointer-events-auto">
                <div class="flex items-end gap-4 mb-6">
                    <h2 class="text-2xl font-black italic uppercase tracking-tighter text-white">Critical Priority</h2>
                    <div class="w-2 h-2 bg-red-500 rounded-full animate-pulse mb-1"></div>
                </div>
                <div class="flex-1 overflow-y-auto pr-4 space-y-4">
                    {priority_cards_html or '<div class="glass-hud p-10 text-center opacity-30 text-xs italic font-black uppercase tracking-widest rounded-[2rem]">Stable State (0 Hazards)</div>'}
                </div>
                <!-- D-DAY HUD -->
                <div class="glass-hud p-6 rounded-3xl mt-10 border-l-4 border-emerald-500/50">
                    <p class="text-[8px] font-black text-gray-500 uppercase tracking-widest mb-2">Estimated Arrival</p>
                    <div class="text-3xl font-black text-white italic">D-{days_to_go:.0f} <span class="text-xs text-emerald-500 ml-2">({proj_date})</span></div>
                </div>
            </div>

            <!-- CENTER: HERO SPACE (IMAGE IS FULLY VISIBLE HERE) -->
            <div class="flex-1 relative flex items-center justify-center pointer-events-none">
                <!-- Empty space to reveal background image -->
                <div class="absolute bottom-10 left-1/2 -translate-x-1/2 glass-hud px-12 py-4 rounded-full border border-[#00F2FF]/20 animate-fade-in-up">
                    <p class="text-[10px] font-black text-[#00F2FF] uppercase tracking-[1em]">Shipyard Digital Twin Interface Active</p>
                </div>
            </div>

            <!-- RIGHT-BOTTOM: COMPACT GLOBAL TRACKING PANEL -->
            <div class="w-[400px] flex flex-col pointer-events-auto pt-[20vh]">
                <div class="glass-hud flex-1 flex flex-col rounded-[3.5rem] overflow-hidden shadow-2xl border border-white/5">
                    <div class="p-8 border-b border-white/5 flex justify-between items-center bg-white/5">
                        <h3 class="text-sm font-black uppercase italic tracking-widest text-[#00F2FF]">Global Tracking</h3>
                        <div class="flex gap-2">
                             <button @click="filter = 'all'" class="text-[8px] font-black px-2 py-1 rounded bg-white/10 hover:bg-white/20">ALL</button>
                             <button @click="filter = 'caution'" class="text-[8px] font-black px-2 py-1 rounded bg-amber-500/20 text-amber-500">CAUTION</button>
                        </div>
                    </div>
                    <!-- SEARCH -->
                    <div class="p-4 bg-black/20">
                        <input type="text" x-model="search" placeholder="Search Node..." class="w-full bg-white/5 border border-white/10 rounded-xl py-3 px-6 text-sm font-black italic focus:outline-none focus:border-[#00F2FF]">
                    </div>
                    <!-- LIST LAYER -->
                    <div class="flex-1 overflow-y-auto custom-scroll">
                        {standard_list_html}
                    </div>
                </div>
            </div>
        </div>

        <footer class="mt-10 flex justify-between items-center opacity-40 py-6 border-t border-white/5 w-full">
            <p class="text-[8px] font-black uppercase tracking-[1em]">Hanwha Ocean AX Master Engine V25.2.1 Global Edition</p>
            <div class="flex gap-4">
                <span class="text-[8px] font-bold text-emerald-500">SYSTEM: OPTIMAL</span>
                <span class="text-[8px] font-bold text-[#00F2FF]">SYNC: 99.98%</span>
            </div>
        </footer>
    </div>

    <!-- AI SISE OVERLAY -->
    <div x-show="guidance.show" x-cloak class="fixed pointer-events-none z-[3000] glass-hud p-10 max-w-sm border-[#FF6B00]/40 rounded-[2.5rem]" :style="`left: ${{guidance.x}}px; top: ${{guidance.y}}px;`" x-transition>
        <h5 class="text-[10px] font-black text-[#FF6B00] uppercase tracking-widest mb-3">SISE BOT PROTOCOL</h5>
        <p class="text-lg font-bold text-white leading-relaxed" x-text="guidance.text"></p>
    </div>

    <script>
        function axDashboard() {{
            return {{
                filter: 'all',
                search: '',
                guidelines: {guidelines_json},
                guidance: {{ show: false, text: '', x: 0, y: 0 }},
                applyFilters() {{
                    const cards = document.querySelectorAll('.card-node');
                    cards.forEach(card => {{
                        const sev = card.dataset.severity;
                        const name = card.dataset.name;
                        const task = card.dataset.task;
                        const matchesFilter = this.filter === 'all' || sev === this.filter;
                        const matchesSearch = name.includes(this.search.toLowerCase()) || task.includes(this.search.toLowerCase());
                        if (matchesFilter && matchesSearch) {{ card.classList.remove('flex'); card.classList.add('flex'); card.style.display = 'flex'; }} 
                        else {{ card.style.display = 'none'; }}
                    }});
                }},
                showGuidance(issue, event) {{
                    const match = this.guidelines.find(g => issue.includes(g.ISSUE));
                    this.guidance.text = match ? match.GUIDANCE : 'Default Protocol: Monitoring...';
                    this.guidance.x = event.clientX + 20;
                    this.guidance.y = event.clientY + 20;
                    this.guidance.show = true;
                }},
                hideGuidance() {{ this.guidance.show = false; }},
                init() {{
                    this.$watch('filter', () => this.applyFilters());
                    this.$watch('search', () => this.applyFilters());
                }}
            }}
        }}
    </script>
</body>
</html>
            """)
        print(f"✨ True Digital Twin Hero Dashboard (v25.2.1) Generated: {{output_path}}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
