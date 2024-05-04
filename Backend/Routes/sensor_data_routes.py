from fastapi import APIRouter, HTTPException,Depends
import asyncio
from Connections.connections import SessionLocal
from sqlalchemy.orm import Session
from Controllers.sensor_data_controllers import (
    get_device_data,
    get_unique_device_ids,
    add_sensor_data_controller,
    add_text_from_sensor,
    start_device_data_collection,
    get_prediction
) 
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.on_event("startup")
# async def startup_event():
#     asyncio.create_task(combine_longitude_latitude())
@router.post("/add")
async def add_sensor_data(sensor_data: dict):
    try:
        await add_sensor_data_controller(sensor_data)
        return {"status": "success", "message": "Data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predictions")
async def get_predictions(sensor_data: dict):
    try:
        res = await get_prediction(sensor_data)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/device/")
async def read_device_data(device_id: str):
    try:
        data = await get_device_data(device_id)
        if not data:
            raise HTTPException(status_code=404, detail="Device not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# get unique device id
@router.get("/device/unique")
async def read_unique_device_id():
    devices = await get_unique_device_ids()
    return {"devices": devices}

@router.post('/device/text/')
async def add_test_route(text_object:dict,db: Session = Depends(get_db)):
    text = text_object['message']
    sent_text = await add_text_from_sensor(db, text)
    return {"status": "success", "message": "Data added successfully"}

@router.get('/soil_data')
async def get_soil_data():
    return await start_device_data_collection()
     