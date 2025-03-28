import logging
from typing import List
from venv import logger
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
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