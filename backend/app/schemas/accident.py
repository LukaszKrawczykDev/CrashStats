from pydantic import BaseModel, constr
from typing import Optional

class AccidentIn(BaseModel):
    collision_type: str
    injury_type: str
    primary_factor: str
    date_id: int
    location_id: int

class AccidentOut(AccidentIn):
    id: int

    class Config:
        orm_mode = True