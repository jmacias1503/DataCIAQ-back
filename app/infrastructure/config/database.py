import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

def get_db():
    # Formato específico para Railway
    MONGODB_URI = os.getenv("MONGODB_URI")
    
    # Asegurar parámetros críticos
    if "?" not in MONGODB_URI:
        MONGODB_URI += "?authSource=admin&retryWrites=true&w=majority"
    elif "authSource=admin" not in MONGODB_URI:
        MONGODB_URI += "&authSource=admin"
    
    client = AsyncIOMotorClient(
        MONGODB_URI,
        # Parámetros adicionales críticos
        tlsAllowInvalidCertificates=True,  # Necesario para Railway
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        serverSelectionTimeoutMS=30000
    )
    return client[os.getenv("DB_NAME", "climate_sensors_db")]