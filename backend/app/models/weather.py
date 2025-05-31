from sqlalchemy import Column, Integer, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Weather(Base):
    __tablename__ = "weather"
    __table_args__ = (UniqueConstraint("date_id", "location_id", name="uix_date_loc"),)

    id          = Column(Integer, primary_key=True, index=True)
    date_id     = Column(Integer, ForeignKey("dates.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    temperature = Column(Float)
    rain_1h     = Column(Float, nullable=True)
    snow_1h     = Column(Float, nullable=True)
    rain_24h    = Column(Float, nullable=True)
    snow_24h    = Column(Float, nullable=True)

    wind_speed  = Column(Float)
    wind_deg    = Column(Integer)
    clouds      = Column(Integer)

    description    = Column(String)
    category       = Column(String)
    road_condition = Column(String)

    date     = relationship("Date", back_populates="weathers")
    location = relationship("Location", back_populates="weathers")