from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.domain.sensor_record import SensorRecord

class SensorRepository(ABC):
    @abstractmethod
    async def save(self, record: SensorRecord) -> SensorRecord:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[SensorRecord]:
        pass
    
    @abstractmethod
    async def find_by_equipment(self, equipo: str) -> List[SensorRecord]:
        pass
    
    @abstractmethod
    async def find_by_date_range(self, start_date: str, end_date: str) -> List[SensorRecord]:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass