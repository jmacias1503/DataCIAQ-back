from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import StreamingResponse
from typing import List
from app.core.domain.sensor_record import SensorRecord
from app.core.services.sensor_service_impl import SensorServiceImpl
from app.infrastructure.repositories.mongo_sensor_repository import MongoSensorRepository
from app.infrastructure.api.utils.export_utils import ExportUtils
from bson import ObjectId

router = APIRouter(prefix="/api/sensors", tags=["sensors"])

# Dependency
def get_sensor_service():
    repository = MongoSensorRepository()
    return SensorServiceImpl(repository)

@router.post("/", response_model=SensorRecord, status_code=201)
async def create_record(record: SensorRecord, service: SensorServiceImpl = Depends(get_sensor_service)):
    try:
        return await service.create_record(record)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[SensorRecord])
async def get_all_records(service: SensorServiceImpl = Depends(get_sensor_service)):
    try:
        return await service.get_all_records()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/equipo/{equipo}", response_model=List[SensorRecord])
async def get_records_by_equipment(equipo: str, service: SensorServiceImpl = Depends(get_sensor_service)):
    try:
        return await service.get_records_by_equipment(equipo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fecha/", response_model=List[SensorRecord])
async def get_records_by_date_range(
    start: str, 
    end: str, 
    service: SensorServiceImpl = Depends(get_sensor_service)
):
    try:
        return await service.get_records_by_date_range(start, end)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}", status_code=204)
async def delete_record(id: str, service: SensorServiceImpl = Depends(get_sensor_service)):
    try:
        success = await service.delete_record(id)
        if not success:
            raise HTTPException(status_code=404, detail="Record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/csv")
async def export_to_csv(service: SensorServiceImpl = Depends(get_sensor_service)):
    try:
        records = await service.get_all_records()
        csv_data = await ExportUtils.to_csv(records)
        
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=sensor_records.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/excel")
async def export_to_excel(service: SensorServiceImpl = Depends(get_sensor_service)):
    try:
        records = await service.get_all_records()
        excel_data = await ExportUtils.to_excel(records)
        
        return Response(
            content=excel_data,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=sensor_records.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))