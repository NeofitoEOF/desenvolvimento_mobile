from http.client import HTTPException

from requests import Session

from app.models import models
from datetime import datetime

from app.schemas import schemas

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    from app.auth.auth import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_parking(db: Session, parking: schemas.ParkingRecordCreate):
    existing_parking = get_parking_by_license_plate(db, license_plate=parking.license_plate)
    if existing_parking:
        raise ValueError("Veículo já está estacionado")

    parking_type = db.query(models.ParkingType).filter(
        models.ParkingType.id == parking.parking_type_id
    ).first()
    
    if not parking_type:
        raise ValueError("Tipo de estacionamento não encontrado")
    
    if parking_type.occupied_spaces >= parking_type.capacity:
        raise ValueError("Estacionamento lotado")

    db_parking = models.ParkingRecord(**parking.dict())
    db.add(db_parking)
    
    parking_type.occupied_spaces += 1
    parking_type.capacity -= 1
    
    db.commit()
    db.refresh(db_parking)
    return db_parking

def get_parking_types(db: Session, skip: int = 0, limit: int = 100):
    parking_types = db.query(models.ParkingType).offset(skip).limit(limit).all()
    
    for pt in parking_types:
        parked_count = db.query(models.ParkingRecord).filter(
            models.ParkingRecord.parking_type_id == pt.id,
            models.ParkingRecord.is_parked == True
        ).count()
        setattr(pt, 'available_spaces', pt.capacity - parked_count)
    
    return parking_types


def get_parking_by_license_plate(db: Session, license_plate: str):
    return db.query(models.ParkingRecord).filter(models.ParkingRecord.license_plate == license_plate).filter(models.ParkingRecord.is_parked == True).first()


def update_parking(db: Session, parking_id: int, parking: schemas.ParkingRecordUpdate):
    db_parking = db.query(models.ParkingRecord).filter(
        models.ParkingRecord.id == parking_id
    ).first()
    
    if not db_parking:
        return None

    if parking.is_parked is False and db_parking.is_parked is True:
        parking_type = db_parking.parking_type
        parking_type.occupied_spaces -= 1

    for var, value in vars(parking).items():
        if value is not None:
            setattr(db_parking, var, value)
    
    db.commit()
    db.refresh(db_parking)
    return db_parking

def get_parked_vehicles_by_plate(db: Session, license_plate: str, skip: int = 0, limit: int = 100):
    return db.query(models.ParkingRecord).filter(
        models.ParkingRecord.license_plate.ilike(f"%{license_plate}%"),
        models.ParkingRecord.is_parked == True
    ).order_by(models.ParkingRecord.entry_time.desc()).offset(skip).limit(limit).all()



def delete_parked_vehicles_by_plate(db: Session, license_plate: str):
    parked_vehicle = db.query(models.ParkingRecord).filter(
        models.ParkingRecord.license_plate == license_plate, 
        models.ParkingRecord.is_parked == True
    ).first()
    
    if not parked_vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado ou já removido")
    
    parking_type = db.query(models.ParkingType).filter(
        models.ParkingType.id == parked_vehicle.parking_type_id
    ).first()
    
    if parking_type:
        parking_type.occupied_spaces -= 1
        parking_type.capacity += 1
    
    db.delete(parked_vehicle)
    db.commit()
    
    return {"message": f"Veículo {license_plate} removido e vaga liberada com sucesso"}