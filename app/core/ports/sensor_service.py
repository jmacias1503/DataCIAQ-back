from abc import ABC, abstractmethod
from typing import List
from app.core.domain.sensor_record import SensorRecord

class SensorService(ABC):
    @abstractmethod
    async def create_record(self, record_data: SensorRecord) -> SensorRecord:
        pass
    
    @abstractmethod
    async def get_all_records(self) -> List[SensorRecord]:
        pass
    
    @abstractmethod
    async def get_records_by_equipment(self, equipo: str) -> List[SensorRecord]:
        pass
    
    @abstractmethod
    async def get_records_by_date_range(self, start_date: str, end_date: str) -> List[SensorRecord]:
        pass
    
    @abstractmethod
    async def delete_record(self, id: str) -> bool:
        pass
    
    @abstractmethod
    async def export_to_csv(self) -> str:
        pass
    
    @abstractmethod
    async def export_to_excel(self) -> bytes:
        pass