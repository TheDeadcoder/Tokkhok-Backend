from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import uuid
from app.api import deps
from app.db.models.users import User as UserModel
from app.db.models.usertrain import UserTrain as UserTrainModel

from app.schemas.users import UserInDBBase, UserCreate, UserUpdate
from app.schemas.usertrain import userTrainBase, userTrainCreate, userTrainUpdate, userTrainInDBBase

from app.helpers.validators import validate_email
router = APIRouter()

#################################################################################################
#   GET all userTrain
#################################################################################################
@router.get("/", response_model=List[userTrainInDBBase])
async def get_all_userTrain(db: Session = Depends(deps.get_db)):
    try:
        db_userTrain = db.query(UserTrainModel).all()
        return db_userTrain
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

#################################################################################################
#   GET all approved userTrain
#################################################################################################
@router.get("/approved", response_model=List[userTrainInDBBase])
async def get_all_approved_userTrain(db: Session = Depends(deps.get_db)):
    try:
        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.is_approved == True).all()
        return db_userTrain
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

#################################################################################################
#   GET all unapproved userTrain
#################################################################################################
@router.get("/unapproved", response_model=List[userTrainInDBBase])
async def get_all_unapproved_userTrain(db: Session = Depends(deps.get_db)):
    try:
        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.is_approved == False).all()
        return db_userTrain
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
#   GET all userTrain for a partcular user
#################################################################################################
@router.get("/user/{user_id}", response_model=List[userTrainInDBBase])
async def get_all_userTrain_for_user(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.user_id == user_id).all()
        return db_userTrain
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
#   GET all approved userTrain for a partcular user
#################################################################################################
@router.get("/user/{user_id}/approved", response_model=List[userTrainInDBBase])
async def get_all_approved_userTrain_for_user(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.user_id == user_id, UserTrainModel.is_approved == True).all()
        return db_userTrain
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
#   GET all unapproved userTrain for a partcular user
#################################################################################################
@router.get("/user/{user_id}/unapproved", response_model=List[userTrainInDBBase])
async def get_all_unapproved_userTrain_for_user(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.user_id == user_id, UserTrainModel.is_approved == False).all()
        return db_userTrain
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

#################################################################################################
#   GET userTrain BY ID
#################################################################################################
@router.get("/{userTrain_id}", response_model=userTrainInDBBase)
async def get_userTrain_by_id(userTrain_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    
    try:
        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.id == userTrain_id).first()
        if not db_userTrain:
            raise HTTPException(status_code=404, detail="UserTrain not found")
        return db_userTrain
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
#   CREATE userTrain
#################################################################################################
@router.post("/", response_model=userTrainInDBBase)
async def create_userTrain(*, db: Session = Depends(deps.get_db), userTrain_in: userTrainCreate):
    
    try:
        db_userTrain = UserTrainModel(
            user_id = userTrain_in.user_id,
            banglish=userTrain_in.banglish,
            bangla=userTrain_in.bangla
        )
        db.add(db_userTrain)
        db.commit()
        db.refresh(db_userTrain)
        return db_userTrain
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
#   UPDATE userTrain
#################################################################################################
@router.put("/{userTrain_id}", response_model=userTrainInDBBase)
async def update_userTrain(*, db: Session = Depends(deps.get_db), userTrain_id: uuid.UUID, userTrain_in: userTrainUpdate):
    
    try:
        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.id == userTrain_id).first()
        if not db_userTrain:
            raise HTTPException(status_code=404, detail="UserTrain not found")
        
        if userTrain_in.banglish:
            db_userTrain.banglish = userTrain_in.banglish
        if userTrain_in.bangla:
            db_userTrain.bangla = userTrain_in.bangla
        if userTrain_in.is_approved:
            db_userTrain.is_approved = userTrain_in.is_approved
        
        db.commit()
        db.refresh(db_userTrain)
        return db_userTrain
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

#################################################################################################
#   DELETE userTrain
#################################################################################################
@router.delete("/{userTrain_id}")
async def delete_userTrain(userTrain_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    
    try:
        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.id == userTrain_id).first()
        if not db_userTrain:
            raise HTTPException(status_code=404, detail="UserTrain not found")
        
        db.delete(db_userTrain)
        db.commit()
        return {"message": "UserTrain deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

