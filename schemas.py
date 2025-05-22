from datetime import datetime

from pydantic import BaseModel


class SSensorAdd(BaseModel):
    type: str

class SSensor(SSensorAdd):
    id: int

class SReadingsAdd(BaseModel):
    sensor_id: int
    data: float
    date: datetime

class SReadings(SReadingsAdd):
    id: int