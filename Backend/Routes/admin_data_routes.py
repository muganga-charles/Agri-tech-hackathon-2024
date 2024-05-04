from fastapi import APIRouter, HTTPException
import asyncio
from Models.models import UsernameChangeRequest
from Controllers.admin_controller import create_admin,login,reset_user_password,send_password_reset,change_username
router = APIRouter()

# create admin
@router.post("/create_admin")
async def create_admin_route(admin:dict):
    try:
        return await create_admin(admin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# login admin
@router.post("/login")
async def login_route(admin:dict):
    try:
        return await login(admin)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/request_password_reset")
async def request_password_reset(credentials: dict):
    username = credentials["username"]
    try:
        send_password_reset(username)
        return {"message": "Reset link sent to your email address"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.post("/reset_password")
async def reset_password_endpoint(token_and_password: dict):
    token = token_and_password["token"]
    new_password = token_and_password["new_password"]
    try:
        reset_user_password(token, new_password)
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/change_username")
async def change_username_endpoint(request: UsernameChangeRequest):
    try:
        response = change_username(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))