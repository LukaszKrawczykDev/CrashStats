# app/routers/filters_meta.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List

from app.database import SessionLocal
from app.auth import get_current_user
from app.models.accident import Accident
from app.models.date import Date
from app.models.weather import Weather

router = APIRouter()

# Predefiniowane wartości (z klasyfikacją "Other")
PREDEFINED_VALUES: Dict[str, List[str]] = {
    "injury_type": [
        "Fatal", "Non-incapacitating", "No injury/unknown", "Incapacitating"
    ],
    "primary_factor": [
        "OTHER (ENVIRONMENTAL) - EXPLAIN IN NARR", "TIRE FAILURE OR DEFECTIVE",
        "ANIMAL/OBJECT IN ROADWAY", "DRIVER ASLEEP OR FATIGUED", "OVERCORRECTING/OVERSTEERING",
        "IMPROPER TURNING", "ENGINE FAILURE OR DEFECTIVE", "DRIVER DISTRACTED - EXPLAIN IN NARRATIVE",
        "OTHER (DRIVER) - EXPLAIN IN NARRATIVE", "OVERSIZE/OVERWEIGHT LOAD",
        "UNSAFE LANE MOVEMENT", "FAILURE TO YIELD RIGHT OF WAY", "ROADWAY SURFACE CONDITION",
        "RAN OFF ROAD RIGHT", "PEDESTRIAN ACTION", "INSECURE/LEAKY LOAD",
        "OTHER (VEHICLE) - EXPLAIN IN NARRATIVE", "CELL PHONE USAGE", "HOLES/RUTS IN SURFACE",
        "ACCELERATOR FAILURE OR DEFECTIVE", "FOLLOWING TOO CLOSELY", "OBSTRUCTION NOT MARKED",
        "OTHER LIGHTS DEFECTIVE", "SPEED TOO FAST FOR WEATHER CONDITIONS",
        "DISREGARD SIGNAL/REG SIGN", "WRONG WAY ON ONE WAY", "BRAKE FAILURE OR DEFECTIVE",
        "HEADLIGHT DEFECTIVE OR NOT ON", "STEERING FAILURE", "UNSAFE BACKING",
        "TOW HITCH FAILURE", "DRIVER ILLNESS", "IMPROPER LANE USAGE", "VIEW OBSTRUCTED",
        "IMPROPER PASSING", "TRAFFIC CONTROL INOPERATIVE/MISSING/OBSC", "LEFT OF CENTER",
        "OTHER TELEMATICS IN USE", "UNSAFE SPEED"
    ],
    "description": [
        "light rain", "moderate rain", "snow", "overcast", "partly cloudy", "heavy rain", "clear sky"
    ],
    "road_condition": ["snowy", "icy", "wet", "dry"],
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def classify_with_other(raw: List[str | None], predefined: List[str]) -> List[str]:
    raw = sorted(set(v for v in raw if v is not None))  # lepsze filtrowanie NULL
    extra = [v for v in raw if v not in predefined]
    result = [v for v in predefined if v in raw]
    if extra:
        result.append("Other")
    return result


@router.get("/data/filters/meta")
def get_filters_meta(db: Session = Depends(get_db), user=Depends(get_current_user)):
    output: Dict[str, List] = {}

    # --- predefiniowane pola ---
    for field, predefined in PREDEFINED_VALUES.items():
        model = Accident if hasattr(Accident, field) else Weather
        values = [row[0] for row in db.query(getattr(model, field)).distinct()]
        output[field] = classify_with_other(values, predefined)

    # --- daty ---
    for field in ["year", "month", "day", "hour"]:
        values = db.query(getattr(Date, field)).distinct().all()
        output[field] = sorted({v[0] for v in values if v[0] is not None})

    return output