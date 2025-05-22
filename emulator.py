import asyncio
import random
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from database import new_session, SensorOrm
from database import ReadingOrm
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

# Получение ID всех сенсоров
async def get_all_sensor_ids() -> list[int]:
    async with new_session() as session:
        result = await session.execute(select(SensorOrm.id).distinct())
        return [row[0] for row in result.all()]

def generate_fake_value(sensor_id: int) -> float:
    match sensor_id:
        case 1:  # Температура thermometer
            return round(random.uniform(20.0, 25.0), 2)
        case 2:  # Влажность humidity
            return round(random.uniform(40.0, 60.0), 2)
        case 3:  # CO2
            return round(random.uniform(400.0, 800.0), 2)
        case _:
            return round(random.uniform(10.0, 100.0), 2)



async def sensor_emulator():
    while True:
        try:
            sensor_ids = await get_all_sensor_ids()
            async with new_session() as session:
                for sensor_id in sensor_ids:
                    new_reading = ReadingOrm(
                        sensor_id =sensor_id,
                        date =datetime.now(ZoneInfo("Europe/Moscow")),
                        data =generate_fake_value(sensor_id)
                    )
                    session.add(new_reading)
                await session.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при эмуляции: {e}")
        await asyncio.sleep(5)