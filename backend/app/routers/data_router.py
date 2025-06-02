from fastapi import APIRouter, Query, Depends, HTTPException, Response, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.database import SessionLocal
from app.models.accident import Accident
from app.models.date import Date
from app.models.location import Location
from app.models.weather import Weather
from app.auth import get_current_user
import json
import yaml
import xml.etree.ElementTree as ET
from io import BytesIO

router = APIRouter(prefix="/data", tags=["data"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/export/{format}")
def export_data(
        format: str,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),  # user or admin can export
        columns: Optional[List[str]] = Query(None),
        include: Optional[List[str]] = Query([]),
        year: Optional[int] = Query(None),
        injury_type: Optional[str] = Query(None),
        primary_factor: Optional[str] = Query(None),
):
    if format not in ("json", "yaml", "xml"):
        raise HTTPException(status_code=400, detail="Invalid format")

    query = db.query(Accident).options(
        joinedload(Accident.date),
        joinedload(Accident.location),
        joinedload(Accident.date).joinedload(Date.weathers),
    )

    if year:
        query = query.join(Accident.date).filter(Date.year == year)
    if injury_type:
        query = query.filter(Accident.injury_type.ilike(f"%{injury_type}%"))
    if primary_factor:
        query = query.filter(Accident.primary_factor.ilike(f"%{primary_factor}%"))

    records = query.all()
    result = []

    for accident in records:
        row = {}

        # Core accident fields
        accident_dict = accident.__dict__
        if columns:
            for col in columns:
                if col in accident_dict:
                    row[col] = accident_dict[col]
        else:
            for k, v in accident_dict.items():
                if not k.startswith("_") and k not in ("date", "location"):
                    row[k] = v

        # Include related models
        if "date" in include:
            row["date"] = {
                k: v for k, v in accident.date.__dict__.items() if not k.startswith("_")
            }

        if "location" in include:
            row["location"] = {
                k: v for k, v in accident.location.__dict__.items() if not k.startswith("_")
            }

        if "weather" in include:
            weather = None
            for w in accident.date.weathers:
                if w.location_id == accident.location_id:
                    weather = w
                    break
            if weather:
                row["weather"] = {
                    k: v for k, v in weather.__dict__.items() if not k.startswith("_")
                }

        result.append(row)

    if format == "json":
        return Response(content=json.dumps(result, indent=2), media_type="application/json")

    elif format == "yaml":
        return Response(content=yaml.dump(result, allow_unicode=True), media_type="application/x-yaml")

    elif format == "xml":
        root = ET.Element("accidents")
        for item in result:
            acc_elem = ET.SubElement(root, "accident")
            for key, value in item.items():
                if isinstance(value, dict):
                    sub_elem = ET.SubElement(acc_elem, key)
                    for sub_key, sub_val in value.items():
                        ET.SubElement(sub_elem, sub_key).text = str(sub_val)
                else:
                    ET.SubElement(acc_elem, key).text = str(value)

        tree = ET.ElementTree(root)
        buffer = BytesIO()
        tree.write(buffer, encoding="utf-8", xml_declaration=True)
        return Response(content=buffer.getvalue(), media_type="application/xml")


@router.post("/import/{format}")
def import_data(
        format: str,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)  # only admin can import
):
    if not current_user.get("role") == "admin":
        raise HTTPException(status_code=403, detail="Tylko administrator może importować dane")

    if format not in ("json", "yaml", "xml"):
        raise HTTPException(status_code=400, detail="Nieobsługiwany format pliku")

    contents = file.file.read()

    try:
        if format == "json":
            records = json.loads(contents)
        elif format == "yaml":
            records = yaml.safe_load(contents)
        elif format == "xml":
            tree = ET.ElementTree(ET.fromstring(contents))
            root = tree.getroot()
            records = []
            for elem in root.findall("accident"):
                item = {}
                for child in elem:
                    if list(child):
                        item[child.tag] = {g.tag: g.text for g in child}
                    else:
                        item[child.tag] = child.text
                records.append(item)
        else:
            raise ValueError("Nieobsługiwany format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd parsowania danych: {str(e)}")

    # Przykładowy import tylko accident + date + location
    for record in records:
        # Date
        d = record.get("date", {})
        date_obj = Date(
            year=int(d.get("year", 2000)),
            month=int(d.get("month", 1)),
            day=int(d.get("day", 1)),
            hour=int(d.get("hour", 0)),
            is_weekend=d.get("is_weekend", "false") in ["True", "true", True]
        )
        db.add(date_obj)
        db.flush()

        # Location
        l = record.get("location", {})
        location_obj = Location(
            street1=l.get("street1", "UNKNOWN"),
            street2=l.get("street2"),
            latitude=float(l.get("latitude", 0)),
            longitude=float(l.get("longitude", 0))
        )
        db.add(location_obj)
        db.flush()

        # Accident
        acc = Accident(
            collision_type=record.get("collision_type", "unknown"),
            injury_type=record.get("injury_type", "unknown"),
            primary_factor=record.get("primary_factor", "unknown"),
            date_id=date_obj.id,
            location_id=location_obj.id
        )
        db.add(acc)

    db.commit()
    return {"msg": f"Zaimportowano {len(records)} rekordów"}