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
    Visualization Engine for Hanwha Ocean AX (v25.2.0 - Focus Strategic Elite).
    STRATEGIC COMMAND & CONTROL INTERFACE:
    - [SELECTED THEME]: 3D Isometric Digital Twin background.
    - [TIERED RESPONSE]: Critical Priority (Immediate) vs. Standard Operations.
    - [COMPACT TRACKING]: High-density grid for non-critical nodes.
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
        print(f"📡 [Enterprise-AX] Rendering Tiered Strategic Dashboard (v25.2.0 Focus Elite)...")
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

        # 3. Component Generation: Priority Cards (Top Tier)
        priority_cards_html = ""
        for _, row in df_critical.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_task = html.escape(str(row['현재작업']))
            e_safety = html.escape(str(row['안전이슈']))
            
            priority_cards_html += f"""
            <div class="glass-hud p-10 rounded-[3.5rem] border-l-[24px] border-red-500 hover:scale-[1.02] transition-all animate-pulse-slow">
                <div class="flex justify-between items-start mb-6">
                    <div>
                        <span class="text-xs font-black tracking-widest text-red-500 uppercase px-4 py-1 bg-red-500/10 rounded-full border border-red-500/20">IMMEDIATE ACTION</span>
                        <h4 class="text-5xl font-black text-white italic tracking-tighter mt-4 uppercase">{e_dock}</h4>
                    </div>
                    <div class="text-5xl font-black text-red-500 italic mt-4">{row['공정률']}%</div>
                </div>
                <div class="w-full bg-white/5 h-2 rounded-full overflow-hidden mb-8">
                    <div class="h-full bg-red-500 rounded-full shadow-[0_0_20px_#EF4444]" style="width: {row['공정률']}%"></div>
                </div>
                <div class="flex flex-col gap-4">
                    <div class="text-lg font-black text-gray-500 uppercase tracking-widest leading-none">작업: {e_task}</div>
                    <div class="text-3xl font-black text-white bg-red-500/20 p-4 rounded-2xl border border-red-500/30 text-center"
                         @mouseenter="showGuidance('{e_safety}', $event)" @mouseleave="hideGuidance()">🆘 {e_safety}</div>
                </div>
            </div>
            """

        # 4. Component Generation: Standard Node Cards (Bottom Tier)
        standard_cards_html = ""
        for _, row in df_standard.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_task = html.escape(str(row['현재작업']))
            e_safety = html.escape(str(row['안전이슈']))
            
            sev = row['sev_score']
            p = {
                1: {"accent": "#F59E0B", "bg": "bg-amber-500/10", "border": "border-amber-500/20", "label": "CAUTION"},
                2: {"accent": "#10B981", "bg": "bg-emerald-500/5", "border": "border-emerald-500/10", "label": "OPTIMAL"}
            }.get(sev, {"accent": "#64748b", "bg": "bg-gray-500/5", "border": "border-gray-500/10", "label": "NORMAL"})
            
            standard_cards_html += f"""
            <div class="glass-hud p-6 rounded-[2.5rem] border border-white/5 group hover:bg-white/10 transition-all card-node" 
                 data-severity="{p['label'].lower()}" data-task="{e_task.lower()}" data-name="{e_dock.lower()}">
                <div class="flex justify-between items-start mb-4">
                    <span class="text-xs font-black tracking-widest text-[#00F2FF]/60 uppercase">{e_dock}</span>
                    <span class="text-[10px] font-bold px-3 py-0.5 rounded-full border border-current/20" style="color: {p['accent']}">{p['label']}</span>
                </div>
                <div class="text-4xl font-black text-white italic tracking-tighter mb-4">{row['공정률']}%</div>
                <div class="w-full bg-white/5 h-1.5 rounded-full overflow-hidden mb-6">
                    <div class="h-full bg-[#FF6B00] rounded-full shadow-[0_0_10px_#FF6B00]" style="width: {row['공정률']}%"></div>
                </div>
                <div class="flex justify-between items-end">
                    <div class="text-[10px] font-black uppercase text-gray-500 tracking-widest">{e_task}</div>
                    <div class="text-xs font-black text-white italic" @mouseenter="showGuidance('{e_safety}', $event)" @mouseleave="hideGuidance()">{e_safety}</div>
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
    <title>한화오션 AX - 전략 커맨드 (v25.2.0)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            {css_vars} 
        }}
        body {{ 
            background: #020617 url('docs/images/final_dashboard_sample.png') no-repeat center center fixed;
            background-size: cover;
            color: #fff; 
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
        }}
        .overlay {{ background: rgba(2, 6, 23, 0.85); backdrop-filter: blur(8px); min-height: 100vh; }}
        .glass-hud {{ background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(40px); border: 1px solid rgba(255, 255, 255, 0.05); }}
        .kpi-card {{ border-top: 4px solid #00F2FF; }}
        @keyframes pulse-slow {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.85; transform: scale(1.01); }} }}
        .animate-pulse-slow {{ animation: pulse-slow 3s infinite ease-in-out; }}
        [x-cloak] {{ display: none !important; }}
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(0, 242, 255, 0.2); border-radius: 10px; }}
    </style>
</head>
<body x-data="axDashboard()">
    
    <div class="overlay p-8 lg:p-16">
        <!-- HEADER HUD -->
        <header class="max-w-[1900px] mx-auto flex flex-col xl:flex-row justify-between items-start gap-12 mb-20">
            <div>
                <div class="flex items-center gap-8 mb-4">
                    <div class="w-20 h-20 bg-gradient-to-tr from-orange-600 to-orange-400 rounded-3xl flex items-center justify-center text-4xl font-black italic shadow-2xl">H</div>
                    <h1 class="text-6xl lg:text-7xl font-black tracking-tighter uppercase italic leading-none">
                        CRITICAL <span class="text-[#FF6B00]">COMMAND CENTER</span>
                    </h1>
                </div>
                <div class="flex items-center gap-6">
                    <span class="w-12 h-[2px] bg-[#FF6B00]"></span>
                    <p class="text-[10px] font-black text-[#00F2FF] uppercase tracking-[1.5em]">v25.2.0 전략적 데이터 레이어 가동 중</p>
                </div>
            </div>

            <div class="flex gap-8">
                <div class="glass-hud p-6 rounded-3xl kpi-card min-w-[240px]">
                    <p class="text-[8px] font-black text-gray-500 uppercase tracking-widest mb-3">전략 리스크 인덱스</p>
                    <p class="text-5xl font-black text-white italic">{risk_index}</p>
                </div>
                <div class="glass-hud p-6 rounded-3xl kpi-card min-w-[240px]" style="border-top-color: #FF6B00;">
                    <p class="text-[8px] font-black text-gray-500 uppercase tracking-widest mb-3">전사 통합 공정률</p>
                    <p class="text-5xl font-black text-[#FF6B00] italic">{avg_proc:.1f}%</p>
                </div>
            </div>
        </header>

        <!-- TIER 1: CRITICAL PRIORITY (DIRECT CHECK) -->
        <section class="max-w-[1900px] mx-auto mb-20 animate-fade-in-up">
            <div class="flex items-end gap-6 mb-10">
                <h2 class="text-4xl font-black italic uppercase tracking-tighter text-white">Critical Priority</h2>
                <span class="text-xs font-black text-red-500 uppercase tracking-widest border border-red-500/20 px-4 py-1 rounded-full bg-red-500/5 mb-2">Immediate Response Required</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10">
                {priority_cards_html or '<div class="col-span-full py-20 text-center opacity-30 text-2xl italic font-black uppercase tracking-widest border-2 border-dashed border-white/5 rounded-[4rem]">Critical Risk Nodes: 0 (전 야드 정상 수렴 중)</div>'}
            </div>
        </section>

        <!-- TIER 2: GLOBAL YARD LIST (COMPACT TRACKING) -->
        <div class="max-w-[1900px] mx-auto grid grid-cols-1 xl:grid-cols-5 gap-12 border-t border-white/5 pt-20">
            <!-- SIDEBAR CONTROL -->
            <div class="xl:col-span-1 space-y-12">
                <div class="glass-hud p-10 rounded-[3.5rem] space-y-8">
                    <h3 class="text-xl font-black uppercase italic tracking-widest border-b border-white/5 pb-4">Standard Filters</h3>
                    <div class="space-y-4">
                        <button @click="filter = 'all'" :class="filter === 'all' ? 'bg-white text-black' : 'hover:bg-white/5'" class="w-full text-left p-5 rounded-2xl text-lg font-black italic transition-all">ALL NODES</button>
                        <button @click="filter = 'caution'" :class="filter === 'caution' ? 'bg-amber-500 text-white' : 'hover:bg-amber-500/10 text-amber-500'" class="w-full text-left p-5 rounded-2xl text-lg font-black italic transition-all">CAUTION AREA</button>
                        <button @click="filter = 'optimal'" :class="filter === 'optimal' ? 'bg-emerald-500 text-white' : 'hover:bg-emerald-500/10 text-emerald-500'" class="w-full text-left p-5 rounded-2xl text-lg font-black italic transition-all">OPTIMAL ZONE</button>
                    </div>
                </div>
                
                <div class="glass-hud p-10 rounded-[3.5rem]">
                    <p class="text-[10px] font-black text-[#00F2FF] uppercase tracking-widest mb-6">Tactical Search</p>
                    <input type="text" x-model="search" placeholder="영역/호선 검색..." class="w-full bg-white/5 border border-white/10 rounded-2xl py-5 px-8 text-xl font-black italic focus:outline-none focus:border-[#00F2FF]">
                </div>
            </div>

            <!-- MAIN COMPACT GRID -->
            <div class="xl:col-span-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-6 overflow-y-auto max-h-[800px] pr-4">
                {standard_cards_html}
            </div>
        </div>

        <footer class="mt-20 text-center opacity-20 py-10">
            <p class="text-[10px] font-black uppercase tracking-[2em]">Hanwha Ocean AX Focused Strategic Engine V25.2.0</p>
        </footer>
    </div>

    <!-- AI SISE OVERLAY -->
    <div x-show="guidance.show" x-cloak class="fixed pointer-events-none z-[3000] glass-hud p-10 max-w-sm border-[#FF6B00]/40 rounded-[2.5rem]" :style="`left: ${{guidance.x}}px; top: ${{guidance.y}}px;`" x-transition>
        <h5 class="text-xs font-black text-[#FF6B00] uppercase tracking-widest mb-3">RPA 가이드라인</h5>
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
                        if (matchesFilter && matchesSearch) {{ card.classList.remove('hidden'); }} else {{ card.classList.add('hidden'); }}
                    }});
                }},
                showGuidance(issue, event) {{
                    const match = this.guidelines.find(g => issue.includes(g.ISSUE));
                    this.guidance.text = match ? match.GUIDANCE : '자동 프로토콜 미지정';
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
        print(f"✨ Focused Tiered Dashboard (v25.2.0) Generated: {{output_path}}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
