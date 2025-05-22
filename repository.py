from sqlalchemy import select

from database import new_session, ReadingOrm, SensorOrm
from schemas import SSensorAdd, SReadingsAdd, SReadings

class SensorRepository:
    @classmethod
    async def add_sensor(cls, sensor: SSensorAdd):
        async with new_session() as session:
            data = sensor.model_dump()
            new_sensor = SensorOrm(**data)
            session.add(new_sensor)
            await session.flush()
            await session.commit()
            return new_sensor.id

    @classmethod
    async def get_sensors(cls):
        async with new_session() as session:
            result = await session.execute(select(SensorOrm))
            sensors = result.scalars().all()
            return sensors


class ReadingRepository:
    @classmethod
    async def add_readings(cls, readings: SReadingsAdd) -> int:
        async with new_session() as session:
            data = readings.model_dump()
            new_readings = ReadingOrm(**data)
            session.add(new_readings)
            await session.flush()
            await session.commit()
            return new_readings.id

    @classmethod
    async def get_readings(cls, sensor_id: int) -> list[SReadings]:
        async with new_session() as session:
            query = select(ReadingOrm).where(ReadingOrm.sensor_id == sensor_id)
            result = await session.execute(query)
            readings_model = result.scalars().all()
            readings = [SReadings.model_validate(r, from_attributes=True) for r in readings_model]
            return readings
