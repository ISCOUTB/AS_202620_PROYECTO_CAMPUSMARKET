from fastapi import FastAPI

app = FastAPI(
    title="CampusMarket API",
    version="0.1.0",
    description="Esqueleto ejecutable del backend de CampusMarket.",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "campusmarket-api"
    }
