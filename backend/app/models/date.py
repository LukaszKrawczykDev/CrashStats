from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Date(Base):
    __tablename__ = "dates"

    id         = Column(Integer, primary_key=True, index=True)
    year       = Column(Integer,  nullable=False)
    month      = Column(Integer,  nullable=False)
    day        = Column(Integer,  nullable=False)
    hour       = Column(Integer,  nullable=False)   # 0-23
    is_weekend = Column(Boolean,  nullable=False)   # True = weekend

    accidents = relationship("Accident", back_populates="date")
    weathers  = relationship("Weather",  back_populates="date")