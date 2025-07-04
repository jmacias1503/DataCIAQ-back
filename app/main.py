from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.api.routers.sensor_router import router as sensor_router
from app.infrastructure.config.database import get_db
import uvicorn

app = FastAPI(
    title="Climate Sensor API",
    description="API for managing climate sensor records",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sensor_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Climate Sensor API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)