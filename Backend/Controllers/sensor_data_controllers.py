import httpx
from sqlalchemy.orm import Session
import asyncio
from Models.models import SensorData, Receved_text
from Connections.connections import session

async def fetch_longitude():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://blynk.cloud/external/api/get?token=_wIJrhc9PmbhZcGZaqlh469aTc2k_ESq&dataStreamId=1')
        return float(response.text)

async def fetch_latitude():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://blynk.cloud/external/api/get?token=_wIJrhc9PmbhZcGZaqlh469aTc2k_ESq&dataStreamId=2')
        return float(response.text)
    
async def start_device_data_collection():
    device_config = [
        {"device_id": "nodeMCU", "longitude_url": "https://blynk.cloud/external/api/get?token=_wIJrhc9PmbhZcGZaqlh469aTc2k_ESq&dataStreamId=1", "latitude_url": "https://blynk.cloud/external/api/get?token=_wIJrhc9PmbhZcGZaqlh469aTc2k_ESq&dataStreamId=2"},
        {"device_id": "esp32", "longitude_url": "https://blynk.cloud/external/api/get?token=ctzGG4ReH04OwRoadMu9Mg_hLmT0J1Q6&dataStreamId=2", "latitude_url": "https://blynk.cloud/external/api/get?token=ctzGG4ReH04OwRoadMu9Mg_hLmT0J1Q6&dataStreamId=1"},
        # Add more devices as needed
    ]

    while True:
        for device in device_config:
            await fetch_and_store_device_data(device["device_id"], device["longitude_url"], device["latitude_url"])
        
        await asyncio.sleep(30) 

async def add_sensor_data_controller(sensor_data):
    try:
        SensorData.add_sensor_data(session,sensor_data["Nitrogen"],sensor_data["Phosphorus"], sensor_data["Potassium"])
        return {"status": "success", "message": "Data added successfully"}
    except Exception as e:
        print(f"Error occurred: {e}")

async def get_prediction(sensor_data):
    try:
        result = SensorData.get_predictions(sensor_data["Nitrogen"], sensor_data["Phosphorus"], sensor_data["Potassium"], 6.5)
        predicted_crop = result['predicted_crop'].tolist()
        print(predicted_crop)
        return {"status": "success", "predicted_crop": predicted_crop, "message": "Crop retrieved successfully"}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"status": "error", "message": str(e)}

        
async def fetch_and_store_device_data(device_id, longitude_url, latitude_url):
    async with httpx.AsyncClient() as client:
        longitude_response = await client.get(longitude_url)
        latitude_response = await client.get(latitude_url)

        longitude = float(longitude_response.text)
        latitude = float(latitude_response.text)

        await add_sensor_data(device_id, longitude, latitude)

async def add_sensor_data(device_id, longitude, latitude):
    db = session
    sensor_data = SensorData(device_id=device_id, lng=longitude, lat=latitude)
    try:
        db.add(sensor_data)
        db.commit()
        db.refresh(sensor_data)
    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback() 

async def combine_longitude_latitude():
    while True:
        try:
            longitude = await fetch_longitude()
            latitude = await fetch_latitude()
            await add_sensor_data(longitude, latitude)
        except Exception as e:
            print(f"Error: {e}") 
        await asyncio.sleep(30)


async def get_device_data(device_id):
    with session as db:
        return SensorData.get_data_by_device_id(db, device_id)
    
async def get_unique_device_ids():
    with session as db:
        result = SensorData.get_unique_devices(db)
        return [device_id for (device_id,) in result]
    
async def add_text_from_sensor(db:Session, text):
    text = Receved_text.add_text(db, text)
    return text

