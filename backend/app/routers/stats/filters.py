# backend/app/routers/stats/filters.py
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.date import Date

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/filters/meta")
def get_filters_meta():
    db: Session = SessionLocal()
    results = db.query(Date.year, Date.month).distinct().all()
    db.close()

    years = {}
    for year, month in results:
        years.setdefault(year, set()).add(month)

    return {str(year): sorted(list(months)) for year, months in years.items()}