from fastapi import FastAPI
from app.routers import parking, auth
from app.database import database
from app.models import models

app = FastAPI(title="Parking API", description="API for parking management")

# Configuração do banco de dados
models.Base.metadata.create_all(bind=database.engine)

# Inclusão dos routers
app.include_router(auth.router)
app.include_router(parking.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Parking API"}