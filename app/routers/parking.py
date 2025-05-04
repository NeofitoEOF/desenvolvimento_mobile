from typing import List, Optional
from venv import logger

from requests import Session

from app import crud
from app.models import models
from app.schemas import schemas
from fastapi import APIRouter, Depends, HTTPException # type: ignore
from app.database.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/parkings/", response_model=schemas.ParkingRecord)
def create_parking(parking: schemas.ParkingRecordCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_parking(db=db, parking=parking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/parkingsTypes/", response_model=List[schemas.ParkingType])
def read_parking_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    parking_types = db.query(models.ParkingType).offset(skip).limit(limit).all()
    return parking_types

@router.get("/parkings/active/search/", response_model=List[schemas.ParkingRecord])
def search_parked_vehicles_by_plate(
    license_plate: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_parked_vehicles_by_plate(
        db,
        license_plate=license_plate,
        skip=skip,
        limit=limit
    )

@router.delete("/parkings/active/{license_plate}")
def delete_parked_vehicle(
    license_plate: str,
    db: Session = Depends(get_db)
):
    return crud.delete_parked_vehicles_by_plate(db, license_plate=license_plate)