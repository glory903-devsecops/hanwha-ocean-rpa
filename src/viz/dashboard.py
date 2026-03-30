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
    Visualization Engine for Hanwha Ocean AX (v26.3.0 - Strategic Command Edition).
    STRATEGIC COMMAND & CONTROL INTERFACE:
    - [DASHBOARD UI]: Clean List format with Horizontal Search & Filter Bar.
    - [PROGRESS VIZ]: Each list item has a Circular Progress Chart (Primary indicator).
    - [INTERACTION]: Dynamic Action Buttons (e.g., ⚠️ [위험] 크레인 오작동 지시 확인).
    - [ALPHINE.JS]: Client-side filtering and real-time search.
    """
    
    def __init__(self):
        self.analytics = analytics.AXAnalytics()
        self.config = config
        self.theme = theme.THEME
        self.df_dock = None
        
    def load_data(self):
        csv_path = os.path.join(self.config.DATA_DIR, "dock_status.csv")
        self.df_dock = pd.read_csv(csv_path)
        # Keep original issue for better matching if needed, but for display we clean prefixes
        self.df_dock["표기_안전이슈"] = self.df_dock["안전이슈"].copy()
        for prefix in ["[주의]", "[기상]", "[위험]", "[경고]", "[장비]"]:
             self.df_dock["표기_안전이슈"] = self.df_dock["표기_안전이슈"].str.replace(prefix + " ", "", regex=False)

    def render(self):
        print(f"📡 [Enterprise-AX] 전략 관제 대시보드 렌더링 중 (v26.3.0 검색/필터 강화 버전)...")
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
            e_safety_display = html.escape(str(row['표기_안전이슈']))
            e_safety_raw = html.escape(str(row['안전이슈']))
            progress = float(row['공정률'])
            
            sev = row['sev_score']
            color = {0: "#EF4444", 1: "#F59E0B", 2: "#10B981"}.get(sev)
            label = {0: "위험", 1: "주의", 2: "정상"}.get(sev)
            
            # Dynamic Button Label
            if label != "정상":
                btn_label = e_safety_display
            else:
                btn_label = "특이사항 없음"

            # Circular Progress
            circ_offset = 301.6 * (1 - progress/100)
            
            # Button Classes based on Severity
            btn_class = {
                0: "bg-red-600/10 border-red-500/30 text-red-500 hover:bg-red-600 hover:text-white shadow-[0_0_30px_rgba(239,68,68,0.2)]",
                1: "bg-amber-500/10 border-amber-400/30 text-amber-500 hover:bg-amber-500 hover:text-white shadow-[0_0_30px_rgba(245,158,11,0.2)]",
                2: "bg-emerald-600/10 border-emerald-500/30 text-emerald-400 hover:bg-emerald-600 hover:text-white shadow-[0_0_30px_rgba(16,185,129,0.2)]"
            }.get(sev)

            list_html += f"""
            <div class="glass flex items-center gap-12 p-8 rounded-[2.5rem] border-l-[16px] group transition-all hover:bg-white/5" 
                 style="border-left-color: {color}"
                 x-show="(filterStatus === '전체' || filterStatus === '{label}') && (searchQuery === '' || '{e_dock}'.includes(searchQuery))"
                 x-transition:enter="transition ease-out duration-300"
                 x-transition:enter-start="opacity-0 transform -translate-y-4"
                 x-transition:enter-end="opacity-100 transform translate-y-0">
                <!-- 원형 진행률 그래프 -->
                <div class="relative w-28 h-28 flex items-center justify-center shrink-0">
                    <svg class="w-full h-full transform -rotate-90">
                        <circle cx="56" cy="56" r="48" stroke="rgba(255,255,255,0.05)" stroke-width="10" fill="transparent" />
                        <circle cx="56" cy="56" r="48" stroke="{color}" stroke-width="10" fill="transparent" 
                                stroke-dasharray="301.6" stroke-dashoffset="{circ_offset}" 
                                class="transition-all duration-1000" />
                    </svg>
                    <div class="absolute inset-0 flex flex-col items-center justify-center">
                        <span class="text-2xl font-black italic text-white leading-none">{progress}%</span>
                        <span class="text-[8px] font-bold uppercase tracking-widest mt-1" style="color: {color}">{label}</span>
                    </div>
                </div>

                <!-- 주요 정보 영역 -->
                <div class="flex-1">
                    <div class="flex flex-col gap-2">
                        <h4 class="text-4xl font-black italic tracking-tighter uppercase whitespace-nowrap text-white group-hover:text-orange-500 transition-colors">{e_dock}</h4>
                        <div class="flex items-center gap-4">
                            <span class="px-4 py-1 rounded bg-white/5 text-xs font-bold text-gray-500 uppercase tracking-widest">현재작업: {e_task}</span>
                            <span class="w-2 h-2 rounded-full bg-white/10"></span>
                            <span class="text-xs font-black italic text-gray-600">안전상태: {e_safety_display}</span>
                        </div>
                    </div>
                </div>

                <!-- 액션 버튼 -->
                <div class="text-right space-y-4">
                    <button @click="openPopup('{e_safety_raw}', '{e_dock}')" 
                            class="px-10 py-6 rounded-3xl border transition-all text-xl font-black uppercase tracking-tighter whitespace-nowrap shadow-2xl {btn_class}">
                        {btn_label}
                    </button>
                </div>
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
    <title>한화오션 AX: 전략 관제 시스템 (v26.3.0)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&family=Noto+Sans+KR:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ {css_vars} }}
        body {{ 
            background: #020617; 
            color: #fff; 
            font-family: 'Outfit', 'Noto Sans KR', sans-serif;
            background-image: radial-gradient(circle at 10% 20%, rgba(249,115,22,0.1), transparent 50%),
                              radial-gradient(circle at 90% 80%, rgba(0,242,255,0.05), transparent 50%);
            min-height: 100vh;
        }}
        .glass {{ background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(40px); border: 1px solid rgba(255,255,255,0.05); }}
        .filter-btn {{
            @apply px-8 py-3 rounded-full text-xs font-black uppercase tracking-widest transition-all;
        }}
        .filter-btn.active {{
            @apply bg-orange-500 text-white shadow-[0_0_20px_rgba(249,115,22,0.4)];
        }}
        [x-cloak] {{ display: none !important; }}
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(249,115,22,0.2); border-radius: 10px; }}
    </style>
