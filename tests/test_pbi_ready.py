import pandas as pd
import os
import sys

def test_data_integrity():
    print("🔍 Testing Power BI Data Integrity...")
    
    # Paths relative to the script in tests/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    
    files_to_check = [
        (os.path.join(data_dir, "dock_status.csv"), ["도크", "공정률", "현재작업", "안전이슈"]),
        (os.path.join(data_dir, "safety_training_master.xlsx"), ["이름", "팀", "이수여부", "교육일자"])
    ]
    
    all_passed = True
    
    for file_path, expected_cols in files_to_check:
        if not os.path.exists(file_path):
            print(f"❌ Missing file: {file_path}")
            all_passed = False
            continue
            
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            # Check columns
            missing_cols = [col for col in expected_cols if col not in df.columns]
            if missing_cols:
                print(f"❌ {file_path}: Missing columns {missing_cols}")
                all_passed = False
            else:
                print(f"✅ {file_path}: Column structure verified.")
                
            # Simulate DAX Calculation Logic
            if "dock_status.csv" in file_path:
                avg_progress = df["공정률"].mean()
                print(f"   📊 [DAX Simulation] Overall Avg Process: {avg_progress:.2f}%")
                
                alerts = df[df["안전이슈"] != "없음"].shape[0]
                print(f"   ⚠️ [DAX Simulation] Safety Alert Count: {alerts}")
                
            if "safety_training_master.xlsx" in file_path:
                compliance = (df["이수여부"] == "이수").sum() / len(df) * 100
                print(f"   🎓 [DAX Simulation] Training Compliance: {compliance:.2f}%")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            all_passed = False

    return all_passed

if __name__ == "__main__":
    success = test_data_integrity()
    if success:
        print("\n✨ All guidelines verified. Data is READY for Power BI import.")
        sys.exit(0)
    else:
        print("\n⚠️ Verification failed. Please check the errors above.")
        sys.exit(1)
