import pandas as pd
import os
import sys
import html
import json

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core import config, analytics
from src.viz import theme

class DashboardEngine:
    """
    Visualization Engine for Hanwha Ocean AX (v26.0.0 - Executive List Edition).
    STRATEGIC COMMAND & CONTROL INTERFACE:
    - [DASHBOARD UI]: Reverted to Executive List with horizontal progress bars.
    - [STATUS VIZ]: Circular status indicators for risk levels.
    - [INTERACTION]: Center Popup for detailed instructions.
    - [LOCALIZATION]: Full Korean Support.
    """
    
    def __init__(self):
        self.analytics = analytics.AXAnalytics()
        self.config = config
        self.theme = theme.THEME
        self.df_dock = None
        
    def load_data(self):
        csv_path = os.path.join(self.config.DATA_DIR, "dock_status.csv")
        self.df_dock = pd.read_csv(csv_path)
        for prefix in ["[주의]", "[기상]", "[위험]", "[경고]", "[장비]"]:
            self.df_dock["안전이슈"] = self.df_dock["안전이슈"].str.replace(prefix + " ", "", regex=False)

    def render(self):
        print(f"📡 [Enterprise-AX] Rendering Executive List Dashboard (v26.0.0 Final)...")
        self.load_data()
        
        avg_proc = self.analytics.calculate_average_progress(self.df_dock)
        risk_index = self.analytics.calculate_executive_risk_index(self.df_dock)
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        
        # Sorting
        def get_severity_score(row):
            val = str(row["안전이슈"])
            if any(x in val for x in ["위험", "경고", "중단"]): return 0
            if any(x in val for x in ["주의", "점검"]): return 1
            return 2
            
        self.df_dock["sev_score"] = self.df_dock.apply(get_severity_score, axis=1)
        df_sorted = self.df_dock.sort_values(["sev_score", "공정률"], ascending=[True, True])

        # Guidelines for Popup
        guidelines_path = os.path.join(self.config.DATA_DIR, "safety_guidelines.csv")
        guidelines_json = "[]"
        if os.path.exists(guidelines_path):
            g_df = pd.read_csv(guidelines_path)
            guidelines_json = g_df.to_json(orient="records")

        # HTML Generation: List Items
        list_html = ""
        for _, row in df_sorted.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_task = html.escape(str(row['현재작업']))
            e_safety = html.escape(str(row['안전이슈']))
            
            sev = row['sev_score']
            color = {0: "#EF4444", 1: "#F59E0B", 2: "#10B981"}.get(sev)
            label = {0: "위험", 1: "주의", 2: "정상"}.get(sev)
            
            list_html += f"""
            <div class="glass flex items-center gap-12 p-10 rounded-[2.5rem] border-l-[16px] group transition-all hover:bg-white/5" style="border-left-color: {color}">
                <!-- CIRCULAR STATUS -->
                <div class="relative w-24 h-24 flex items-center justify-center shrink-0">
                    <svg class="w-full h-full transform -rotate-90">
                        <circle cx="48" cy="48" r="40" stroke="rgba(255,255,255,0.05)" stroke-width="8" fill="transparent" />
                        <circle cx="48" cy="48" r="40" stroke="{color}" stroke-width="8" fill="transparent" 
                                stroke-dasharray="251.2" stroke-dashoffset="{251.2 * (1 - (100 if sev==2 else 50 if sev==1 else 25)/100)}" 
                                class="transition-all duration-1000" />
                    </svg>
                    <div class="absolute inset-0 flex items-center justify-center text-xs font-black" style="color: {color}">{label}</div>
                </div>

                <!-- MAIN INFO -->
                <div class="flex-1 space-y-3">
                    <div class="flex items-end gap-6">
                        <h4 class="text-4xl font-black italic tracking-tighter uppercase whitespace-nowrap">{e_dock}</h4>
                        <span class="text-sm font-bold text-gray-500 uppercase tracking-widest pb-1">{e_task}</span>
                    </div>
                    <!-- PROGRESS BAR -->
                    <div class="flex items-center gap-8">
                        <div class="flex-1 bg-white/5 h-2.5 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-orange-600 to-orange-400 rounded-full transition-all duration-1000" style="width: {row['공정률']}%"></div>
                        </div>
                        <div class="text-4xl font-black italic tracking-tighter w-24 text-right">{row['공정률']}%</div>
                    </div>
                </div>

                <!-- PRECAUTION ACTION BUTTON -->
                <button @click="openPopup('{e_safety}', '{e_dock}')" class="px-8 py-5 rounded-2xl bg-white/5 border border-white/10 hover:bg-orange-500 hover:border-orange-400 transition-all text-xs font-black uppercase tracking-widest whitespace-nowrap">
                    ⚠️ 주의사항 확인
                </button>
            </div>
            """

        css_vars = theme.get_css_vars()
        output_path = os.path.join(self.config.BASE_DIR, "smart_yard_dashboard.html")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"""
<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한화오션 AX: 전략 관제 시스템 (v26.0.0)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ {css_vars} }}
        body {{ 
            background: #020617; 
            color: #fff; 
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            background-image: radial-gradient(circle at 0% 0%, rgba(249,115,22,0.1), transparent 50%);
            min-height: 100vh;
        }}
        .glass {{ background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(40px); border: 1px solid rgba(255,255,255,0.05); }}
        [x-cloak] {{ display: none !important; }}
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(249,115,22,0.2); border-radius: 10px; }}
    </style>
</head>
<body x-data="dashboard()" class="p-8 lg:p-20">
    <div class="max-w-[1400px] mx-auto">
        <!-- HEADER -->
        <header class="flex justify-between items-end mb-20">
            <div>
                <div class="flex items-center gap-6 mb-6">
                    <div class="w-16 h-16 bg-orange-500 rounded-2xl flex items-center justify-center text-3xl font-black italic shadow-2xl">H</div>
                    <h1 class="text-6xl font-black italic tracking-tighter uppercase leading-none">STRATEGIC <span class="text-orange-500">AX DASHBOARD</span></h1>
                </div>
                <div class="flex items-center gap-4">
                    <span class="w-12 h-0.5 bg-orange-500"></span>
                    <p class="text-xs font-black text-gray-500 uppercase tracking-[1em]">v26.0.0 전사 통합 관제 시스템</p>
                </div>
            </div>
            <div class="flex gap-10">
                <div class="text-right">
                    <p class="text-[10px] font-black text-gray-700 uppercase tracking-widest mb-2">RISK INDEX</p>
                    <p class="text-5xl font-black italic">{risk_index}</p>
                </div>
                <div class="text-right border-l border-white/10 pl-10">
                    <p class="text-[10px] font-black text-gray-700 uppercase tracking-widest mb-2">YARD PROGRESS</p>
                    <p class="text-5xl font-black italic text-orange-500">{avg_proc:.1f}%</p>
                </div>
            </div>
        </header>

        <!-- MAIN LIST AREA -->
        <main class="space-y-6 pb-40">
            <div class="flex justify-between items-center px-10 mb-10">
                <h2 class="text-2xl font-black italic uppercase tracking-widest text-white/50">Yard Asset Operations</h2>
                <div class="flex items-center gap-4 text-xs font-black text-orange-500 bg-orange-500/5 px-6 py-3 rounded-full border border-orange-500/20">
                    <span class="w-2 h-2 bg-orange-500 rounded-full animate-ping"></span>
                    D-{days_to_go:.0f} (예상 인도: {proj_date})
                </div>
            </div>
            {list_html}
        </main>

        <!-- FOOTER WITH GITHUB LINK -->
        <footer class="flex flex-col items-center py-20 border-t border-white/5 opacity-40">
             <p class="text-[10px] font-black uppercase tracking-[1.5em] mb-12">Proprietary AX Engine | Hanwha Ocean AX Team</p>
             <a href="https://github.com/glory903-devsecops/hanwha-ocean-rpa" target="_blank" 
                class="inline-flex items-center gap-4 px-10 py-5 bg-white text-black rounded-full font-black italic tracking-tighter hover:scale-110 active:scale-95 transition-all">
                 <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                 GITHUB REPOSITORY
             </a>
        </footer>

        <!-- CENTER POPUP OVERLAY -->
        <div x-show="popup.open" x-cloak class="fixed inset-0 z-[1000] flex items-center justify-center p-10 bg-black/80 backdrop-blur-md" x-transition>
            <div class="glass max-w-2xl w-full p-16 rounded-[4rem] border-orange-500/30 relative" @click.away="popup.open = false">
                <button @click="popup.open = false" class="absolute top-10 right-10 text-4xl text-white/50 hover:text-white">&times;</button>
                <div class="flex items-center gap-6 mb-10">
                    <div class="w-16 h-16 bg-orange-500/10 rounded-2xl flex items-center justify-center text-4xl">🤖</div>
                    <div>
                        <h3 class="text-4xl font-black italic tracking-tighter uppercase mb-2">지시사항 <span class="text-orange-500">브리핑</span></h3>
                        <p class="text-[10px] font-bold text-gray-500 uppercase tracking-widest" x-text="`DOCK ID: ${{popup.dock}}`"></p>
                    </div>
                </div>
                <div class="space-y-8">
                    <div>
                        <p class="text-[10px] font-black text-orange-500 uppercase tracking-[0.5em] mb-4">현재 이슈</p>
                        <p class="text-3xl font-black text-white" x-text="popup.issue"></p>
                    </div>
                    <div class="h-px bg-white/10"></div>
                    <div>
                        <p class="text-[10px] font-black text-orange-500 uppercase tracking-[0.5em] mb-4">AX 대응 지침 (Protocol)</p>
                        <p class="text-2xl font-bold text-gray-300 leading-relaxed" x-text="popup.guidance"></p>
                    </div>
                </div>
                <button @click="popup.open = false" class="mt-16 w-full py-6 rounded-3xl bg-orange-500 text-white text-xl font-black italic transition-all hover:scale-[1.02]">알겠습니다. 즉시 시행합니다.</button>
            </div>
        </div>
    </div>

    <script>
        function dashboard() {{
            return {{
                popup: {{ open: false, issue: '', guidance: '', dock: '' }},
                guidelines: {guidelines_json},
                openPopup(issue, dock) {{
                    const match = this.guidelines.find(g => issue.includes(g.ISSUE)) || {{ GUIDANCE: '해당 항목에 대한 자동 프로토콜이 정의되지 않았습니다. 관리 센터에 직접 문의하십시오.' }};
                    this.popup.issue = issue;
                    this.popup.dock = dock;
                    this.popup.guidance = match.GUIDANCE;
                    this.popup.open = true;
                }}
            }}
        }}
    </script>
</body>
</html>
            """)
        print(f"✨ Executive List Dashboard (v26.0.0) Generated: {{output_path}}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
