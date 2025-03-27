from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ParkingTypeBase(BaseModel):
    name: str = Field(..., example="Aeroporto")
    capacity: int = Field(..., gt=0, example=20) 

class ParkingTypeCreate(ParkingTypeBase):
    pass 

class ParkingType(ParkingTypeBase): 
    id: int

    class Config:
        orm_mode = True


class ParkingRecordBase(BaseModel):
    license_plate: str = Field(..., example="BRA2E19")
    vehicle_year: Optional[int] = Field(None, example=2020)
    vehicle_color: Optional[str] = Field(None, example="Prata")
    parking_type_id: int = Field(..., example=1)

class ParkingRecordCreate(ParkingRecordBase):
    pass

class ParkingRecordUpdate(BaseModel):
    exit_time: Optional[datetime] = None
    fee: Optional[float] = None
    is_parked: Optional[bool] = False 

class ParkingRecord(ParkingRecordBase): 
    id: int
    entry_time: datetime
    exit_time: Optional[datetime]
    is_parked: bool
    fee: Optional[float]
    created_at: datetime
    updated_at: datetime
    parking_type: ParkingType 

    class Config:
        orm_mode = True