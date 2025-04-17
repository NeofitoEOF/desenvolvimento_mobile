from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    func 
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base 

Base = declarative_base() 

class ParkingType(Base):
    __tablename__ = "parking_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False) 
    occupied_spaces = Column(Integer, default=0, nullable=False)  

    parking_records = relationship("ParkingRecord", back_populates="parking_type")

    @property
    def available_spaces(self):
        return self.capacity - self.occupied_spaces

    def __repr__(self):
        return f"<ParkingType(id={self.id}, name='{self.name}', capacity={self.capacity}, occupied={self.occupied_spaces})>"


class ParkingRecord(Base):
    __tablename__ = "parking_records"
    id = Column(Integer, primary_key=True, index=True)
    parking_type_id = Column(Integer, ForeignKey("parking_types.id"), nullable=False)
    license_plate = Column(String, index=True, nullable=False)
    vehicle_year = Column(Integer, nullable=True) 
    vehicle_color = Column(String, nullable=True) 
    entry_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    exit_time = Column(DateTime(timezone=True), nullable=True)
    is_parked = Column(Boolean, default=True, nullable=False) 
    fee = Column(Float, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(), 
        nullable=False
    )
    parking_type = relationship("ParkingType", back_populates="parking_records")

    def __repr__(self):
        status = "Parked" if self.is_parked else "Exited"
        return (f"<ParkingRecord(id={self.id}, plate='{self.license_plate}', "
                f"type_id={self.parking_type_id}, status='{status}')>")