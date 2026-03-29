import subprocess
import time
import sys
import os

def run_enterprise_ax():
    print("\n" + "="*80)
    print("⚓ HANWHA OCEAN SMART YARD AX: STRATEGIC ENTERPRISE DEPLOYMENT (v25.0.0)")
    print("🚀 Initializing Digital Twin Strategic Insight Engines...")
    print("="*80 + "\n")
    
    # [1] Start Static Dashboard Server (8081)
    print("📡 [1/2] Starting Dashboard Server (Static Global Assets) on Port 8081...")
    p1 = subprocess.Popen([sys.executable, "run_server.py"])
    
    # [2] Start Intelligence Data API (8082)
    print("🤖 [2/2] Starting Intelligence Data API (API & Governance) on Port 8082...")
    p2 = subprocess.Popen([sys.executable, "src/api/server.py"])
    
    time.sleep(3)
    
    print("\n" + "-"*80)
    print("✨ ALL STRATEGIC SYSTEMS ACTIVE (v25.0.0 Global Edition)")
    print("-"*80)
    print("📊 1. Strategic Command (Dashboard): http://localhost:8081/index.html")
    print("🎮 2. Enterprise Launchpad (Gateway):  http://localhost:8081/launchpad.html")
    print("🛡️ 3. Governance Portal (Guidelines): http://localhost:8081/src/viz/admin_guidance.html")
    print("💻 4. ERP Simulator (Data Sync):      http://localhost:8081/src/viz/erp_input.html")
    print("⚙️ 5. Technical API Documentation:    http://localhost:8082/docs")
    print("-"*80)
    print("💡 Tip: Use the Live Dashboard Badge in README for GitHub Pages version.")
    print("="*80 + "\n")
    
    try:
        # Keep both alive
        p1.wait()
        p2.wait()
    except KeyboardInterrupt:
        print("\n🛑 SHUTDOWN SEQUENCE INITIATED: Terminating AX Strategic Assets...")
        p1.terminate()
        p2.terminate()
        print("✅ All systems offline. Enterprise security cleared.")

if __name__ == "__main__":
    run_enterprise_ax()
