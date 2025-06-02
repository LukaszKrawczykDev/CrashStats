from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.accident import Accident
from app.models.date import Date
from sqlalchemy import func

router = APIRouter()

MONTH_NAMES = [
    "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
    "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
]

SEASONS = {
    "Zima": [12, 1, 2],
    "Wiosna": [3, 4, 5],
    "Lato": [6, 7, 8],
    "Jesień": [9, 10, 11]
}

@router.get("/accidents/monthly")
def get_accidents_by_month(
        years: str = Query(""),
        seasons: str = Query(""),
        db: Session = Depends(get_db)
):
    # Przygotowanie filtrów
    years_list = [int(y) for y in years.split(",") if y]
    selected_seasons = [s for s in seasons.split(",") if s]
    selected_months = [m for season in selected_seasons for m in SEASONS.get(season, [])]

    # Query: Dołącz tabelę Date
    query = db.query(Date.month, func.count(Accident.id)) \
        .join(Accident, Accident.date_id == Date.id)

    if years_list:
        query = query.filter(Date.year.in_(years_list))
    if selected_months:
        query = query.filter(Date.month.in_(selected_months))

    query = query.group_by(Date.month).order_by(Date.month)

    result = query.all()

    # Zbuduj pełne dane z zerami dla braku miesiąca
    month_count_map = {month: 0 for month in range(1, 13)}
    for month, count in result:
        month_count_map[month] = count

    return [
        {"month": MONTH_NAMES[i - 1], "count": month_count_map[i]}
        for i in range(1, 13)
    ]