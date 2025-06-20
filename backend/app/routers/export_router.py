from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.accident import Accident
from app.models.date import Date
from app.schemas.export import ExportSchema
from fastapi.responses import Response
import yaml, dicttoxml, json

router = APIRouter(prefix="/export", tags=["export"])

@router.get("/years")
def get_years(db: Session = Depends(get_db)):
    years = db.query(Date.year).distinct().order_by(Date.year).all()
    return {"years": [y[0] for y in years]}

@router.get("/data")
def export_data(
        years: list[int] = Query(None),
        format: str = Query("json", regex="^(json|yaml|xml)$"),
        preview: bool = Query(False, description="Czy tylko podgląd (limit 10)"),
        db: Session = Depends(get_db),
):
    try:
        db.connection(
            execution_options={"isolation_level": "REPEATABLE READ"}
        )
        db.begin_nested()
        query = (
            db.query(Accident)
            .options(
                joinedload(Accident.date).joinedload(Date.weathers),
                joinedload(Accident.location)
            )
            .join(Accident.date)
        )
        if years:
            query = query.filter(Date.year.in_(years))
        query = query.order_by(Accident.id)
        if preview:
            query = query.limit(10)
        records = query.all()
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd eksportu danych: {str(e)}")

    export_list = [ExportSchema.from_orm(r).dict() for r in records]

    if format == "json":
        content = json.dumps(export_list, indent=2, ensure_ascii=False)
        media_type = "application/json"
    elif format == "yaml":
        content = yaml.dump(export_list, sort_keys=False, allow_unicode=True)
        media_type = "application/x-yaml"
    else:  # xml
        content = dicttoxml.dicttoxml(export_list, custom_root="records", attr_type=False)
        media_type = "application/xml"

    headers = {}
    if not preview:
        headers["Content-Disposition"] = f'attachment; filename="export.{format}"'

    return Response(content=content, media_type=media_type, headers=headers)