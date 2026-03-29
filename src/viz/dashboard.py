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
    Visualization Engine for Hanwha Ocean AX (v25.0.0 - Enterprise Elite).
    STRATEGIC COMMAND & CONTROL INTERFACE:
    - Real-time Digital Twin Synchronization Monitoring.
    - Large-scale high-visibility asset hierarchy (50+ nodes).
    - AI-Driven Strategic Action Planning.
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
        for prefix in ["[주의]", "[기상]", "[위험]", "[경고]", "[장비]", "[주의]"]:
            self.df_dock["안전이슈"] = self.df_dock["안전이슈"].str.replace(prefix + " ", "", regex=False)

    def render(self):
        print(f"📡 [Enterprise-AX] Rendering Scale-UP Filterable Dashboard (v25.0.0 Enterprise Quantum Elite)...")
        self.load_data()
        
        # 1. High-Level KPI Data (Strategic)
        avg_proc = self.analytics.calculate_average_progress(self.df_dock)
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        risk_index = self.analytics.calculate_executive_risk_index(self.df_dock)
        critical_count = len(self.df_dock[self.df_dock["안전이슈"].isin(["위험", "경고", "분진위험", "중량물 주의", "크레인 점검"])])
        
        # 2. Sorting Logic (Severity > Process)
        def get_severity_score(row):
            val = str(row["안전이슈"])
            if any(x in val for x in ["위험", "경고", "중단", "점검", "주의"]): 
                return 0 if "위험" in val or "경고" in val else 1
            return 2 # 정상/안전
            
        self.df_dock["sev_score"] = self.df_dock.apply(get_severity_score, axis=1)
        df_sorted = self.df_dock.sort_values(["sev_score", "공정률"], ascending=[True, True])

        # Load Guidelines for Injection
        guidelines_path = os.path.join(self.config.DATA_DIR, "safety_guidelines.csv")
        guidelines_json = "[]"
        if os.path.exists(guidelines_path):
            g_df = pd.read_csv(guidelines_path)
            guidelines_json = g_df.to_json(orient="records")

        # 3. Component Generation: Individual Priority Cards
        cards_html = ""
        for _, row in df_sorted.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_task = html.escape(str(row['현재작업']))
            e_safety = html.escape(str(row['안전이슈']))
            e_time = html.escape(str(row['마지막업데이트']))
            
            sev = get_severity_score(row)
            palette = {
                0: {"accent": "#EF4444", "bg": "bg-red-500/10", "border": "border-red-500/20", "label": "위험", "sev_key": "critical"},
                1: {"accent": "#F59E0B", "bg": "bg-amber-500/10", "border": "border-amber-500/20", "label": "주의", "sev_key": "warning"},
                2: {"accent": "#10B981", "bg": "bg-emerald-500/5", "border": "border-emerald-500/10", "label": "정상", "sev_key": "optimal"}
            }
            p = palette.get(sev, palette[2])
            
            cards_html += f"""
            <div class="glass rounded-[2.5rem] p-12 border-l-[18px] group transition-all hover:translate-x-3 {p['border']} animate-fade-in-up card-node" 
                 data-severity="{p['sev_key']}" data-task="{e_task.lower()}" data-name="{e_dock.lower()}"
                 style="border-left-color: {p['accent']}; margin-bottom: var(--h-gap-main);">
                <div class="flex flex-col xl:flex-row justify-between xl:items-center gap-12">
                    <div class="flex-1 space-y-6 text-left">
                        <div class="flex items-center gap-6">
                            <h4 class="text-5xl font-black uppercase italic tracking-tighter text-white group-hover:text-orange-500 transition-colors leading-tight">{e_dock}</h4>
                            <span class="px-6 py-2 rounded-full text-xl font-black border border-current/20 {p['bg']}" style="color: {p['accent']}">{p['label']}</span>
                        </div>
                        <p class="text-3xl font-bold text-gray-400 uppercase tracking-widest leading-none">
                            {e_task} <span class="mx-4 opacity-20">|</span> <span class="font-mono text-xl opacity-60">업데이트: {e_time}</span>
                        </p>
                    </div>

                    <div class="flex-[1.5] flex items-center gap-12">
                        <div class="flex-1 bg-white/[0.05] rounded-full h-6 overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-orange-600 to-orange-400 rounded-full transition-all duration-1000 shadow-[0_0_20px_rgba(249,115,22,0.6)]" 
                                 style="width: {row['공정률']}%"></div>
                        </div>
                        <div class="text-7xl font-black font-mono text-white min-w-[8rem] text-right">{row['공정률']}%</div>
                    </div>

                    <div class="xl:min-w-[320px] text-right relative">
                        <div class="text-base font-black text-gray-600 uppercase mb-4 tracking-[0.3em]">실시간 보안/안전 상태</div>
                        <div class="text-5xl font-black uppercase italic tracking-widest cursor-help hover:text-white transition-colors" 
                             @mouseenter="showGuidance('{e_safety}', $event)" 
                             @mouseleave="hideGuidance()"
                             style="color: {p['accent']}">{e_safety}</div>
                    </div>
                </div>
            </div>
            """

        # 4. Final HTML Assembly
        output_path = os.path.join(self.config.BASE_DIR, "smart_yard_dashboard.html")
        css_vars = theme.get_css_vars()
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한화오션 AX - 전략 커맨드 센터 (v25.0.0)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            {css_vars} 
            --h-gap-main: 30px;
        }}
        body {{ 
            background-color: var(--h-bg); 
            color: #fff; 
            font-family: 'Noto Sans KR', var(--h-font-main);
            background-image: radial-gradient(circle at 10% 0%, rgba(249, 115, 22, 0.1), transparent 50%),
                              radial-gradient(circle at 90% 100%, rgba(0, 242, 255, 0.05), transparent 50%);
            background-attachment: fixed;
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
        }}
        .glass {{ background: var(--h-surface); backdrop-filter: var(--h-glass-blur); border: 1px solid var(--h-border); }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(40px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .animate-fade-in-up {{ animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
        
        [x-cloak] {{ display: none !important; }}

        /* Scrollbar Styling */
        ::-webkit-scrollbar {{ width: 10px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255,107,0,0.2); border-radius: 10px; border: 3px solid var(--h-bg); }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(255,107,0,0.5); }}
    </style>
</head>
<body class="p-8 lg:p-24" x-data="axDashboard()">
    
    <!-- HQ STRATEGIC HEADER -->
    <div class="max-w-[1700px] mx-auto flex flex-col xl:flex-row justify-between items-end gap-20 mb-32 border-b border-white/5 pb-20">
        <div class="flex items-center gap-16">
            <div class="w-32 h-32 bg-gradient-to-tr from-orange-600 to-orange-400 rounded-[3rem] flex items-center justify-center text-6xl font-black italic shadow-[0_0_80px_rgba(249,115,22,0.5)] border-4 border-white/20 select-none">H</div>
            <div class="text-left">
                <h1 class="text-7xl lg:text-9xl font-black tracking-tighter uppercase italic leading-none whitespace-nowrap">
                    AX <span class="text-orange-500">CONTROL</span>
                </h1>
                <p class="text-sm lg:text-base text-gray-500 font-bold uppercase tracking-[0.8em] mt-8 flex items-center gap-4">
                    <span class="w-12 h-[2px] bg-orange-500"></span> 
                    v25.0.0 Strategic Quantum Elite
                </p>
            </div>
        </div>
        
        <div class="flex flex-wrap gap-12 lg:gap-24">
            <div class="group py-4 px-8 rounded-[2rem] hover:bg-white/5 transition-all text-right">
                <p class="text-xs text-gray-700 font-bold uppercase tracking-[0.3em] mb-4 group-hover:text-cyan-400">전략 리스크 지수</p>
                <p class="text-6xl font-black text-white leading-none tracking-tighter tabular-nums text-right">{risk_index}</p>
            </div>
            <div class="group border-l border-white/10 pl-16 py-4 px-8 rounded-[2rem] hover:bg-white/5 transition-all text-right">
                <p class="text-xs text-gray-700 font-bold uppercase tracking-[0.3em] mb-4 group-hover:text-red-500 transition-colors">통합 위기 경보</p>
                <p class="text-6xl font-black text-red-500 leading-none tabular-nums text-right">{critical_count}</p>
            </div>
            <div class="group border-l border-white/10 pl-16 py-4 px-8 rounded-[2rem] hover:bg-white/5 transition-all text-right">
                <p class="text-xs text-gray-700 font-bold uppercase tracking-[0.3em] mb-4 group-hover:text-orange-500 transition-colors">전사 공정률</p>
                <div class="flex justify-end font-black text-orange-500 leading-none">
                    <span class="text-6xl tabular-nums">{avg_proc:.1f}</span>
                    <span class="text-3xl ml-2 font-black">%</span>
                </div>
            </div>
        </div>
    </div>

    <!-- STRATEGIC EXECUTIVE SUMMARY ROW -->
    <div class="max-w-[1700px] mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 mb-20 animate-fade-in-up">
        <div class="glass rounded-[3.5rem] p-12 border-t-8 border-cyan-500/30 flex justify-between items-center group overflow-hidden relative">
            <div class="w-40 h-40 bg-cyan-500/10 rounded-full absolute -right-10 -bottom-10 blur-3xl group-hover:scale-150 transition-transform duration-1000"></div>
            <div class="z-10 text-left">
                <p class="text-xs font-black text-gray-600 uppercase tracking-widest mb-4 font-bold">Digital Twin Sync</p>
                <p class="text-6xl font-black text-white italic tracking-tighter">99.98<span class="text-xl text-cyan-500 ml-1 font-black">%</span></p>
                <div class="flex items-center gap-3 mt-6">
                    <div class="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></div>
                    <span class="text-xs font-bold text-emerald-500 uppercase tracking-widest font-black">Active Real-time</span>
                </div>
            </div>
            <div class="text-7xl opacity-10 group-hover:opacity-30 transition-opacity">📡</div>
        </div>

        <div class="glass rounded-[3.5rem] p-12 border-t-8 border-orange-500/30 flex justify-between items-center group overflow-hidden relative">
             <div class="w-40 h-40 bg-orange-500/10 rounded-full absolute -right-10 -top-10 blur-3xl group-hover:scale-150 transition-transform duration-1000"></div>
            <div class="z-10 text-left">
                <p class="text-xs font-black text-gray-600 uppercase tracking-widest mb-4 font-bold">RPA BOT Fleet</p>
                <p class="text-6xl font-black text-white italic tracking-tighter">12<span class="text-2xl text-orange-500 ml-1">/</span>12</p>
                <div class="flex items-center gap-3 mt-6">
                    <span class="px-4 py-1.5 rounded-full bg-orange-500/10 text-orange-500 text-[10px] font-black uppercase tracking-widest border border-orange-500/20">All Healthy</span>
                </div>
            </div>
            <div class="text-7xl opacity-10 group-hover:opacity-30 transition-opacity">🤖</div>
        </div>

        <div class="glass rounded-[3.5rem] p-12 border-t-8 border-emerald-500/30 flex justify-between items-center group overflow-hidden relative">
            <div class="w-40 h-40 bg-emerald-500/10 rounded-full absolute -right-10 -bottom-10 blur-3xl group-hover:scale-150 transition-transform duration-1000"></div>
            <div class="z-10 text-left">
                <p class="text-xs font-black text-gray-600 uppercase tracking-widest mb-4 font-bold">Estimated Delivery (D-Day)</p>
                <p class="text-6xl font-black text-white italic tracking-tighter">D-{days_to_go:.0f}</p>
                <p class="text-xl text-gray-500 font-bold uppercase tracking-widest mt-4">Exp: {proj_date}</p>
            </div>
            <div class="text-7xl opacity-10 group-hover:opacity-30 transition-opacity">⚓</div>
        </div>
    </div>

    <!-- TACTICAL FILTER BAR -->
    <div class="max-w-[1700px] mx-auto mb-20 flex flex-col md:flex-row gap-8 items-center justify-between animate-fade-in-up" style="animation-delay: 0.1s;">
        <div class="flex bg-white/5 p-3 rounded-[2.5rem] border border-white/10">
            <button @click="filter = 'all'" :class="filter === 'all' ? 'bg-white text-black shadow-2xl' : 'text-gray-500 hover:text-white'" class="px-12 py-5 rounded-[2rem] text-xl font-black italic tracking-tighter uppercase transition-all duration-300">ALL</button>
            <button @click="filter = 'critical'" :class="filter === 'critical' ? 'bg-red-500 text-white shadow-2xl scale-105' : 'text-gray-500 hover:text-red-500'" class="px-12 py-5 rounded-[2rem] text-xl font-black italic tracking-tighter uppercase transition-all duration-300">위험</button>
            <button @click="filter = 'warning'" :class="filter === 'warning' ? 'bg-amber-500 text-white shadow-2xl scale-105' : 'text-gray-500 hover:text-amber-500'" class="px-12 py-5 rounded-[2rem] text-xl font-black italic tracking-tighter uppercase transition-all duration-300">주의</button>
            <button @click="filter = 'optimal'" :class="filter === 'optimal' ? 'bg-emerald-500 text-white shadow-2xl scale-105' : 'text-gray-500 hover:text-emerald-500'" class="px-12 py-5 rounded-[2rem] text-xl font-black italic tracking-tighter uppercase transition-all duration-300">정상</button>
        </div>
        <div class="flex-1 max-w-xl group relative">
            <div class="absolute inset-y-0 left-8 flex items-center text-gray-600 pointer-events-none group-focus-within:text-orange-500 transition-colors">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
            <input type="text" x-model="search" placeholder="구역 또는 도크 검색 (e.g. 제1도크)" class="w-full bg-white/5 border border-white/10 rounded-[2.5rem] py-6 pl-20 pr-10 text-2xl font-black italic tracking-tight focus:outline-none focus:border-orange-500 transition-all focus:bg-white/10 group-hover:border-white/20">
        </div>
    </div>

    <!-- MAIN ASSET GRID -->
    <div class="max-w-[1700px] mx-auto space-y-12 pb-40">
        {cards_html}
    </div>

    <!-- FOOTER -->
    <footer class="max-w-[1700px] mx-auto py-20 border-t border-white/5 opacity-20 text-center">
        <p class="text-[10px] font-black tracking-[1.5em] uppercase">Proprietary AX Engine | Hanwha Ocean AX Team V25.0.0</p>
    </footer>

    <!-- SISE GUIDANCE OVERLAY -->
    <div x-show="guidance.show" 
         x-cloak 
         class="fixed pointer-events-none z-[2000] glass rounded-[2.5rem] p-10 max-w-sm shadow-[0_0_80px_rgba(0,0,0,0.8)] border-orange-500/40"
         :style="`left: ${{guidance.x}}px; top: ${{guidance.y}}px;`"
         x-transition:enter="transition ease-out duration-300"
         x-transition:enter-start="opacity-0 scale-90"
         x-transition:enter-end="opacity-100 scale-100">
        <div class="flex items-center gap-4 mb-4">
            <span class="text-3xl">🤖</span>
            <div class="h-[2px] flex-1 bg-gradient-to-r from-orange-500 to-transparent"></div>
        </div>
        <h5 class="text-lg font-black text-orange-500 uppercase tracking-widest mb-3">AI SISE 대처 방안</h5>
        <p class="text-xl font-bold text-white leading-relaxed" x-text="guidance.text"></p>
    </div>

    <script>
        function axDashboard() {{
            return {{
                filter: 'all',
                search: '',
                guidelines: {guidelines_json},
                guidance: {{ show: false, text: '', x: 0, y: 0 }},
                
                init() {{
                    this.$watch('filter', () => this.applyFilters());
                    this.$watch('search', () => this.applyFilters());
                }},

                applyFilters() {{
                    const cards = document.querySelectorAll('.card-node');
                    cards.forEach(card => {{
                        const sev = card.dataset.severity;
                        const name = card.dataset.name;
                        const task = card.dataset.task;
                        
                        const matchesFilter = this.filter === 'all' || sev === this.filter;
                        const matchesSearch = name.includes(this.search.toLowerCase()) || task.includes(this.search.toLowerCase());
                        
                        if (matchesFilter && matchesSearch) {{
                            card.classList.remove('hidden');
                        }} else {{
                            card.classList.add('hidden');
                        }}
                    }});
                }},

                showGuidance(issue, event) {{
                    const match = this.guidelines.find(g => issue.includes(g.ISSUE));
                    this.guidance.text = match ? match.GUIDANCE : '본 항목에 대한 자동화 프로토콜이 정의되지 않았습니다. 관리 센터에 문의하십시오.';
                    this.guidance.x = event.clientX + 20;
                    this.guidance.y = event.clientY + 20;
                    this.guidance.show = true;
                }},

                hideGuidance() {{
                    this.guidance.show = false;
                }}
            }}
        }}
    </script>
</body>
</html>
            """)
        print(f"✨ Strategic Enterprise Dashboard (v25.0.0) Generated: {{output_path}}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
