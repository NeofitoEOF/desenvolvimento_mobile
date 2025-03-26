from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/parkings/", response_model=schemas.Parking)
def create_parking(parking: schemas.ParkingCreate, db: Session = Depends(get_db)):
    """
    Registra a entrada de um veículo no estacionamento.
    """
    existing_parking = crud.get_parking_by_license_plate(db, license_plate=parking.license_plate)
    if existing_parking:
        raise HTTPException(status_code=400, detail="Veículo já está estacionado")
    return crud.create_parking(db=db, parking=parking)

@router.get("/parkings/{parking_id}", response_model=schemas.Parking)
def read_parking(parking_id: int, db: Session = Depends(get_db)):
    """
    Retorna informações de um veículo específico no estacionamento.
    """
    db_parking = crud.get_parking(db, parking_id=parking_id)
    if db_parking is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return db_parking

@router.get("/parkings/", response_model=list[schemas.Parking])
def read_parkings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todos os veículos no estacionamento.
    """
    parkings = crud.get_parkings(db, skip=skip, limit=limit)
    return parkings

@router.patch("/parkings/{parking_id}", response_model=schemas.Parking)
def update_parking(parking_id: int, parking: schemas.ParkingUpdate, db: Session = Depends(get_db)):
    """
    Atualiza as informações de um veículo no estacionamento (saída, taxa).
    """
    existing_parking = crud.get_parking(db, parking_id=parking_id)
    if not existing_parking:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    if parking.exit_time and not parking.fee:
        entry_time = existing_parking.entry_time
        exit_time = parking.exit_time
        duration = exit_time - entry_time

        fee = (duration.total_seconds() / 3600) * 10
        parking.fee = round(fee, 2)  

    updated_parking = crud.update_parking(db, parking_id, parking)
    if not updated_parking:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return updated_parking


@router.delete("/parkings/{parking_id}", response_model=bool)
def delete_parking(parking_id: int, db: Session = Depends(get_db)):
    """
    Remove um veículo do estacionamento.
    """
    if not crud.delete_parking(db, parking_id):
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return True