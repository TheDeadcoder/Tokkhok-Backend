from fastapi import APIRouter, HTTPException, Request, Response, Depends
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.auth import UserAuth, TokenData
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from app.core.supabase import supabase 
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.api import deps
# from app.schemas.users import User
from app.db.models.users import User as UserModel

router = APIRouter()


################################################################################################
#  Sign up with email and password
################################################################################################
@router.post("/signup")
async def sign_up(user: UserAuth):
    try:
        response = supabase.auth.sign_up({
            'email': user.email,
            'password': user.password
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Sign-up failed")
        return {"message": "User signed up successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#################################################################################################
#   Log in with email and password
#################################################################################################
@router.post("/signin")
async def sign_in(user: UserAuth):
    try:
        response = supabase.auth.sign_in_with_password({
            'email': user.email,
            'password': user.password
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Sign-in failed")
        return {"message": "User signed in successfully", "session": response.session}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#################################################################################################
#   Logout
#################################################################################################
@router.post("/logout")
async def log_out(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        supabase.auth.sign_out()
        return {"message": f"Logged Out"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
