from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET
import json
import yaml
from datetime import datetime, timezone

from app.database import get_db
from app.auth import get_current_admin
from app.models.date import Date
from app.models.location import Location
from app.models.accident import Accident
from app.models.weather import Weather
from app.utils.weather import (
    fetch_weather_block,
    build_description,
    build_category,
    road_condition,
)

router = APIRouter()

@router.post("/api/import")
async def import_data(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        admin = Depends(get_current_admin),
):
    text = (await file.read()).decode("utf-8")
    ext = file.filename.rsplit(".", 1)[-1].lower()

    db.connection(
        execution_options={"isolation_level": "SERIALIZABLE"}
    )

    try:
        if ext == "json":
            records = json.loads(text)
        elif ext in ("yml", "yaml"):
            records = yaml.safe_load(text)
        elif ext == "xml":
            root = ET.fromstring(text)
            records = [
                {child.tag: child.text for child in col}
                for col in root.findall(".//Collision")
            ]
        else:
            raise ValueError(f"Unsupported format: {ext}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parse error: {e}")

    results = []

    try:


        for idx, rec in enumerate(records, start=1):
            row_res = {"row": idx}

            try:
                year = int(rec["Year"])
                month = int(rec["Month"])
                day = int(rec["Day"])
                hour = int(rec["Hour"])
                is_weekend = rec.get("Weekend", "").strip().lower() == "weekend"
                ctype = rec["Collision_Type"]
                intype = rec["Injury_Type"]
                factor = rec["Primary_Factor"]
                place = rec["Reported_Location"]
                lat = float(rec["Latitude"])
                lon = float(rec["Longitude"])

                date = (
                        db.query(Date)
                        .filter_by(year=year, month=month, day=day, hour=hour, is_weekend=is_weekend)
                        .first()
                        or Date(year=year, month=month, day=day, hour=hour, is_weekend=is_weekend)
                )
                db.add(date); db.flush(); db.refresh(date)

                if "&" in place:
                    street1, street2 = [p.strip() for p in place.split("&", 1)]
                else:
                    street1, street2 = place.strip(), None

                loc = (
                        db.query(Location)
                        .filter_by(street1=street1, street2=street2, latitude=lat, longitude=lon)
                        .first()
                        or Location(street1=street1, street2=street2, latitude=lat, longitude=lon)
                )
                db.add(loc); db.flush(); db.refresh(loc)

                acc = Accident(
                    date_id=date.id,
                    location_id=loc.id,
                    collision_type=ctype,
                    injury_type=intype,
                    primary_factor=factor,
                )
                db.add(acc); db.flush(); db.refresh(acc)

                try:
                    ts = datetime(year, month, day, hour, tzinfo=timezone.utc)
                    block = fetch_weather_block(lat, lon, ts)
                    hr = block["hourly"]
                    ih = ts.hour

                    temp = round(hr["temperature_2m"][ih], 2)
                    rain1 = round(hr.get("precipitation", [0.0]*24)[ih], 2)
                    snow1 = round(hr.get("snowfall", [0.0]*24)[ih], 2)
                    cloud = round(hr.get("cloudcover", [0.0]*24)[ih], 2)
                    wsp = round(hr.get("wind_speed_10m", [0.0]*24)[ih] / 3.6, 2)
                    wdeg = int(hr.get("wind_direction_10m", [0.0]*24)[ih])
                    rain24 = round(sum(hr.get("precipitation", [0.0]*24)), 2)
                    snow24 = round(sum(hr.get("snowfall", [0.0]*24)), 2)

                    w = Weather(
                        date_id=date.id,
                        location_id=loc.id,
                        temperature=temp,
                        rain_1h=rain1,
                        snow_1h=snow1,
                        rain_24h=rain24,
                        snow_24h=snow24,
                        wind_speed=wsp,
                        wind_deg=wdeg,
                        clouds=cloud,
                        description=build_description(rain1, snow1, cloud),
                        category=build_category(rain1, snow1, cloud),
                        road_condition=road_condition(temp, rain24, snow24),
                    )
                    db.add(w); db.flush()

                    row_res.update({"status": "success"})
                except Exception as e:
                    row_res.update({
                        "status": "warning",
                        "error": f"Weather fetch failed: {e}"
                    })

            except Exception as e:
                row_res.update({
                    "status": "error",
                    "error": f"DB/parsing error: {e}"
                })

            results.append(row_res)

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {e}")

    return results