from contextlib import asynccontextmanager
import asyncio

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

from fastapi import FastAPI

from emulator import sensor_emulator
from repository import SensorRepository
from router import router as router


from database import delete_tables, create_tables
from schemas import  SSensorAdd


@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   await create_sensor()
   await startup_event()
   print("База готова")
   yield
   await delete_tables()
   print("База очищена")
app = FastAPI(lifespan=lifespan)




templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def create_sensor():
   types = ["temperature", "humidity", "co2"]
   for t in types:
      await SensorRepository.add_sensor(SSensorAdd(type=t))

async def startup_event():
    asyncio.create_task(sensor_emulator())
app.include_router(router)

