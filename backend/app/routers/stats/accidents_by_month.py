from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from app.database import SessionLocal
from app.models.accident import Accident
from app.models.date import Date
from app.models.weather import Weather  # potrzebne do filtrów pogodowych

router = APIRouter(prefix="/stats", tags=["stats"])

season_to_months = {
    "Wiosna": [3, 4, 5],
    "Lato": [6, 7, 8],
    "Jesień": [9, 10, 11],
    "Zima": [12, 1, 2],
}

@router.post("/accidents-by-month")
async def accidents_by_month(request: Request):
    filters = await request.json()
    print("filters:", filters)

    db: Session = SessionLocal()

    # Wyciągamy filtry
    year_month_pairs = []
    if filters and "years" in filters:
        for year_str, seasons in filters["years"].items():
            year = int(year_str)
            months = []
            for season in seasons:
                months.extend(season_to_months.get(season, []))
            for month in months:
                year_month_pairs.append((year, month))

    base_query = db.query(Date.year, Date.month, Weather.road_condition, func.count().label("count")) \
        .join(Accident, Accident.date_id == Date.id) \
        .join(Weather, and_(
        Weather.date_id == Date.id,
        Weather.location_id == Accident.location_id
    ))

    if year_month_pairs:
        base_query = base_query.filter(or_(*[
            and_(Date.year == y, Date.month == m) for y, m in year_month_pairs
        ]))

    base_query = base_query.group_by(Date.year, Date.month, Weather.road_condition)
    results = base_query.all()
    db.close()

    # Normalizacja wyników do struktury { (year, month): {rc: count} }
    data_map = {}
    for year, month, rc, count in results:
        key = (year, month)
        if key not in data_map:
            data_map[key] = {}
        data_map[key][rc] = count

    # Uzupełnienie zerami brakujących stanów
    all_conds = ["snowy", "icy", "wet", "dry"]
    final = []
    for year, month in sorted(data_map.keys()):
        breakdown = {cond: data_map[(year, month)].get(cond, 0) for cond in all_conds}
        final.append({
            "year": year,
            "month": month,
            "breakdown": breakdown
        })

    return final