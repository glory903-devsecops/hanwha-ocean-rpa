import pandas as pd
import os
from filelock import SoftFileLock
from src.core import config

class YardDataRepository:
    """
    Enterprise Repository for Yard Asset Data.
    Features:
    - Thread-safe & Process-safe Soft File Locking (Network-safe).
    - Automatic Schema Initialization.
    - Standardized Read/Write Buffers.
    """
    
    def __init__(self):
        self.csv_path = os.path.join(config.DATA_DIR, "dock_status.csv")
        self.lock_path = self.csv_path + ".lock"
        self._ensure_init()

    def _ensure_init(self):
        """Build initial CSV template if not exists."""
        if not os.path.exists(self.csv_path):
            df = pd.DataFrame(columns=["구역/도크", "공정률", "현재작업", "안전이슈", "마지막업데이트"])
            df.to_csv(self.csv_path, index=False, encoding="utf-8-sig")

    def load_all(self) -> pd.DataFrame:
        """Securely load full yard status."""
        lock = SoftFileLock(self.lock_path, timeout=60)
        with lock:
            return pd.read_csv(self.csv_path)

    def update_record(self, dock_id: str, progress: float, task: str, safety: str, timestamp: str):
        """原子(Atomic) record update with synchronization."""
        lock = SoftFileLock(self.lock_path, timeout=60)
        with lock:
            df = pd.read_csv(self.csv_path)
            # Normalize strings to prevent subtle logic bugs
            dock_id = str(dock_id).strip()
            task = str(task).strip()
            
            mask = (df["구역/도크"] == dock_id) & (df["현재작업"] == task)
            new_row = {
                "구역/도크": dock_id,
                "공정률": float(progress),
                "현재작업": task,
                "안전이슈": safety,
                "마지막업데이트": timestamp
            }
            
            if mask.any():
                df.loc[mask, ["공정률", "안전이슈", "마지막업데이트"]] = [
                    new_row["공정률"], new_row["안전이슈"], new_row["마지막업데이트"]
                ]
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            df.to_csv(self.csv_path, index=False, encoding="utf-8-sig")
            return len(df)
