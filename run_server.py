from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import os
import uvicorn
import datetime
import logging
from src.viz.dashboard import DashboardEngine

# Enterprise Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AX-Unified-Server")

app = FastAPI(title="Hanwha Ocean AX Unified Server")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

class DockUpdate(BaseModel):
    dock: str
    progress: float
    task: str
    safety: str

class GuidelineUpdate(BaseModel):
    issue: str
    guidance: str

# Helper to re-render dashboard
def refresh_dashboard():
    try:
        engine = DashboardEngine()
        engine.render()
        logger.info("Dashboard re-rendered successfully.")
    except Exception as e:
        logger.error(f"Failed to re-render dashboard: {e}")

@app.post("/api/update_dock")
async def update_dock(data: DockUpdate):
    csv_path = os.path.join(DATA_DIR, "dock_status.csv")
    df = pd.read_csv(csv_path)
    
    # Check if exists
    mask = df["구역/도크"] == data.dock
    if mask.any():
        df.loc[mask, "공정률"] = data.progress
        df.loc[mask, "현재작업"] = data.task
        df.loc[mask, "안전이슈"] = data.safety
        df.loc[mask, "마지막업데이트"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Updated existing dock: {data.dock}")
    else:
        new_row = {
            "구역/도크": data.dock,
            "공정률": data.progress,
            "현재작업": data.task,
            "안전이슈": data.safety,
            "마지막업데이트": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        logger.info(f"Added new dock: {data.dock}")
    
    df.to_csv(csv_path, index=False)
    refresh_dashboard()
    return {"status": "success", "dock": data.dock}

@app.post("/api/update_guideline")
async def update_guideline(data: GuidelineUpdate):
    csv_path = os.path.join(DATA_DIR, "safety_guidelines.csv")
    df = pd.read_csv(csv_path)
    
    # Check if exists
    mask = df["ISSUE"] == data.issue
    if mask.any():
        df.loc[mask, "GUIDANCE"] = data.guidance
        logger.info(f"Updated guideline for: {data.issue}")
    else:
        new_row = {"ISSUE": data.issue, "GUIDANCE": data.guidance}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        logger.info(f"Added new guideline for: {data.issue}")
    
    df.to_csv(csv_path, index=False)
    refresh_dashboard()
    return {"status": "success", "issue": data.issue}

# Serve Static Files
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/{filename}")
async def read_file(filename: str):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

# Mount docs for images
app.mount("/docs", StaticFiles(directory=os.path.join(BASE_DIR, "docs")), name="docs")

if __name__ == "__main__":
    # Initial render
    refresh_dashboard()
    logger.info("⚓ Hanwha Ocean AX Unified Command Server starting on http://localhost:8081")
    uvicorn.run(app, host="0.0.0.0", port=8081)
