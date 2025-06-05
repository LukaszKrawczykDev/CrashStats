#routers/data_export.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_
from datetime import datetime
import io, json, yaml
from dicttoxml import dicttoxml

from app.database import SessionLocal
from app.auth import get_current_user
from app.models.accident import Accident
from app.models.date import Date
from app.models.location import Location
from app.models.weather import Weather
from app.schemas.export import ExportRequest

router = APIRouter()

PREDEFINED_VALUES = {
    "injury_type": ["Fatal", "Non-incapacitating", "No injury/unknown", "Incapacitating"],
    "primary_factor": [
        "OTHER (ENVIRONMENTAL) - EXPLAIN IN NARR", "TIRE FAILURE OR DEFECTIVE", "ANIMAL/OBJECT IN ROADWAY",
        "DRIVER ASLEEP OR FATIGUED", "OVERCORRECTING/OVERSTEERING", "IMPROPER TURNING",
        "ENGINE FAILURE OR DEFECTIVE", "DRIVER DISTRACTED - EXPLAIN IN NARRATIVE",
        "OTHER (DRIVER) - EXPLAIN IN NARRATIVE", "OVERSIZE/OVERWEIGHT LOAD",
        "UNSAFE LANE MOVEMENT", "FAILURE TO YIELD RIGHT OF WAY", "ROADWAY SURFACE CONDITION",
        "RAN OFF ROAD RIGHT", "PEDESTRIAN ACTION", "INSECURE/LEAKY LOAD", "OTHER (VEHICLE) - EXPLAIN IN NARRATIVE",
        "CELL PHONE USAGE", "HOLES/RUTS IN SURFACE", "ACCELERATOR FAILURE OR DEFECTIVE",
        "FOLLOWING TOO CLOSELY", "OBSTRUCTION NOT MARKED", "OTHER LIGHTS DEFECTIVE",
        "SPEED TOO FAST FOR WEATHER CONDITIONS", "DISREGARD SIGNAL/REG SIGN", "WRONG WAY ON ONE WAY",
        "BRAKE FAILURE OR DEFECTIVE", "HEADLIGHT DEFECTIVE OR NOT ON", "STEERING FAILURE",
        "UNSAFE BACKING", "TOW HITCH FAILURE", "DRIVER ILLNESS", "IMPROPER LANE USAGE",
        "VIEW OBSTRUCTED", "IMPROPER PASSING", "TRAFFIC CONTROL INOPERATIVE/MISSING/OBSC",
        "LEFT OF CENTER", "OTHER TELEMATICS IN USE", "UNSAFE SPEED"
    ],
    "description": ["light rain", "moderate rain", "snow", "overcast", "partly cloudy", "heavy rain", "clear sky"],
    "road_condition": ["snowy", "icy", "wet", "dry"]
}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def is_other(value: str, field: str) -> bool:
    return value == "Other" or value not in PREDEFINED_VALUES.get(field, [])


@router.post("/export")
@router.post("/export/preview")
def export_data(
        req: ExportRequest,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    acc = aliased(Accident)
    dat = aliased(Date)
    loc = aliased(Location)
    wea = aliased(Weather)

    q = db.query(acc, dat, loc, wea) \
        .select_from(acc) \
        .join(dat, acc.date_id == dat.id) \
        .join(loc, acc.location_id == loc.id) \
        .join(wea, (dat.id == wea.date_id) & (loc.id == wea.location_id))

    for field, selected in req.filters.items():
        if not selected:
            continue

        col = None
        if hasattr(acc, field): col = getattr(acc, field)
        elif hasattr(dat, field): col = getattr(dat, field)
        elif hasattr(loc, field): col = getattr(loc, field)
        elif hasattr(wea, field): col = getattr(wea, field)
        if not col:
            continue

        normal = [v for v in selected if not is_other(v, field)]
        conditions = []
        if normal:
            conditions.append(col.in_(normal))
        if any(is_other(v, field) for v in selected):
            conditions.append(~col.in_(PREDEFINED_VALUES.get(field, [])))
        q = q.filter(or_(*conditions))

    if req.limit:
        q = q.limit(req.limit)

    rows = []
    for a, d, l, w in q.all():
        data = {}
        for col in req.columns:
            for src in [a, d, l, w]:
                if hasattr(src, col):
                    data[col] = getattr(src, col)
                    break
        rows.append(data)

    # Preview mode (JSON for frontend)
    if req.limit:
        return {"rows": rows}

    # Export file
    filename = f"export_{datetime.utcnow():%Y%m%d_%H%M%S}.{req.format}"
    media_type = "application/octet-stream"

    if req.format == "json":
        content = json.dumps(rows, ensure_ascii=False).encode()
        media_type = "application/json"
    elif req.format == "yaml":
        content = yaml.safe_dump(rows, allow_unicode=True).encode()
        media_type = "application/x-yaml"
    elif req.format == "xml":
        content = dicttoxml(rows, custom_root="rows", attr_type=False)
        media_type = "application/xml"
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

    return StreamingResponse(
        io.BytesIO(content),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )