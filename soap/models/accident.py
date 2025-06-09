from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Accident(Base):
    __tablename__ = "accidents"
    id             = Column(Integer, primary_key=True, index=True)
    date_id        = Column(Integer, ForeignKey("dates.id"), nullable=False)
    location_id    = Column(Integer, ForeignKey("locations.id"), nullable=False)
    collision_type = Column(String)
    primary_factor = Column(String)