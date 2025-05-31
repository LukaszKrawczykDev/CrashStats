from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship
from app.database import Base

class Location(Base):
    __tablename__ = "locations"

    id        = Column(Integer, primary_key=True, index=True)
    street1   = Column(String, nullable=False)
    street2   = Column(String, nullable=True)
    latitude  = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    accidents = relationship("Accident", back_populates="location")
    weathers  = relationship("Weather",  back_populates="location")