from sqlalchemy.orm import Session
from fastapi import Depends, Request, HTTPException
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id(request: Request):
    user_id = getattr(request.state, 'user_id', None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id

def get_current_user_id_optional(request: Request):
    return getattr(request.state, 'user_id', None)   