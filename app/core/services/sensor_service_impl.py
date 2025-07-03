from typing import List
from app.core.domain.sensor_record import SensorRecord
from app.core.ports.sensor_service import SensorService
from app.core.ports.sensor_repository import SensorRepository

class SensorServiceImpl(SensorService):
    def __init__(self, repository: SensorRepository):
        self.repository = repository
    async def create_record(self, record_data: SensorRecord) -> SensorRecord:
        return await self.repository.save(record_data)
    
    async def get_all_records(self) -> List[SensorRecord]:
        return await self.repository.find_all()
    
    async def get_records_by_equipment(self, equipo: str) -> List[SensorRecord]:
        return await self.repository.find_by_equipment(equipo)
    
    async def get_records_by_date_range(self, start_date: str, end_date: str) -> List[SensorRecord]:
        return await self.repository.find_by_date_range(start_date, end_date)
    
    async def delete_record(self, id: str) -> bool:
        return await self.repository.delete(id)
    
    async def export_to_csv(self) -> str:
        raise NotImplementedError("Method should be implemented in infrastructure layer")
    
    async def export_to_excel(self) -> bytes:
        raise NotImplementedError("Method should be implemented in infrastructure layer")