from app.models import models
from fastapi import FastAPI # type: ignore
from app.database.database import engine
from app.routers import parking
from fastapi.middleware.cors import CORSMiddleware # type: ignore

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(parking.router)