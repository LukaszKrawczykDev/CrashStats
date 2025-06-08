from pydantic import BaseModel

class ExportSchema(BaseModel):
    id: int
    collision_type: str
    injury_type: str
    primary_factor: str
    date: str
    hour: int
    is_weekend: bool
    street: str
    latitude: float
    longitude: float
    weather: dict

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        date_str = f"{obj.date.year}-{obj.date.month}-{obj.date.day}"
        street_str = f"{obj.location.street1} & {obj.location.street2 or ''}".strip('& ')
        weather_dict = {
            "temperature": obj.date.weathers[0].temperature,
            "rain_1h": obj.date.weathers[0].rain_1h,
            "snow_1h": obj.date.weathers[0].snow_1h,
            "rain_24h": obj.date.weathers[0].rain_24h,
            "snow_24h": obj.date.weathers[0].snow_24h,
            "wind_speed": obj.date.weathers[0].wind_speed,
            "wind_deg": obj.date.weathers[0].wind_deg,
            "clouds":   obj.date.weathers[0].clouds,
            "description": obj.date.weathers[0].description,
            "category": obj.date.weathers[0].category,
            "road_condition": obj.date.weathers[0].road_condition
        }

        return cls(
            id=obj.id,
            collision_type=obj.collision_type,
            injury_type=obj.injury_type,
            primary_factor=obj.primary_factor,
            date=date_str,
            hour=obj.date.hour,
            is_weekend=obj.date.is_weekend,
            street=street_str,
            latitude=obj.location.latitude,
            longitude=obj.location.longitude,
            weather=weather_dict
        )