from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from Controllers.sensor_data_controllers import start_device_data_collection

from Routes import (
    admin_data_routes,
    sensor_data_routes
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class AppLifespan:
#     def __init__(self):
#         self.background_task = None

#     async def startup(self):
#         self.background_task = asyncio.create_task(start_device_data_collection())

#     async def shutdown(self):
#         if self.background_task:
#             self.background_task.cancel()
#             try:
#                 await self.background_task
#             except asyncio.CancelledError:
#                 pass

# app_lifespan = AppLifespan()

# @app.on_event("startup")
# async def startup_event():
#     await app_lifespan.startup()

# @app.on_event("shutdown")
# async def shutdown_event():
#     await app_lifespan.shutdown()

# @app.get("/")
# async def read_root(lifespan: AppLifespan = Depends()):
#     return {"Hello": "World"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(sensor_data_routes.router, prefix= "/data")
app.include_router(admin_data_routes.router, prefix= "/admin")

if __name__ == "__main__":
    import uvicorn
    from watchgod import watch
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000,reload=True, workers=2)
