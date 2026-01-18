from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev ke liye ok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrafficData(BaseModel):
    failed_logins: int
    traffic_spike: bool

@app.get("/")
def root():
    return {"status": "IDS backend running"}

@app.post("/analyze")
def analyze(data: TrafficData):
    alerts = []

    if data.failed_logins > 20:
        alerts.append({
            "title": "Possible Brute Force Attack",
            "severity": "high",
            "riskScore": 85,
            "confidence": 92,
            "reason": "More than 20 failed login attempts detected"
        })

    if data.traffic_spike:
        alerts.append({
            "title": "Traffic Spike Detected",
            "severity": "medium",
            "riskScore": 60,
            "confidence": 80,
            "reason": "Traffic exceeded normal baseline"
        })

    return {
        "alertCount": len(alerts),
        "alerts": alerts
    }