</head>
<body x-data="dashboard()" class="p-8 lg:p-20">
    <div class="max-w-[1400px] mx-auto">
        <!-- 헤더 영역 -->
        <header class="flex justify-between items-end mb-20">
            <div>
                <div class="flex items-center gap-8 mb-6">
                    <div class="w-16 h-16 bg-gradient-to-tr from-orange-600 to-orange-400 rounded-2xl flex items-center justify-center text-4xl font-black italic shadow-2xl">H</div>
                    <h1 class="text-6xl font-black italic tracking-tighter uppercase leading-none">전략 관제 <span class="text-orange-500">데이터 센터</span></h1>
                </div>
                <div class="flex items-center gap-4">
                    <span class="w-12 h-1 bg-orange-500 rounded-full"></span>
                    <p class="text-[10px] font-black text-gray-700 uppercase tracking-[1em]">전사 통합 실시간 모니터링 시스템 v26.3.0</p>
                </div>
            </div>
            <div class="flex gap-12">
                <div class="text-right">
                    <p class="text-[10px] font-black text-gray-700 uppercase tracking-widest mb-2">리스크 인덱스 (QRI)</p>
                    <p class="text-6xl font-black italic tabular-nums">{risk_index}</p>
                </div>
                <div class="text-right border-l border-white/10 pl-12">
                    <p class="text-[10px] font-black text-gray-700 uppercase tracking-widest mb-2">전체 평균 공정률</p>
                    <p class="text-6xl font-black italic text-orange-500 tabular-nums">{avg_proc:.1f}%</p>
                </div>
            </div>
        </header>

        <!-- 검색 및 필터 가로형 바 -->
        <div class="glass flex flex-wrap items-center justify-between gap-10 p-8 rounded-[3rem] mb-16 border-orange-500/10 shadow-2xl">
            <div class="flex-1 min-w-[300px] relative group">
                <div class="absolute left-8 top-1/2 -translate-y-1/2 text-orange-500/50 group-focus-within:text-orange-500 transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
                <input x-model="searchQuery" type="text" placeholder="도크 이름 또는 구역 검색..." 
                       class="w-full bg-black/20 border border-white/5 rounded-2xl py-6 pl-20 pr-10 text-xl font-bold text-white focus:outline-none focus:border-orange-500/50 transition-all placeholder:text-gray-700">
            </div>
            
            <div class="flex items-center gap-4 bg-black/20 p-2 rounded-full border border-white/5">
                <button @click="filterStatus = '전체'" :class="filterStatus === '전체' ? 'bg-orange-500 text-white' : 'text-gray-500 hover:text-white'" class="px-8 py-3 rounded-full text-xs font-black uppercase tracking-widest transition-all">전체</button>
                <button @click="filterStatus = '위험'" :class="filterStatus === '위험' ? 'bg-red-600 text-white shadow-[0_0_20px_rgba(239,68,68,0.4)]' : 'text-gray-500 hover:text-red-400'" class="px-8 py-3 rounded-full text-xs font-black uppercase tracking-widest transition-all">심각/위험</button>
                <button @click="filterStatus = '주의'" :class="filterStatus === '주의' ? 'bg-amber-500 text-white shadow-[0_0_20px_rgba(245,158,11,0.4)]' : 'text-gray-500 hover:text-amber-400'" class="px-8 py-3 rounded-full text-xs font-black uppercase tracking-widest transition-all">주의</button>
                <button @click="filterStatus = '정상'" :class="filterStatus === '정상' ? 'bg-emerald-600 text-white shadow-[0_0_20px_rgba(16,185,129,0.4)]' : 'text-gray-500 hover:text-emerald-400'" class="px-8 py-3 rounded-full text-xs font-black uppercase tracking-widest transition-all">정상/안전</button>
            </div>
        </div>

        <!-- 메인 도크 리스트 -->
        <main class="space-y-6 pb-40">
            <div class="flex justify-between items-center px-10 mb-12">
                <h2 class="text-2xl font-black italic uppercase tracking-[0.3em] text-white/40">야드 자산 운영 현황</h2>
                <div class="flex items-center gap-4 text-xs font-black text-orange-500 bg-orange-500/10 px-8 py-4 rounded-full border border-orange-500/20 shadow-2xl">
                    <span class="w-2.5 h-2.5 bg-orange-500 rounded-full animate-ping"></span>
                    D-{days_to_go:.0f} (최종 예상 인도일: {proj_date})
                </div>
            </div>
            {list_html}
            
            <!-- 데이터 없음 메시지 -->
            <div x-show="Object.keys($el.parentElement.children).filter(i => $el.parentElement.children[i].style.display !== 'none').length <= 2" x-cloak class="py-40 text-center">
                <p class="text-4xl font-black text-white/10 uppercase italic tracking-widest">검색 결과가 없습니다</p>
            </div>
        </main>

        <!-- 푸터 영역 -->
        <footer class="flex flex-col items-center py-20 border-t border-white/10 opacity-30 mt-20">
             <a href="https://github.com/glory903-devsecops/hanwha-ocean-rpa" target="_blank" 
                class="inline-flex items-center gap-4 px-8 py-4 bg-white text-black rounded-full font-bold italic tracking-tighter hover:scale-110 active:scale-95 transition-all shadow-2xl text-[10px]">
                 <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                 VISIT GITHUB REPOSITORY
             </a>
        </footer>

        <!-- 중앙 지시사항 팝업 오버레이 -->
        <div x-show="popup.open" x-cloak class="fixed inset-0 z-[1000] flex items-center justify-center p-10 bg-black/80 backdrop-blur-md" x-transition>
            <div class="glass max-w-2xl w-full p-16 rounded-[4rem] border-orange-500/30 relative" @click.away="popup.open = false">
                <button @click="popup.open = false" class="absolute top-10 right-10 text-4xl text-white/50 hover:text-white">&times;</button>
                <div class="flex items-center gap-6 mb-10">
                    <div class="w-20 h-20 bg-orange-500/20 rounded-3xl flex items-center justify-center text-5xl">🤖</div>
                    <div>
                        <h3 class="text-4xl font-black italic tracking-tighter uppercase mb-2">AX <span class="text-orange-500">운영 지시사항</span></h3>
                        <p class="text-[10px] font-bold text-gray-500 uppercase tracking-widest" x-text="`관제 대상 도크: ${{popup.dock}}`"></p>
                    </div>
                </div>
                <div class="space-y-10">
                    <div>
                        <p class="text-[10px] font-black text-orange-500 uppercase tracking-[0.5em] mb-4">탐지된 안전 이슈</p>
                        <p class="text-3xl font-black text-white" x-text="popup.issueDisplay"></p>
                    </div>
                    <div class="h-px bg-white/10"></div>
                    <div>
                        <p class="text-[10px] font-black text-orange-500 uppercase tracking-[0.5em] mb-4">대응 지침 (프로토콜)</p>
                        <p class="text-2xl font-bold text-gray-300 leading-relaxed italic" x-text="popup.guidance"></p>
                    </div>
                </div>
                <button @click="popup.open = false" class="mt-16 w-full py-8 rounded-3xl bg-orange-500 text-white text-2xl font-black italic transition-all hover:scale-[1.02] shadow-2xl">지시 확인: 즉시 집행</button>
            </div>
        </div>
    </div>

    <script>
        function dashboard() {{
            return {{
                popup: {{ open: false, issueDisplay: '', guidance: '', dock: '' }},
                guidelines: {guidelines_json},
                searchQuery: '',
                filterStatus: '전체',
                openPopup(rawIssue, dock) {{
                    const prefixes = ["[주의]", "[기상]", "[위험]", "[경고]", "[장비]"];
                    let cleanIssue = rawIssue;
                    prefixes.forEach(p => {{ cleanIssue = cleanIssue.replace(p + " ", ""); }});
                    
                    const match = this.guidelines.find(g => cleanIssue.includes(g.ISSUE) || rawIssue.includes(g.ISSUE));
                    
                    this.popup.issueDisplay = cleanIssue;
                    this.popup.dock = dock;
                    this.popup.guidance = match ? match.GUIDANCE : '대응 프로토콜 분석 중입니다. 현장 즉시 보고를 권장합니다.';
                    this.popup.open = true;
                }}
            }}
        }}
    </script>
</body>
</html>
            """)
        print(f"✨ 전략 관제 대시보드 (v26.3.0 검색/필터 강화 완료) 생성 완료: {{output_path}}")

if __name__ == "__main__":
    engine = DashboardEngine()
    engine.render()
