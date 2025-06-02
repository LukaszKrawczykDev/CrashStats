from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.database import SessionLocal
from app.models import Accident, Date
from collections import defaultdict

router = APIRouter(prefix="/stats")

@router.post("/time-of-day-chart")
def time_of_day_chart(request: Request):
    db: Session = SessionLocal()
    body = request.json() if callable(getattr(request, "json", None)) else {}

    accident_type_filter = set(body.get("collision_types", []))

    # Zakresy czasowe do kategorii pory dnia
    time_of_day_case = case(
        (
            (Date.hour >= 22) | (Date.hour < 6),
            "Noc"
        ),
        (
            (Date.hour >= 6) & (Date.hour < 12),
            "Rano"
        ),
        (
            (Date.hour >= 12) & (Date.hour < 18),
            "Dzień"
        ),
        (
            (Date.hour >= 18) & (Date.hour < 22),
            "Wieczór"
        ),
        else_="Inna"
    )

    query = (
        db.query(
            time_of_day_case.label("time_of_day"),
            Accident.collision_type,
            func.count().label("count")
        )
        .join(Date, Accident.date_id == Date.id)
        .group_by("time_of_day", Accident.collision_type)
    )

    if accident_type_filter:
        query = query.filter(Accident.collision_type.in_(accident_type_filter))

    results = query.all()

    # Konwersja do formatu wykresu
    grouped_data = defaultdict(lambda: defaultdict(int))
    for row in results:
        time_of_day = row.time_of_day
        collision_type = row.collision_type
        count = row.count
        grouped_data[time_of_day][collision_type] = count

    # Zabezpieczone kategorie por dnia w ustalonej kolejności
    all_times = ["Noc", "Rano", "Dzień", "Wieczór"]
    all_types = sorted({row.collision_type for row in results})

    data = []
    for time in all_times:
        entry = {"time": time}
        for ctype in all_types:
            entry[ctype] = grouped_data[time].get(ctype, 0)
        data.append(entry)

    return {"data": data, "types": all_types}