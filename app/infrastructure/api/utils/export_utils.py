import pandas as pd
from io import StringIO, BytesIO
from typing import List
from app.core.domain.sensor_record import SensorRecord

class ExportUtils:
    @staticmethod
    async def to_csv(records: List[SensorRecord]) -> str:
        df = pd.DataFrame([record.model_dump() for record in records])
        output = StringIO()
        df.to_csv(output, index=False)
        return output.getvalue()
    
    @staticmethod
    async def to_excel(records: List[SensorRecord]) -> bytes:
        df = pd.DataFrame([record.model_dump() for record in records])
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()