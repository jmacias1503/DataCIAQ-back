from app.infrastructure.config.database import get_db
from app.core.domain.sensor_record import SensorRecord
from bson import ObjectId
from typing import List, Optional
import logging
from datetime import datetime

class MongoSensorRepository:
    def __init__(self):
        try:
            self.db = get_db()
            self.collection = self.db["sensor_records"]
            logging.info("Repositorio MongoDB inicializado correctamente")
        except Exception as e:
            logging.error(f"Error al inicializar repositorio MongoDB: {str(e)}")
            raise
    
    async def check_connection(self):
        """Método asíncrono para verificar la conexión"""
        try:
            await self.db.command('ping')
            logging.info("Conexión a MongoDB verificada correctamente")
            return True
        except Exception as e:
            logging.error(f"Error de conexión a MongoDB: {str(e)}")
            return False
    
    async def find_all(self, limit: int = 100, skip: int = 0) -> List[SensorRecord]:
        """Obtener todos los registros de sensores"""
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            sensor_records = []
            for doc in documents:
                sensor_record = self._document_to_sensor_record(doc)
                sensor_records.append(sensor_record)
            
            return sensor_records
        except Exception as e:
            logging.error(f"Error al obtener registros: {str(e)}")
            raise
    
    async def find_by_id(self, record_id: str) -> Optional[SensorRecord]:
        """Obtener un registro por ID"""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(record_id)})
            if doc:
                return self._document_to_sensor_record(doc)
            return None
        except Exception as e:
            logging.error(f"Error al obtener registro por ID: {str(e)}")
            raise
    
    async def save(self, sensor_record: SensorRecord) -> SensorRecord:
        """Guardar un nuevo registro"""
        try:
            document = self._sensor_record_to_document(sensor_record)
            result = await self.collection.insert_one(document)
            
            # Si SensorRecord no tiene atributo 'id', necesitas manejarlo diferente
            # Opción 1: Si el modelo tiene un método para establecer el ID
            if hasattr(sensor_record, 'id'):
                sensor_record.id = str(result.inserted_id)
            
            # Opción 2: Crear una nueva instancia con el ID
            # O retornar el documento insertado convertido de nuevo
            saved_doc = await self.collection.find_one({"_id": result.inserted_id})
            return self._document_to_sensor_record(saved_doc)
            
        except Exception as e:
            logging.error(f"Error al guardar registro: {str(e)}")
            raise
    
    async def update(self, sensor_record: SensorRecord) -> Optional[SensorRecord]:
        """Actualizar un registro existente"""
        try:
            document = self._sensor_record_to_document(sensor_record)
            document.pop('_id', None)  # Remover _id para la actualización
            
            result = await self.collection.update_one(
                {"_id": ObjectId(sensor_record.id)},
                {"$set": document}
            )
            
            if result.modified_count > 0:
                return sensor_record
            return None
        except Exception as e:
            logging.error(f"Error al actualizar registro: {str(e)}")
            raise
    
    async def delete(self, record_id: str) -> bool:
        """Eliminar un registro por ID"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(record_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f"Error al eliminar registro: {str(e)}")
            raise
    
    async def find_by_sensor_id(self, equipo: str, limit: int = 100) -> List[SensorRecord]:
        """Obtener registros por equipo"""
        try:
            cursor = self.collection.find({"equipo": equipo}).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            sensor_records = []
            for doc in documents:
                sensor_record = self._document_to_sensor_record(doc)
                sensor_records.append(sensor_record)
            
            return sensor_records
        except Exception as e:
            logging.error(f"Error al obtener registros por equipo: {str(e)}")
            raise
    
    def _document_to_sensor_record(self, doc: dict) -> SensorRecord:
        """Convertir documento de MongoDB a SensorRecord"""
        # Manejar el caso donde id puede no existir en el modelo
        sensor_data = {
            "equipo": doc.get("equipo") or "",
            "fecha_hora": doc.get("fecha_hora") or "",
            "temperatura": doc.get("temperatura") or 0.0,
            "humedad": doc.get("humedad") or "",
            "humedad_s30": doc.get("humedad_s30") or "",
            "humedad_s15": doc.get("humedad_s15") or "",
            "radiacion": doc.get("radiacion") or ""
        }
        
        # Solo agregar id si el modelo lo soporta
        if hasattr(SensorRecord, 'id') or 'id' in SensorRecord.__annotations__:
            sensor_data["id"] = str(doc.get("_id"))
        
        return SensorRecord(**sensor_data)

    def _sensor_record_to_document(self, sensor_record: SensorRecord) -> dict:
        """Convertir SensorRecord a documento de MongoDB"""
        doc = {
            "equipo": sensor_record.equipo,
            "fecha_hora": sensor_record.fecha_hora,
            "temperatura": sensor_record.temperatura,
            "humedad": sensor_record.humedad,
            "humedad_s30": sensor_record.humedad_s30,
            "humedad_s15": sensor_record.humedad_s15,
            "radiacion": sensor_record.radiacion
        }
        
        # Solo agregar _id si el objeto tiene id
        if hasattr(sensor_record, 'id') and sensor_record.id:
            doc["_id"] = ObjectId(sensor_record.id)
        
        return doc