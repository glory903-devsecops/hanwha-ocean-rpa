import pandas as pd
import os

def test_data_integrity():
    print("🔍 Testing Power BI Data Integrity...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    
    files_to_check = [
        (os.path.join(data_dir, "dock_status.csv"), ["ID", "구역/도크", "건립선종", "공정률", "현재작업", "안전이슈"]),
        (os.path.join(data_dir, "safety_training_master.xlsx"), ["이름", "팀", "이수여부", "교육일자"])
    ]
    
    all_passed = True
    for file_path, expected_cols in files_to_check:
        if not os.path.exists(file_path):
            print(f"❌ File NOT found: {file_path}")
            all_passed = False
            continue
            
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        missing_cols = [col for col in expected_cols if col not in df.columns]
        if missing_cols:
            print(f"❌ {os.path.basename(file_path)}: Missing columns {missing_cols}")
            all_passed = False
        else:
            print(f"✅ {os.path.basename(file_path)}: Column structure verified.")

    if not all_passed:
        raise Exception("Data Integrity Check Failed.")
    print("\n✨ All guidelines verified. Data is READY for AX Dashboard.")

if __name__ == "__main__":
    test_data_integrity()
