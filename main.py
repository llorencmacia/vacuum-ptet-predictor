import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import simulation  # Importem des del paquet 'app'

app = FastAPI()

# BASE_DIR serà "C:\Users\lars\Documents\Shared\00.API"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# La carpeta static és a "BASE_DIR/app/static"
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(simulation.router)