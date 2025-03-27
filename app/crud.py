from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

def create_parking(db: Session, parking: schemas.ParkingTypeBase):
    db_parking = models.Parking(**parking.dict())
    db.add(db_parking)
    db.commit()
    db.refresh(db_parking)
    return db_parking

def get_parking_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ParkingType).offset(skip).limit(limit).all()

def get_parking(db: Session, parking_id: int):
    return db.query(models.Parking).filter(models.Parking.id == parking_id).first()

def get_parkings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parking).offset(skip).limit(limit).all()

def get_parking_by_license_plate(db: Session, license_plate: str):
    return db.query(models.Parking).filter(models.Parking.license_plate == license_plate).filter(models.Parking.is_parked == True).first()

def update_parking(db: Session, parking_id: int, parking: schemas.ParkingRecordUpdate):
    db_parking = db.query(models.Parking).filter(models.Parking.id == parking_id).first()
    if db_parking:
        for var, value in vars(parking).items():
            if value is not None:
                setattr(db_parking, var, value)
        db.commit()
        db.refresh(db_parking)
    return db_parking

def delete_parking(db: Session, parking_id: int):
    db_parking = db.query(models.Parking).filter(models.Parking.id == parking_id).first()
    if db_parking:
        db.delete(db_parking)
        db.commit()
        return True
    return False