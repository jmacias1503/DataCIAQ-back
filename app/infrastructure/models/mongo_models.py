from bson import ObjectId
from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing import Any, Dict, Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v: str) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

class MongoSensorRecord(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    equipo: str
    fecha_hora: str
    temperatura: float
    humedad: str
    humedad_s30: str
    humedad_s15: str
    radiacion: str

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}
        populate_by_name = True