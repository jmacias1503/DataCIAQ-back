from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SensorRecord(BaseModel):
    equipo: str
    fecha_hora: str
    temperatura: float
    humedad: str
    humedad_s30: str
    humedad_s15: str
    radiacion: str

    class Config:
        from_attributes = True