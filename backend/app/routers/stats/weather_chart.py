from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.database import SessionLocal
from app.models.accident import Accident
from app.models.weather import Weather

router = APIRouter(prefix="/stats", tags=["stats"])

INJURY_KEYS = [
    "Fatal",
    "Incapacitating",
    "Non-incapacitating",
    "No injury/unknown",
]

DIMENSION_MAP = {
    "category": Weather.category,
    "road_condition": Weather.road_condition,
}

@router.post("/weather-chart")
async def weather_chart(request: Request):
    body = await request.json()
    dimension_key = body.get("dimension", "category")
    dim_column = DIMENSION_MAP.get(dimension_key, Weather.category)

    filter_injuries = set(body.get("injury_types", []))
    include_all = not filter_injuries

    db: Session = SessionLocal()

    query = (
        db.query(
            dim_column.label("dim"),
            Accident.injury_type,
            func.count().label("cnt"),
        )
        .join(
            Weather,
            and_(
                Weather.date_id == Accident.date_id,
                Weather.location_id == Accident.location_id,
                ),
        )
        .group_by("dim", Accident.injury_type)
    )

    if not include_all:
        if "OTHER" in filter_injuries:
            query = query.filter(
                ~Accident.injury_type.in_(set(INJURY_KEYS) - {"OTHER"})
                | Accident.injury_type.in_(filter_injuries - {"OTHER"})
            )
        else:
            query = query.filter(Accident.injury_type.in_(filter_injuries))

    rows = query.all()
    db.close()
    tmp = {}
    for dim, inj, cnt in rows:
        if dim is None:
            dim = "Nieznane"
        inj = inj if inj in INJURY_KEYS else "OTHER"
        tmp.setdefault(dim, {k: 0 for k in INJURY_KEYS + ["OTHER"]})
        tmp[dim][inj] += cnt

    ordered = sorted(tmp.items(), key=lambda x: -sum(x[1].values()))

    return [
        {"dim": dim, **counts} for dim, counts in ordered
    ]