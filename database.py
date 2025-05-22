from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine("sqlite+aiosqlite:///sensor.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
   pass

class SensorOrm(Model):
    __tablename__ = 'sensors'
    id: Mapped[int] = Column(Integer, primary_key=True)
    type: Mapped[str]
    readings = relationship("ReadingOrm")

    class Config:
        orm_mode = True

class ReadingOrm(Model):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'), nullable=False)
    data: Mapped[float]
    date: Mapped[datetime] = mapped_column()

    class Config:
        orm_mode = True

async def create_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
   async with engine.begin() as conn:
       await conn.run_sync(Model.metadata.drop_all)