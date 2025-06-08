import os
import time
import json
import random
import requests
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database import SessionLocal
from app.models.date import Date
from app.models.location import Location
from app.models.accident import Accident
from app.models.weather import Weather

from tqdm import tqdm

OP_url = "https://archive-api.open-meteo.com/v1/archive"
PROGRESS_FILE = "weather_progress.json"
MAX_REQUESTS_PER_DAY = 10000
DEFAULT_LAT = 39.16144
DEFAULT_LON = -86.534848

def build_category(rain: float, snow: float, cloud: float) -> str:
    if snow > 0:
        return "snow"
    if rain > 0:
        return "rain"
    if cloud > 60:
        return "cloudy"
    return "clear"

def build_description(rain: float, snow: float, cloud: float) -> str:
    if snow > 0:
        return "snow"
    if rain > 2:
        return "heavy rain"
    if rain > 0.2:
        return "moderate rain"
    if rain > 0:
        return "light rain"
    if cloud > 70:
        return "overcast"
    if cloud > 30:
        return "partly cloudy"
    return "clear sky"

def road_condition(temp: float, rain24: float, snow24: float) -> str:
    if snow24 > 0:
        return "snowy"
    if rain24 > 0:
        return "icy" if temp <= 0 else "wet"
    return "dry"

def load_progress():
    try:
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_date_id": 0}

def save_progress(date_id):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"last_date_id": date_id}, f)


def fetch_weather_block(lat: float, lon: float, ts_utc: datetime, tries: int = 4) -> dict:
    date_str = ts_utc.strftime("%Y-%m-%d")
    url = (
        f"{OP_url}?latitude={lat}&longitude={lon}"
        f"&start_date={date_str}&end_date={date_str}"
        f"&hourly=temperature_2m,precipitation,cloudcover,snowfall,wind_speed_10m,wind_direction_10m"
        f"&timezone=UTC"
    )

    for attempt in range(1, tries + 1):
        try:
            print(f"🔍 URL: {url}")
            r = requests.get(url, timeout=30)
            if r.status_code == 429:
                raise RuntimeError("🛑 Przekroczono limit zapytań (429)")
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  {e.__class__.__name__} attempt {attempt}/{tries} – sleep {2*attempt:.1f}s")
            time.sleep(2 * attempt + random.uniform(0, 1))
    raise RuntimeError(f"Open-Meteo failed after {tries} tries for {lat},{lon} {date_str}")

def main() -> None:
    db: Session = SessionLocal()
    progress = load_progress()
    last_date_id = progress.get("last_date_id", 0)

    to_fetch = (
        db.query(Date, Location)
        .select_from(Accident)
        .join(Date, Accident.date_id == Date.id)
        .join(Location, Accident.location_id == Location.id)
        .outerjoin(Weather, (Weather.date_id == Date.id) & (Weather.location_id == Location.id))
        .filter(Weather.id == None)
        .filter(Date.id > last_date_id)
        .order_by(Date.id)
        .distinct()
        .all()
    )

    print("⏳ missing weather rows:", len(to_fetch))

    request_count = 0

    for date, loc in tqdm(to_fetch, desc="Pobieranie pogody", unit="rekord"):
        if request_count >= MAX_REQUESTS_PER_DAY:
            print("🚦 Limit dzienny 10000 zapytań osiągnięty. Zatrzymuję.")
            break

        lat = loc.latitude if loc.latitude != 0 else DEFAULT_LAT
        lon = loc.longitude if loc.longitude != 0 else DEFAULT_LON

        ts = datetime(date.year, date.month, date.day, date.hour, tzinfo=timezone.utc)

        try:
            data = fetch_weather_block(lat, lon, ts)
            request_count += 1
        except RuntimeError as err:
            print("❌", err, "– skipping")
            break

        try:
            hour_idx = ts.hour
            hourly = data["hourly"]
            temp = round(hourly["temperature_2m"][hour_idx], 2)
            rain = round(hourly.get("precipitation", [0.0]*24)[hour_idx], 2)
            snow = round(hourly.get("snowfall", [0.0]*24)[hour_idx], 2)
            cloud = round(hourly.get("cloudcover", [0.0]*24)[hour_idx], 2)
            wind_speed = round(hourly.get("wind_speed_10m", [0.0]*24)[hour_idx] / 3.6, 2)
            wind_deg = round(hourly.get("wind_direction_10m", [0.0]*24)[hour_idx], 2)
        except (KeyError, IndexError):
            print(f"⚠️ Brak danych godzinowych dla {ts}, pomijam")
            continue

        rain24 = round(sum(hourly.get("precipitation", [0.0]*24)), 2)
        snow24 = round(sum(hourly.get("snowfall", [0.0]*24)), 2)

        weather = Weather(
            date_id=date.id,
            location_id=loc.id,
            temperature=temp,
            rain_1h=rain,
            snow_1h=snow,
            rain_24h=rain24,
            snow_24h=snow24,
            wind_speed=wind_speed,
            wind_deg=wind_deg,
            clouds=cloud,
            description=build_description(rain, snow, cloud),
            category=build_category(rain, snow, cloud),
            road_condition=road_condition(temp, rain24, snow24),
        )

        db.add(weather)
        db.commit()
        save_progress(date.id)
        print(f"✓ saved weather for date {date.id} / loc {loc.id}")
        time.sleep(0.4)

if __name__ == "__main__":
    main()