import subprocess
import time
import sys
import os

def run_enterprise_ax():
    print("\n" + "="*80)
    print("⚓ HANWHA OCEAN SMART YARD AX: STRATEGIC HUB DEPLOYMENT (v26.0.0)")
    print("🚀 Initializing Unified Enterprise Command & Control Hub...")
    print("="*80 + "\n")
    
    # [1] Start Unified Command Server (8081)
    # This server handles Static Files, ERP APIs, and Dashboard Rendering.
    print("📡 [Unified] Starting Strategic Command Server on Port 8081...")
    p1 = subprocess.Popen([sys.executable, "run_server.py"])
    
    time.sleep(3)
    
    print("\n" + "-"*80)
    print("✨ ALL AX SYSTEMS ACTIVE (v26.0.0 Enterprise Elite)")
    print("🌐 ACCESS PORTAL (LOCAL): http://localhost:8081/index.html")
    print("-" * 80)
    print("📦 1. 통합 런처 (Launchpad):     http://localhost:8081/index.html")
    print("📊 2. 전략 관제 (Dashboard):     http://localhost:8081/smart_yard_dashboard.html")
    print("📝 3. 도크 입력 (RPA/ERP):      http://localhost:8081/erp_input.html")
    print("⚙️ 4. 지휘 관리 (Admin Portal):  http://localhost:8081/admin_portal.html")
    print("-" * 80)
    print("💡 Tip: 제출용 데모 링크는 README.md를 확인하십시오.")
    print("="*80 + "\n")
    
    try:
        p1.wait()
    except KeyboardInterrupt:
        print("\n🛑 SHUTDOWN SEQUENCE INITIATED: Terminating Unified Server...")
        p1.terminate()
        print("✅ All systems offline. Hanwha Ocean AX cleared.")

if __name__ == "__main__":
    run_enterprise_ax()
