import pandas as pd
import os
import logging
from datetime import datetime
from filelock import SoftFileLock, Timeout
from src.core import config

# Enterprise Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | [%(levelname)s] | %(name)s : %(message)s'
)
logger = logging.getLogger("AX-Repository")

class YardDataRepository:
    """
    Enterprise Repository for Hanwha Ocean Yard Asset Data.
    Designed for reliability on distributed network drives (Google Drive).
    """
    
    def __init__(self):
        self.csv_path = os.path.join(config.DATA_DIR, "dock_status.csv")
        self.lock_path = self.csv_path + ".lock"
        self._ensure_init()

    def _ensure_init(self):
        """Initializes the persistent store if missing."""
        if not os.path.exists(self.csv_path):
            try:
                df = pd.DataFrame(columns=["구역/도크", "공정률", "현재작업", "안전이슈", "마지막업데이트"])
                df.to_csv(self.csv_path, index=False, encoding="utf-8-sig")
                logger.info(f"Initialized new data store at: {self.csv_path}")
            except Exception as e:
                logger.critical(f"Storage Initialization Failed: {e}")

    def load_all(self) -> pd.DataFrame:
        """Process-safe load of yard state."""
        lock = SoftFileLock(self.lock_path, timeout=60)
        try:
            with lock:
                return pd.read_csv(self.csv_path)
        except Timeout:
            logger.error("Data Load Timeout: Lock acquisition failed.")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Data Load Error: {e}")
            return pd.DataFrame()

    def update_record(self, dock_id: str, progress: float, task: str, safety: str, timestamp: str = None):
        """Atomic record synchronization with data validation."""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lock = SoftFileLock(self.lock_path, timeout=60)
        try:
            with lock:
                df = pd.read_csv(self.csv_path)
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
                logger.info(f"Synchronized Asset: {dock_id} ({progress}%)")
                return True
        except Timeout:
            logger.warning(f"Sync Conflict: '{dock_id}' update deferred.")
            return False
        except Exception as e:
            logger.error(f"Critical Sync Failure for '{dock_id}': {e}")
            return False
