from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
import sys

# 프로젝트 루트를 path에 추가하여 src 모듈을 불러올 수 있게 함
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core import config
from src.viz.dashboard import DashboardEngine

app = FastAPI(title="Hanwha Ocean ERP Backend")

# CORS 설정 (포털에서 API 호출 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DockUpdate(BaseModel):
    dock_id: str
    progress: float
    current_task: str
    safety_issue: bool | str
    timestamp: str | None = None

@app.post("/api/v1/update-dock")
async def update_dock(data: DockUpdate):
    try:
        csv_path = os.path.join(config.DATA_DIR, "dock_status.csv")
        
        # Load existing data or create new
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            df = pd.DataFrame(columns=["구역/도크", "공정률", "현재작업", "안전이슈", "마지막업데이트"])

        safety_str = "위험/주의" if isinstance(data.safety_issue, bool) and data.safety_issue else ("안전" if data.safety_issue == False else str(data.safety_issue))

        new_row = {
            "구역/도크": data.dock_id,
            "공정률": data.progress,
            "현재작업": data.current_task,
            "안전이슈": safety_str,
            "마지막업데이트": data.timestamp if data.timestamp else pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if data.dock_id in df["구역/도크"].values:
            df.loc[df["구역/도크"] == data.dock_id, ["공정률", "현재작업", "안전이슈", "마지막업데이트"]] = [
                data.progress, data.current_task, safety_str, new_row["마지막업데이트"]
            ]
        else:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        DashboardEngine().render()
        
        return {
            "status": "saved", 
            "message": f"Updated {data.dock_id} successfully.",
            "file": csv_path,
            "updated_record_count": 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/dashboard-status")
async def get_dashboard_status(dock_id: str | None = None):
    csv_path = os.path.join(config.DATA_DIR, "dock_status.csv")
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="No data available")
    
    df = pd.read_csv(csv_path)
    if dock_id:
        record = df[df["구역/도크"] == dock_id]
        if record.empty:
            return {"error": "Dock not found"}
        # Return in TestSprite expected format
        res = record.iloc[0].to_dict()
        return {
            "dock_id": res["구역/도크"],
            "progress": res["공정률"],
            "current_task": res["현재작업"],
            "safety_issue": res["안전이슈"],
            "timestamp": res["마지막업데이트"]
        }
    return df.to_dict(orient="records")

@app.get("/api/v1/export-report")
async def export_report():
    csv_path = os.path.join(config.DATA_DIR, "dock_status.csv")
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="No data available")
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    return {"status": "success", "content": content}

@app.get("/api/v1/analytics")
async def get_analytics(dock_id: str | None = None):
    return {"d_day": "2026-05-15", "recommendation": "최적 조업 유지"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
