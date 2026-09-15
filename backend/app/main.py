from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.app.publicaciones.router import router as publicaciones_router


class HealthResponse(BaseModel):
    status: str
    service: str


app = FastAPI(
    title="CampusMarket API",
    version="1.0.0",
    description=(
        "API HTTP/JSON de CampusMarket para crear y consultar publicaciones. "
        "El contrato versionado es contracts/openapi-v1.json."
    ),
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Entorno local",
        }
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(publicaciones_router)


@app.get(
    "/health",
    response_model=HealthResponse,
    operation_id="consultarSalud",
    summary="Consultar la salud del backend",
)
def health_check():
    return {
        "status": "ok",
        "service": "campusmarket-api",
    }
