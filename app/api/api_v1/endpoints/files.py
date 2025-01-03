from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import uuid
from app.api import deps


from app.db.models.users import User as UserModel
from app.db.models.files import File as FileModel



from app.schemas.files import FileCreate, FileInDBBase, FileUpdate
router = APIRouter()


#################################################################################################
# GET all files
#################################################################################################
@router.get("/", response_model=List[FileInDBBase])
async def get_all_files(db: Session = Depends(deps.get_db)):
    try:
        db_userTrain = db.query(FileModel).all()
        return db_userTrain
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

#################################################################################################
# GET all files for a user
#################################################################################################
@router.get("/user/{user_id}", response_model=List[FileInDBBase])
async def get_all_files_for_a_user(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        db_file = db.query(FileModel).filter(FileModel.uploader_id == user_id).all()
        return db_file
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

#################################################################################################
# GET all public files for a user
#################################################################################################
@router.get("/user/public/{user_id}", response_model=List[FileInDBBase])
async def get_all_public_files_for_a_user(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        db_file = db.query(FileModel).filter(FileModel.uploader_id == user_id, FileModel.privacy_status == "public").all()
        return db_file
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
# GET all private files for a user
#################################################################################################
@router.get("/user/private/{user_id}", response_model=List[FileInDBBase])
async def get_all_private_files_for_a_user(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        db_file = db.query(FileModel).filter(FileModel.uploader_id == user_id, FileModel.privacy_status == "private").all()
        return db_file
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
# GET all public files cross-platform
#################################################################################################
@router.get("/public", response_model=List[FileInDBBase])
async def get_all_public_files_cross_platform(db: Session = Depends(deps.get_db)):
    try:
        db_file = db.query(FileModel).filter(FileModel.privacy_status == "public").all()
        return db_file
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
# create a file
#################################################################################################
