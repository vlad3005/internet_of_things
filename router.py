from fastapi import APIRouter, Depends
from repository import ReadingRepository, SensorRepository
from schemas import SReadingsAdd, SReadings, SSensor, SSensorAdd


router = APIRouter(prefix="/api")

@router.post("/readings")
async def add_task(reading: SReadingsAdd = Depends()):
   reading_id = await ReadingRepository.add_readings(reading)
   return {"id": reading_id}

@router.get("/readings")
async def get_tasks() -> list[SReadings]:
   readings = await ReadingRepository.get_readings(1)
   return readings

@router.get("/readings/{sensor_id}")
async def get_readings(sensor_id: int):
    readings = await ReadingRepository.get_readings(sensor_id)
    return readings


@router.post("/sensors")
async def post_sensor(sensor: SSensorAdd = Depends()):
   new_sensor_id = await SensorRepository.add_sensor(sensor)
   return {"id": new_sensor_id}