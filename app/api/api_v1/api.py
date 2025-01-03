from fastapi import APIRouter
from app.api.api_v1.endpoints import users, auth, chats, usertrain, files
api_router_v1 = APIRouter()

api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
api_router_v1.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router_v1.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router_v1.include_router(usertrain.router, prefix="/usertrain", tags=["usertrain"])
api_router_v1.include_router(files.router, prefix="/files", tags=["files"])
