import time
import random
import requests
from datetime import datetime, timezone

OP_URL = "https://archive-api.open-meteo.com/v1/archive"
MAX_TRIES = 4
DEFAULT_LAT = 39.16144
DEFAULT_LON = -86.534848

def fetch_weather_block(lat: float, lon: float, ts_utc: datetime, tries: int = MAX_TRIES) -> dict:
    date_str = ts_utc.strftime("%Y-%m-%d")
    url = (
        f"{OP_URL}?latitude={lat}&longitude={lon}"
        f"&start_date={date_str}&end_date={date_str}"
        f"&hourly=temperature_2m,precipitation,cloudcover,snowfall,wind_speed_10m,wind_direction_10m"
        f"&timezone=UTC"
    )
    for attempt in range(1, tries + 1):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 429:
                raise RuntimeError("Przekroczono limit zapytań (429)")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == tries:
                raise
            time.sleep(2 * attempt + random.random())

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