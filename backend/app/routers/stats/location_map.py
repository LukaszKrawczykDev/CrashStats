# app/routers/stats/location_map.py
from fastapi import APIRouter, Request
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.database import SessionLocal
from app.models.accident import Accident
from app.models.location import Location

router = APIRouter()

# ------------------------------------------------------------
# 1️⃣  KONFIGURACJA  –  stałe widoczne dla całego modułu
# ------------------------------------------------------------
ALLOWED_INJURIES = {
    "Fatal",
    "Non-incapacitating",
    "No injury/unknown",
    "Incapacitating",
}
ALLOWED_FACTORS = {
    "OTHER (ENVIRONMENTAL) - EXPLAIN IN NARR",
    "TIRE FAILURE OR DEFECTIVE",
    "ANIMAL/OBJECT IN ROADWAY",
    "DRIVER ASLEEP OR FATIGUED",
    "OVERCORRECTING/OVERSTEERING",
    "IMPROPER TURNING",
    "ENGINE FAILURE OR DEFECTIVE",
    "DRIVER DISTRACTED - EXPLAIN IN NARRATIVE",
    "OTHER (DRIVER) - EXPLAIN IN NARRATIVE",
    "OVERSIZE/OVERWEIGHT LOAD",
    "UNSAFE LANE MOVEMENT",
    "FAILURE TO YIELD RIGHT OF WAY",
    "ROADWAY SURFACE CONDITION",
    "RAN OFF ROAD RIGHT",
    "PEDESTRIAN ACTION",
    "INSECURE/LEAKY LOAD",
    "OTHER (VEHICLE) - EXPLAIN IN NARRATIVE",
    "CELL PHONE USAGE",
    "HOLES/RUTS IN SURFACE",
    "ACCELERATOR FAILURE OR DEFECTIVE",
    "FOLLOWING TOO CLOSELY",
    "OBSTRUCTION NOT MARKED",
    "OTHER LIGHTS DEFECTIVE",
    "SPEED TOO FAST FOR WEATHER CONDITIONS",
    "DISREGARD SIGNAL/REG SIGN",
    "WRONG WAY ON ONE WAY",
    "BRAKE FAILURE OR DEFECTIVE",
    "HEADLIGHT DEFECTIVE OR NOT ON",
    "STEERING FAILURE",
    "UNSAFE BACKING",
    "TOW HITCH FAILURE",
    "DRIVER ILLNESS",
    "IMPROPER LANE USAGE",
    "VIEW OBSTRUCTED",
    "IMPROPER PASSING",
    "TRAFFIC CONTROL INOPERATIVE/MISSING/OBSC",
    "LEFT OF CENTER",
    "OTHER TELEMATICS IN USE",
    "UNSAFE SPEED",
}
# ------------------------------------------------------------


@router.post("/stats/location-map")
async def location_map(request: Request):
    """
    Zwraca listę punktów na mapę z pełnym opisem (accident + location + weather + date).
    Przyjmuje JSON:
        {
            "injury_types": ["Fatal", "OTHER", ...],
            "primary_factors": ["UNSAFE SPEED", "OTHER", ...]
        }
    """
    payload = await request.json()

    # ------------------  DB ------------------
    db: Session = SessionLocal()

    query = (
        db.query(Accident)
        .options(
            joinedload(Accident.date),
            joinedload(Accident.location).joinedload(Location.weathers),
        )
        .join(Accident.date)
        .join(Accident.location)
    )

    # --------------  FILTRY  ------------------
    # injury_type
    if isinstance(payload.get("injury_types"), list):
        sel = payload["injury_types"]
        wanted = [i for i in sel if i in ALLOWED_INJURIES]
        want_other = "OTHER" in sel

        cond = []
        if wanted:
            cond.append(Accident.injury_type.in_(wanted))
        if want_other:
            cond.append(~Accident.injury_type.in_(ALLOWED_INJURIES))
        if cond:
            query = query.filter(or_(*cond))

    # primary_factor
    if isinstance(payload.get("primary_factors"), list):
        sel = payload["primary_factors"]
        wanted = [pf for pf in sel if pf in ALLOWED_FACTORS]
        want_other = "OTHER" in sel

        cond = []
        if wanted:
            cond.append(Accident.primary_factor.in_(wanted))
        if want_other:
            cond.append(~Accident.primary_factor.in_(ALLOWED_FACTORS))
        if cond:
            query = query.filter(or_(*cond))

    # --------------  EXECUTE  -----------------
    accidents = query.limit(5000).all()
    db.close()

    # --------------  FORMATKA  ----------------
    points: list[dict] = []
    for a in accidents:
        loc = a.location
        if not loc or loc.latitude is None or loc.longitude is None:
            continue

        # spróbuj dopasować pogodę do tej samej daty, w razie braku – pierwsza dostępna
        weather = next(
            (w for w in loc.weathers if w.date_id == a.date_id),  # type: ignore[attr-defined]
            loc.weathers[0] if loc.weathers else None,            # type: ignore[attr-defined]
        )

        points.append(
            {
                # --- pozycja ---
                "lat": loc.latitude,
                "lng": loc.longitude,
                # --- accident ---
                "collision_type": a.collision_type,
                "injury_type": a.injury_type
                if a.injury_type in ALLOWED_INJURIES
                else "OTHER",
                "primary_factor": a.primary_factor
                if a.primary_factor in ALLOWED_FACTORS
                else "OTHER",
                # --- location ---
                "street1": loc.street1,
                "street2": loc.street2,
                # --- weather (może być None) ---
                "temperature": getattr(weather, "temperature", None),
                "rain_24h": getattr(weather, "rain_24h", None),
                "snow_24h": getattr(weather, "snow_24h", None),
                "wind_speed": getattr(weather, "wind_speed", None),
                "wind_deg": getattr(weather, "wind_deg", None),
                "clouds": getattr(weather, "clouds", None),
                "description": getattr(weather, "description", None),
                "category": getattr(weather, "category", None),
                "road_condition": getattr(weather, "road_condition", None),
                # --- date ---
                "year": a.date.year,
                "month": a.date.month,
                "day": a.date.day,
                "hour": a.date.hour,
                "is_weekend": a.date.is_weekend,
            }
        )

    return points