from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Accident(Base):
    __tablename__ = "accidents"

    id             = Column(Integer, primary_key=True, index=True)
    collision_type = Column(String)
    injury_type    = Column(String)
    primary_factor = Column(String)

    date_id     = Column(Integer, ForeignKey("dates.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    date     = relationship("Date", back_populates="accidents")
    location = relationship("Location", back_populates="accidents")