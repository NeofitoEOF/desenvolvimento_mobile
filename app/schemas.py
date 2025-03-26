from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ParkingBase(BaseModel):
    parking_type: str
    license_plate: str

class ParkingCreate(ParkingBase):
    pass

class ParkingUpdate(BaseModel):
    exit_time: Optional[datetime] = None
    fee: Optional[float] = None
    is_parked: Optional[bool] = False

class Parking(ParkingBase):
    id: int
    entry_time: datetime
    exit_time: Optional[datetime]
    is_parked: bool
    fee: Optional[float]

    class Config:
        orm_mode = True