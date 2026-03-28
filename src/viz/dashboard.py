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
    Visualization Engine for Hanwha Ocean AX (v16.0.0).
    ENTERPRISE FILTERABLE DASHBOARD:
    - Real-time client-side filtering (Alpine.js).
    - Fully localized to Korean (K-Shipyard Standard).
    - Large-scale asset monitoring (20+ nodes).
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
        print(f"📡 [Enterprise-AX] Rendering Scale-UP Filterable Dashboard (v16.0.0)...")
        self.load_data()
        
        # 1. High-Level KPI Data
        avg_proc = self.df_dock["공정률"].mean() if not self.df_dock.empty else 0
        days_to_go, proj_date = self.analytics.predict_dday(avg_proc)
        critical_count = len(self.df_dock[self.df_dock["안전이슈"].isin(["위험", "경고", "분진위험", "중량물 주의", "크레인 점검"])])
        
        # 2. Sorting Logic (Severity > Process)
        def get_severity_score(row):
            val = str(row["안전이슈"])
            if any(x in val for x in ["위험", "경고", "중단", "점검", "주의"]): 
                return 0 if "위험" in val or "경고" in val else 1
            return 2 # 정상/안전
            
        self.df_dock["sev_score"] = self.df_dock.apply(get_severity_score, axis=1)
        df_sorted = self.df_dock.sort_values(["sev_score", "공정률"], ascending=[True, True])

        # 3. Component Generation: Individual Priority Cards
        cards_html = ""
        for _, row in df_sorted.iterrows():
            e_dock = html.escape(str(row['구역/도크']))
            e_task = html.escape(str(row['현재작업']))
            e_safety = html.escape(str(row['안전이슈']))
            e_time = html.escape(str(row['마지막업데이트']))
            
            sev = get_severity_score(row)
            # v16 Severity Mapping
            # Status: 0=위험, 1=주의, 2=정상
            palette = {
                0: {"accent": "#EF4444", "bg": "bg-red-500/10", "border": "border-red-500/20", "label": "위험 (Critical)", "sev_key": "critical"},
                1: {"accent": "#F59E0B", "bg": "bg-amber-500/10", "border": "border-amber-500/20", "label": "주의 (Caution)", "sev_key": "warning"},
                2: {"accent": "#10B981", "bg": "bg-emerald-500/5", "border": "border-emerald-500/10", "label": "정상 (Optimal)", "sev_key": "optimal"}
            }
            p = palette.get(sev, palette[2])
            
            # Card Template with data attributes for JS filtering
            cards_html += f"""
            <div class="glass rounded-[2.5rem] p-12 border-l-[18px] group transition-all hover:translate-x-3 {p['border']} animate-fade-in-up card-node" 
                 data-severity="{p['sev_key']}" data-task="{e_task.lower()}" data-name="{e_dock.lower()}"
                 style="border-left-color: {p['accent']}; margin-bottom: var(--h-gap-main);">
                <div class="flex flex-col xl:flex-row justify-between xl:items-center gap-12">
                    <div class="flex-1 space-y-6">
                        <div class="flex items-center gap-6">
                            <h4 class="text-6xl font-black uppercase italic tracking-tighter text-white group-hover:text-orange-500 transition-colors leading-tight">{e_dock}</h4>
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

                    <div class="xl:min-w-[320px] text-right">
                        <div class="text-sm font-black text-gray-600 uppercase mb-4 tracking-[0.3em]">실시간 보안/안전 상태</div>
                        <div class="text-5xl font-black uppercase italic tracking-widest" style="color: {p['accent']}">{e_safety}</div>
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
    <title>한화오션 AX - 미션 컨트롤 센터</title>
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
            background-image: radial-gradient(circle at 50% -20%, rgba(249, 115, 22, 0.15), transparent 85%);
            background-attachment: fixed;
        }}
        .glass {{ background: var(--h-surface); backdrop-filter: var(--h-glass-blur); border: 1px solid var(--h-border); }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(40px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .animate-fade-in-up {{ animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
        
        /* Custom Filter Button Style */
        .filter-btn {{
            @apply px-8 py-3 rounded-2xl font-black text-sm transition-all border border-white/5 uppercase tracking-widest;
        }}
        .filter-btn.active {{
            @apply bg-orange-500 text-white shadow-[0_10px_30px_rgba(249,115,22,0.4)] border-transparent;
        }}
    </style>
</head>
<body class="p-8 lg:p-20" x-data="{{ filter: 'all', search: '' }}">
    
    <!-- COMMAND HEADER (SCALED FOR V16) -->
    <header class="max-w-[1600px] mx-auto flex flex-col lg:flex-row justify-between items-start lg:items-end gap-16 border-b border-white/10 pb-20 mb-16 animate-fade-in-up">
        <div class="space-y-10">
            <div class="flex items-center gap-10">
                <div class="w-24 h-24 bg-gradient-to-tr from-orange-600 to-orange-400 rounded-[2.5rem] flex items-center justify-center text-5xl font-black italic shadow-[0_0_50px_rgba(249,115,22,0.4)]">H</div>
                <div>
                    <h1 class="text-6xl font-black tracking-tighter uppercase italic leading-none">
                        AX <span class="text-orange-500">커맨드 센터</span>
                    </h1>
                    <p class="text-xs text-gray-500 font-bold uppercase tracking-[0.5em] mt-5">v16.0.0 엔터프라이즈 운영 지능화 시스템</p>
                </div>
            </div>
            <div class="flex gap-16">
                <div class="group">
                    <p class="text-[11px] text-gray-600 font-black uppercase mb-2 tracking-[0.2em] group-hover:text-red-500 transition-colors">현재 위기 노드</p>
                    <p class="text-4xl font-black text-red-500 leading-none">{critical_count} <span class="text-xs text-gray-700 font-bold ml-1 uppercase">Alerts</span></p>
                </div>
                <div class="group">
                    <p class="text-[11px] text-gray-600 font-black uppercase mb-2 tracking-[0.2em]">마지막 데이터 갱신</p>
                    <p class="text-4xl font-black text-white font-mono leading-none">{datetime.datetime.now().strftime('%H:%M:%S')}</p>
                </div>
            </div>
        </div>
        
        <div class="flex gap-20">
            <div class="text-right">
                <p class="text-2xl text-gray-400 font-bold uppercase mb-4 tracking-widest">전사 공정 도달율</p>
                <div class="text-7xl font-black text-white font-mono leading-none tracking-tighter">{avg_proc:.1f}<span class="text-xl ml-2 text-gray-700">%</span></div>
            </div>
            <div class="text-right">
                <p class="text-2xl text-orange-500 font-bold uppercase mb-4 tracking-widest">전략적 완공 예정일</p>
                <div class="text-7xl font-black text-orange-500 font-mono leading-none tracking-tighter italic">{proj_date}</div>
            </div>
        </div>
    </header>

    <!-- STICKY FILTER BAR (NEW V16 UX) -->
    <nav class="sticky top-10 z-50 max-w-[1600px] mx-auto mb-16 animate-fade-in-up" style="animation-delay: 0.2s">
        <div class="glass rounded-[2rem] p-6 flex flex-col md:flex-row items-center justify-between gap-6 px-12 border-white/10 shadow-2xl">
            <div class="flex items-center gap-6 text-gray-400 font-bold text-sm">
                <span class="mr-4 text-orange-500 uppercase tracking-widest text-sm">노드 필터링:</span>
                <button @click="filter = 'all'" :class="filter === 'all' ? 'bg-orange-600 text-white shadow-lg' : 'hover:bg-white/5'" class="px-8 py-3 rounded-2xl transition-all font-black text-base uppercase tracking-widest">전체</button>
                <button @click="filter = 'critical'" :class="filter === 'critical' ? 'bg-red-600 text-white shadow-lg' : 'hover:bg-red-900/20'" class="px-8 py-3 rounded-2xl transition-all font-black text-base uppercase tracking-widest">위험</button>
                <button @click="filter = 'warning'" :class="filter === 'warning' ? 'bg-amber-600 text-white shadow-lg' : 'hover:bg-amber-900/20'" class="px-8 py-3 rounded-2xl transition-all font-black text-base uppercase tracking-widest">주의</button>
                <button @click="filter = 'optimal'" :class="filter === 'optimal' ? 'bg-emerald-600 text-white shadow-lg' : 'hover:bg-emerald-900/20'" class="px-8 py-3 rounded-2xl transition-all font-black text-base uppercase tracking-widest">정상</button>
            </div>
            
            <div class="relative w-full md:w-[450px] group">
                <input type="text" x-model="search" placeholder="작업 내용 또는 구역명 검색..." 
                       class="w-full bg-white/5 border border-white/10 rounded-2xl px-8 py-5 text-lg font-bold focus:outline-none focus:border-orange-500 focus:bg-white/10 transition-all placeholder:text-gray-600">
                <div class="absolute right-6 top-1/2 -translate-y-1/2 pointer-events-none opacity-20 group-focus-within:opacity-100 transition-opacity">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
            </div>
        </div>
    </nav>

    <!-- OPERATIONAL NODES (20+ ASSETS) -->
    <main class="max-w-[1600px] mx-auto space-y-12">
        <div class="flex items-center justify-between px-6 pb-4">
            <div class="flex items-center gap-6">
                <div class="w-2 h-8 bg-orange-500 rounded-full"></div>
                <h2 class="text-3xl font-black italic uppercase tracking-tight">전사 야드 자산 가동 현황</h2>
            </div>
            <div class="text-sm font-black uppercase tracking-[0.3em] text-gray-500">
                실시간 야드 자산 모니터링 모드 활성화됨
            </div>
        </div>

        <div class="space-y-10">
            <!-- CARDS CONTENT -->
            <template x-for="card in Array.from(document.querySelectorAll('.card-node'))">
                <div x-show="(filter === 'all' || card.dataset.severity === filter) && (search === '' || card.dataset.name.includes(search.toLowerCase()) || card.dataset.task.includes(search.toLowerCase()))"
                     x-transition:enter="transition ease-out duration-300 transform"
                     x-transition:enter-start="opacity-0 translate-y-4"
                     x-transition:enter-end="opacity-100 translate-y-0"
                     class="contents">
                    <div x-html="card.outerHTML"></div>
                </div>
            </template>
            
            <!-- RAW CARDS DATA (HIDDEN FOR ALPINE CONSUMPTION) -->
            <div class="hidden">
                {cards_html}
            </div>
        </div>
    </main>

    <footer class="mt-60 mb-20 flex flex-col items-center gap-8 opacity-20">
        <div class="w-60 h-px bg-gradient-to-r from-transparent via-white to-transparent"></div>
        <p class="text-xs font-bold uppercase tracking-[1.5em] text-center">HANWHA OCEAN AX PROPRIETARY CONTROL MESH V16.0.0</p>
    </footer>

    <script>
        // Alpine data injection helper if needed
        document.addEventListener('alpine:init', () => {{
            console.log('AX Logic Matrix Initialized');
        }});
    </script>
</body>
</html>
            """)
        print(f"✨ Enterprise Scaled Dashboard (v16.0.0) Generated: {output_path}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
