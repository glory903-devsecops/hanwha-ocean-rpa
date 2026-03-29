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
    Visualization Engine for Hanwha Ocean AX (v25.0.0 - Isometric Elite).
    STRATEGIC COMMAND & CONTROL INTERFACE:
    - [SELECTED THEME]: 3D Isometric Digital Twin background.
    - Transparent Command HUD (Overlay).
    - Blueprint Blue & Enterprise Orange Color Palette.
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
        print(f"📡 [Enterprise-AX] Rendering Digital Twin Isometric Dashboard (v25.0.0 - Selected Theme)...")
        self.load_data()
        
        # 1. High-Level KPI Data
        avg_proc = self.analytics.calculate_average_progress(self.df_dock)
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        risk_index = self.analytics.calculate_executive_risk_index(self.df_dock)
        critical_count = len(self.df_dock[self.df_dock["안전이슈"].isin(["위험", "경고", "분진위험", "중량물 주의", "크레인 점검"])])
        
        # 2. Sorting Logic
        def get_severity_score(row):
            val = str(row["안전이슈"])
            if any(x in val for x in ["위험", "경고", "중단", "점검", "주의"]): 
                return 0 if "위험" in val or "경고" in val else 1
            return 2
            
        self.df_dock["sev_score"] = self.df_dock.apply(get_severity_score, axis=1)
        df_sorted = self.df_dock.sort_values(["sev_score", "공정률"], ascending=[True, True])

        # 3. Generate Cards HTML (Compact HUD Style)
        guidelines_path = os.path.join(self.config.DATA_DIR, "safety_guidelines.csv")
        guidelines_json = "[]"
        if os.path.exists(guidelines_path):
            g_df = pd.read_csv(guidelines_path)
            guidelines_json = g_df.to_json(orient="records")

        cards_html = ""
        for _, row in df_sorted.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_task = html.escape(str(row['현재작업']))
            e_safety = html.escape(str(row['안전이슈']))
            
            sev = get_severity_score(row)
            p = {
                0: {"accent": "#EF4444", "bg": "bg-red-500/10", "border": "border-red-500/20", "label": "CRITICAL"},
                1: {"accent": "#F59E0B", "bg": "bg-amber-500/10", "border": "border-amber-500/20", "label": "CAUTION"},
                2: {"accent": "#10B981", "bg": "bg-emerald-500/5", "border": "border-emerald-500/10", "label": "OPTIMAL"}
            }.get(sev)
            
            cards_html += f"""
            <div class="glass-hud p-6 rounded-[2rem] border border-white/5 group hover:bg-white/10 transition-all card-node" 
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
                    <div class="text-[10px] font-black uppercase text-gray-500 tracking-widest">TASK: {e_task}</div>
                    <div class="text-xs font-black text-white italic" @mouseenter="showGuidance('{e_safety}', $event)" @mouseleave="hideGuidance()">{e_safety}</div>
                </div>
            </div>
            """

        # 4. Final Assembly
        output_path = os.path.join(self.config.BASE_DIR, "smart_yard_dashboard.html")
        css_vars = theme.get_css_vars()
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한화오션 AX - 디지털 트윈 전략 커맨드 (v25.0.0)</title>
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
        .overlay {{ background: rgba(2, 6, 23, 0.75); backdrop-filter: blur(10px); min-height: 100vh; }}
        .glass-hud {{ background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(40px); border: 1px solid rgba(255, 255, 255, 0.05); }}
        .kpi-card {{ border-top: 4px solid #00F2FF; }}
        [x-cloak] {{ display: none !important; }}
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(0, 242, 255, 0.2); border-radius: 10px; }}
    </style>
