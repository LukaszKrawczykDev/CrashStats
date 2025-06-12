import csv
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database import Base
from app.models.location import Location
from app.models.accident import Accident
from app.models.date import Date

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
session = Session(bind=engine)

CSV_PATH = "app/data/accidents.csv"


def main() -> None:
    raw_handle = open(CSV_PATH, "rb")
    decoded_iter = (line.decode("utf-8", errors="replace") for line in raw_handle)
    reader = csv.DictReader(decoded_iter, skipinitialspace=True)

    for row in reader:
        if row["Weekend?"].strip().lower() == "weekend":
            is_weekend = True
        else:
            is_weekend = False
        hour = int(row["Hour"].zfill(4)[:2])

        year = int(row["Year"])
        month = int(row["Month"])
        day = int(row["Day"])

        date_obj = (
            session.query(Date)
            .filter_by(
                year=year,
                month=month,
                day=day,
                hour=hour,
                is_weekend=is_weekend,
            )
            .first()
        )
        if not date_obj:
            date_obj = Date(
                year=year,
                month=month,
                day=day,
                hour=hour,
                is_weekend=is_weekend,
            )
            session.add(date_obj)
            session.flush()

        parts = [p.strip() for p in row["Reported_Location"].split("&")]
        street1 = parts[0]
        street2 = parts[1] if len(parts) > 1 else None

        lat_raw = row["Latitude"].strip()
        lon_raw = row["Longitude"].strip()
        if not lat_raw or not lon_raw:
            print(f"Skipping row without coordinates: {row['Reported_Location']}")
            continue

        lat = float(lat_raw)
        lon = float(lon_raw)

        loc_obj = (
            session.query(Location)
            .filter_by(
                street1=street1,
                street2=street2,
                latitude=lat,
                longitude=lon,
            )
            .first()
        )
        if not loc_obj:
            loc_obj = Location(
                street1=street1,
                street2=street2,
                latitude=lat,
                longitude=lon,
            )
            session.add(loc_obj)
            session.flush()

        acc = Accident(
            collision_type=row["Collision Type"],
            injury_type=row["Injury Type"],
            primary_factor=row["Primary Factor"],
            date_id=date_obj.id,
            location_id=loc_obj.id,
        )
        session.add(acc)

    session.commit()
    print("Import completed.")


if __name__ == "__main__":
    main()