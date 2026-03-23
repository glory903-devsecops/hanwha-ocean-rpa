import pandas as pd
import os

# Get absolute path to the data folder
data_dir = r"g:\내 드라이브\99.Develop\한화오션\hanwha-ocean-rpa\data"
file_path = os.path.join(data_dir, "safety_training_master.xlsx")

try:
    df = pd.read_excel(file_path)
    print("Columns:", df.columns.tolist())
    print("\nFirst 5 rows:")
    # Ensure UTF-8 printing or use a safe method
    print(df.head().to_string())
except Exception as e:
    print(f"Error reading file: {e}")
