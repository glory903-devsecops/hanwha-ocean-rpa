import sys
import os

# Add src to python path to allow absolute imports within the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_engine.generator import generate_enterprise_datasets
from src.viz.dashboard import DashboardEngine

def main():
    print("🚀 [AX Command Center] Starting Enterprise Smart Yard Pipeline...")
    
    try:
        # Phase 1: Data Accumulation (Massive Simulation)
        generate_enterprise_datasets()
        
        # Phase 2: Analytics & Verification (TBD in next version)
        
        # Phase 3: Premium Visualization
        viz = DashboardEngine()
        viz.render()
        
        print("\n✅ Hanwha Ocean AX Pipeline Completed: v2.5.0")
    except Exception as e:
        print(f"\n❌ Pipeline Failure: {e}")

if __name__ == "__main__":
    main()