</head>
<body x-data="axDashboard()">
    
    <div class="overlay p-10 lg:p-20">
        <!-- HEADER HUD -->
        <header class="max-w-[1800px] mx-auto flex flex-col xl:flex-row justify-between items-start gap-12 mb-20">
            <div>
                <div class="flex items-center gap-8 mb-4">
                    <div class="w-20 h-20 bg-gradient-to-tr from-orange-600 to-orange-400 rounded-3xl flex items-center justify-center text-4xl font-black italic shadow-2xl">H</div>
                    <h1 class="text-6xl lg:text-8xl font-black tracking-tighter uppercase italic leading-none">
                        STRATEGIC <span class="text-[#FF6B00]">AX ENGINE</span>
                    </h1>
                </div>
                <div class="flex items-center gap-6">
                    <span class="w-12 h-[2px] bg-[#FF6B00]"></span>
                    <p class="text-lg font-black text-[#00F2FF] uppercase tracking-[1em]">v25.0.0 디지털 트윈 가동 중</p>
                </div>
            </div>

            <div class="flex gap-10">
                <div class="glass-hud p-8 rounded-[2.5rem] kpi-card min-w-[280px]">
                    <p class="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-4">전략 리스크 인덱스 (QRI)</p>
                    <p class="text-6xl font-black text-white tracking-widest tabular-nums italic">{risk_index}</p>
                </div>
                <div class="glass-hud p-8 rounded-[2.5rem] kpi-card min-w-[280px]" style="border-top-color: #FF6B00;">
                    <p class="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-4">전사 통합 공정률</p>
                    <p class="text-6xl font-black text-[#FF6B00] tracking-widest tabular-nums italic">{avg_proc:.1f}%</p>
                </div>
            </div>
        </header>

        <!-- COMMAND SUB-GRID -->
        <div class="max-w-[1800px] mx-auto grid grid-cols-1 xl:grid-cols-4 gap-12">
            <!-- SIDEBAR: INSIGHTS & FILTERS -->
            <div class="xl:col-span-1 space-y-12">
                <div class="glass-hud p-10 rounded-[3rem] space-y-8">
                    <h3 class="text-2xl font-black uppercase italic tracking-widest">TACTICAL FILTERS</h3>
                    <div class="space-y-4">
                        <button @click="filter = 'all'" :class="filter === 'all' ? 'bg-white text-black' : 'hover:bg-white/5'" class="w-full text-left p-6 rounded-2xl text-xl font-black italic transition-all">ALL NODES</button>
                        <button @click="filter = 'critical'" :class="filter === 'critical' ? 'bg-red-500 text-white' : 'hover:bg-red-500/10 text-red-500'" class="w-full text-left p-6 rounded-2xl text-xl font-black italic transition-all">CRITICAL RISK</button>
                        <button @click="filter = 'warning'" :class="filter === 'warning' ? 'bg-amber-500 text-white' : 'hover:bg-amber-500/10 text-amber-500'" class="w-full text-left p-6 rounded-2xl text-xl font-black italic transition-all">CAUTION AREA</button>
                    </div>
                    <div class="relative pt-6 border-t border-white/5">
                        <input type="text" x-model="search" placeholder="영역 검색..." class="w-full bg-white/5 border border-white/10 rounded-2xl py-6 px-8 text-xl font-black italic focus:outline-none focus:border-[#00F2FF]">
                    </div>
                </div>

                <div class="glass-hud p-10 rounded-[3rem] border border-[#00F2FF]/20">
                    <p class="text-xs font-black text-[#00F2FF] uppercase tracking-widest mb-6">AI 전략 권고 사항</p>
                    <div class="space-y-6">
                        <div class="p-5 bg-white/5 rounded-2xl border-l-4 border-[#FF6B00]">
                            <p class="text-base font-bold text-gray-300">D-Day 예측 업데이트 완료</p>
                            <p class="text-2xl font-black text-white mt-2">D-{days_to_go:.0f} (예상: {proj_date})</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- MAIN HUD GRID -->
            <div class="xl:col-span-3 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-8 overflow-y-auto max-h-[1000px] pr-4">
                {cards_html}
            </div>
        </div>

        <footer class="mt-20 text-center opacity-20 py-10 border-t border-white/5">
            <p class="text-[10px] font-black uppercase tracking-[2em]">Hanwha Ocean AX Advanced Digital Twin System V25.0.0 Global Edition</p>
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
        print(f"✨ Digital Twin Isometric Strategic Dashboard (v25.0.0) Generated: {{output_path}}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
