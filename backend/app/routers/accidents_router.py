from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import get_current_user
from app.models.accident import Accident
from app.schemas.accident import AccidentIn, AccidentOut
from typing import List, Optional

router = APIRouter(prefix="/accidents", tags=["accidents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- GET all (with filters) -----------
@router.get("/", response_model=List[AccidentOut])
def list_accidents(
        year: Optional[int] = Query(None),
        injury: Optional[str] = Query(None),
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    query = db.query(Accident)

    if year:
        query = query.join(Accident.date).filter_by(year=year)
    if injury:
        query = query.filter(Accident.injury_type.ilike(f"%{injury}%"))

    return query.all()

# ----------- GET by ID -----------
@router.get("/{accident_id}", response_model=AccidentOut)
def get_accident(accident_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    acc = db.query(Accident).get(accident_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Nie znaleziono")
    return acc

# ----------- POST (add) – admin only -----------
@router.post("/", status_code=201, response_model=AccidentOut)
def create_accident(
        data: AccidentIn,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Tylko administrator może dodawać dane")

    acc = Accident(**data.dict())
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return acc

# ----------- DELETE – admin only -----------
@router.delete("/{accident_id}", status_code=204)
def delete_accident(
        accident_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Tylko administrator może usuwać dane")

    acc = db.query(Accident).get(accident_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Nie znaleziono")

    db.delete(acc)
    db.commit()