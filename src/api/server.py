from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field, field_validator
import pandas as pd
import os
import sys
import logging

# [1] Structured Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AX_Server")

# 프로젝트 루트를 path에 추가하여 src 모듈을 불러올 수 있게 함
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core import config, analytics, repository
from src.viz.dashboard import DashboardEngine

# Components Initialization
ax_analytics = analytics.AXAnalytics()
yard_repo = repository.YardDataRepository()

app = FastAPI(title="Hanwha Ocean AX Enterprise Backend", version="13.3.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# [2] Models with Strict Validation
class DockUpdate(BaseModel):
    dock_id: str = Field(..., min_length=2, max_length=50)
    progress: float = Field(..., ge=0, le=100)
    current_task: str = Field(..., min_length=2, max_length=100)
    safety_issue: bool | str
    timestamp: str | None = None

class GuidelineUpdate(BaseModel):
    issue: str = Field(..., min_length=1)
    guidance: str = Field(..., min_length=2)
    severity: str = "WARNING"
    rpa_trigger: str = "NONE"
    bot_id: str = "DISPATCH_ALL"
    delete: bool = False

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": "INTERNAL_SERVER_ERROR"})

@app.get("/api/v1/guidelines")
async def get_guidelines():
    path = os.path.join(config.DATA_DIR, "safety_guidelines.csv")
    if not os.path.exists(path):
        return []
    df = pd.read_csv(path)
    # Ensure columns exist if loading older versions
    for col in ["RPA_TRIGGER", "BOT_ID"]:
        if col not in df.columns: df[col] = "N/A"
    return df.to_dict(orient="records")

@app.post("/api/v1/update-guideline")
async def update_guideline(data: GuidelineUpdate):
    path = os.path.join(config.DATA_DIR, "safety_guidelines.csv")
    df = pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=["ISSUE", "GUIDANCE", "SEVERITY", "RPA_TRIGGER", "BOT_ID"])
    
    if data.delete:
        df = df[df["ISSUE"] != data.issue]
    else:
        # Update or Insert
        new_row = {"ISSUE": data.issue, "GUIDANCE": data.guidance, "SEVERITY": data.severity, "RPA_TRIGGER": data.rpa_trigger, "BOT_ID": data.bot_id}
        if data.issue in df["ISSUE"].values:
            df.loc[df["ISSUE"] == data.issue, ["GUIDANCE", "SEVERITY", "RPA_TRIGGER", "BOT_ID"]] = [data.guidance, data.severity, data.rpa_trigger, data.bot_id]
        else:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
    df.to_csv(path, index=False, encoding="utf-8")
    DashboardEngine().render()
    return {"status": "success", "issue": data.issue}

@app.get("/dashboard")
async def get_dashboard():
    dashboard_path = os.path.join(config.BASE_DIR, "smart_yard_dashboard.html")
    if not os.path.exists(dashboard_path):
        raise HTTPException(status_code=404, detail="Dashboard not generated yet")
    return FileResponse(dashboard_path)

@app.post("/api/v1/update-dock")
async def update_dock(data: DockUpdate):
    try:
        logger.info(f"Update Signal: {data.dock_id} at {data.progress}%")
        safety_str = "위험/주의" if isinstance(data.safety_issue, bool) and data.safety_issue else ("안전" if data.safety_issue == False else str(data.safety_issue))
        total_count = yard_repo.update_record(
            dock_id=data.dock_id, progress=data.progress, task=data.current_task, safety=safety_str,
            timestamp=data.timestamp if data.timestamp else pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        DashboardEngine().render()
        return {"status": "synchronized", "sync_count": total_count, "ref": data.dock_id}
    except Exception as e:
        logger.error(f"Sync Failure: {str(e)}")
        raise HTTPException(status_code=500, detail="Data Synchronization Failed")

@app.get("/api/v1/dashboard-status")
async def get_dashboard_status(dock_id: str | None = None):
    df = yard_repo.load_all()
    if dock_id:
        record = df[df["구역/도크"] == dock_id]
        if record.empty: return JSONResponse(status_code=404, content={"error": "Not Found"})
        res = record.iloc[0].to_dict()
        return {"dock_id": res["구역/도크"], "progress": float(res["공정률"]), "current_task": res["현재작업"], "safety_issue": False if res["안전이슈"] == "안전" else True, "timestamp": res["마지막업데이트"]}
    return df.to_dict(orient="records")

@app.get("/api/v1/export-report")
async def export_report():
    df = yard_repo.load_all()
    content = df.to_csv(index=False, encoding="utf-8-sig")
    return JSONResponse(content={"csv": content, "filename": "yard_report.csv"})

@app.get("/api/v1/analytics")
async def get_analytics():
    df = yard_repo.load_all()
    avg_proc = ax_analytics.calculate_average_progress(df)
    days_to_go, predicted_date = ax_analytics.predict_dday(avg_proc)
    insights = ax_analytics.generate_ai_insights(df)
    return {"status": "success", "d_day": predicted_date, "days_remaining": round(days_to_go, 1), "insights": insights}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
