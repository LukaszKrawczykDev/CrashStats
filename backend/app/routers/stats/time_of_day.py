# app/routers/stats/time_of_day.py

from typing import List, Dict, Any
from collections import defaultdict

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Accident, Date

router = APIRouter(prefix="/stats", tags=["stats"])

# ---------- Request & Response Schemas ----------
class ChartRequest(BaseModel):
    collision_types: List[str] = Field(default_factory=list)

class ChartResponse(BaseModel):
    data: List[Dict[str, Any]]
    types: List[str]

# ---------- Utilities ----------
def hour_to_period(hour: int) -> str:
    if 6 <= hour < 12:
        return "Rano"
    elif 12 <= hour < 18:
        return "Dzień"
    elif 18 <= hour < 22:
        return "Wieczór"
    return "Noc"

PERIODS = ["Noc", "Rano", "Dzień", "Wieczór"]

DEFAULT_TYPES = [
    "1-Car", "2-Car", "Pedestrian", "Moped/Motorcycle",
    "Bus", "Cyclist", "3+ Cars"
]

# ---------- Endpoint ----------
@router.post("/time-of-day-chart", response_model=ChartResponse)
def time_of_day_chart(req: ChartRequest):
    sel_types = req.collision_types or DEFAULT_TYPES
    print(f"📥 Request received: {sel_types}")

    db: Session = SessionLocal()
    try:
        rows = (
            db.query(Accident.collision_type, Date.hour)
            .join(Date, Accident.date_id == Date.id)
            .filter(Accident.collision_type.in_(sel_types))
            .all()
        )

        print(f"📊 Fetched {len(rows)} rows.")

        agg = defaultdict(lambda: defaultdict(int))
        for collision_type, hour in rows:
            if hour is None:
                continue
            period = hour_to_period(hour)
            agg[period][collision_type] += 1

        data = []
        for period in PERIODS:
            row = {"time": period}
            for ct in sel_types:
                row[ct] = agg[period].get(ct, 0)
            data.append(row)

        print("✅ Final data:", data)
        return {"data": data, "types": sel_types}

    except Exception as e:
        print("❌ ERROR:", e)
        raise
    finally:
        db.close()