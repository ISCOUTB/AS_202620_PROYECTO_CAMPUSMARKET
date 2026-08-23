from fastapi import FastAPI

app = FastAPI(
    title="CampusMarket API",
    version="0.1.0",
    description="Esqueleto ejecutable del backend de CampusMarket.",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "campusmarket-api",
    }
