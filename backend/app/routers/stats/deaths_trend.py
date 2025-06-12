from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.accident import Accident
from app.models.date import Date
from sqlalchemy import and_, func
from collections import defaultdict

router = APIRouter()

season_to_months = {
    "Wiosna": [3, 4, 5],
    "Lato": [6, 7, 8],
    "Jesień": [9, 10, 11],
    "Zima": [12, 1, 2],
}

@router.post("/stats/deaths-trend")
async def deaths_trend(request: Request):
    filters = await request.json()
    db: Session = SessionLocal()

    valid_types = ["Fatal", "Non-incapacitating", "No injury/unknown", "Incapacitating"]
    selected_year_months = set()

    if filters and "years" in filters:
        for year_str, seasons in filters["years"].items():
            year = int(year_str)
            months = []
            for s in seasons:
                months.extend(season_to_months.get(s, []))
            for m in months:
                selected_year_months.add((year, m))

    query = db.query(Date.year, Date.month, Accident.injury_type, func.count()) \
        .join(Accident)

    if selected_year_months:
        from sqlalchemy import or_
        filters_sql = [and_(Date.year == year, Date.month == month) for (year, month) in selected_year_months]
        query = query.filter(or_(*filters_sql))

    query = query.group_by(Date.year, Date.month, Accident.injury_type).order_by(Date.year, Date.month)
    results = query.all()
    db.close()

    data_map = defaultdict(lambda: defaultdict(int))
    labels = sorted(selected_year_months)

    for year, month, injury_type, count in results:
        label = f"{str(month).zfill(2)}.{year}"
        category = injury_type if injury_type in valid_types else "Other"
        data_map[label][category] += count

    final_data = []
    for year, month in labels:
        label = f"{str(month).zfill(2)}.{year}"
        row = {"label": label}
        for t in valid_types + ["Other"]:
            row[t] = data_map[label][t]
        final_data.append(row)

    return final_data