from fastapi import APIRouter
from app.api.api_v1.endpoints import users, auth, chats, usertrain, files, translation, audio_chat, analysis
api_router_v1 = APIRouter()

api_router_v1.include_router(users.router, prefix="/users", tags=["users"])
api_router_v1.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router_v1.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router_v1.include_router(usertrain.router, prefix="/usertrain", tags=["usertrain"])
api_router_v1.include_router(files.router, prefix="/files", tags=["files"])
api_router_v1.include_router(translation.router, prefix="/translation", tags=["translation"])
api_router_v1.include_router(audio_chat.router, prefix="/audio_chat", tags=["audio_chat"])
api_router_v1.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
