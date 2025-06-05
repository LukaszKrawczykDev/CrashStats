from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from collections import defaultdict
from app.models import Accident, Date, Weather

router = APIRouter()

@router.post("/stats/user-weather-chart")
async def user_weather_chart(request: Request):
    body = await request.json()
    collision_types = body.get("collision_types", [])

    print("📥 Request received:", collision_types)

    db: Session = SessionLocal()

    results = db.query(
        Date.hour,
        Weather.category,
        Accident.collision_type,
    ).join(Date, Date.id == Accident.date_id) \
        .join(Weather, (Weather.date_id == Date.id) & (Weather.location_id == Accident.location_id)) \
        .filter(Accident.collision_type.in_(collision_types)) \
        .all()

    print(f"📊 Fetched {len(results)} rows.")

    def classify_hour(hour: int) -> str:
        if 22 <= hour or hour < 6:
            return "Noc"
        elif 6 <= hour < 12:
            return "Rano"
        elif 12 <= hour < 18:
            return "Dzień"
        else:
            return "Wieczór"

    grouped = defaultdict(lambda: defaultdict(int))
    for hour, weather, ctype in results:
        time = classify_hour(hour)
        label = f"{time} / {weather or 'Brak danych'}"
        grouped[label][ctype] += 1

    response_data = []
    all_types = set(collision_types)
    for label, counts in grouped.items():
        row = {"label": label}
        for ctype in all_types:
            row[ctype] = counts.get(ctype, 0)
        response_data.append(row)

    print("✅ Final data:", response_data[:3], "...")

    return {
        "data": response_data,
        "types": list(all_types)
    }