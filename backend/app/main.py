from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.publicaciones.router import router as publicaciones_router


app = FastAPI(
    title="CampusMarket API",
    version="0.2.0",
    description="Backend ejecutable de CampusMarket con corte vertical S4.",
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


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "campusmarket-api",
    }
