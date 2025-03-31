# from typing import List
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import SQLAlchemyError
# from pydantic import ValidationError
# import uuid
# from app.api import deps
# from app.db.models.users import User as UserModel
# from app.db.models.friends import Friend as FriendModel
# from app.schemas.frineds import FriendCreate, FriendUpdate, Friend
# router = APIRouter()

# #################################################################################################
# #   create a friend of a user
# #################################################################################################
# @router.post("/", response_model=Friend)
# async def create_friend(*, db: Session = Depends(deps.get_db), friend_in: FriendCreate): 
#     try:   
#         db_friend_1 = FriendModel(
#             user_id = friend_in.user_id,
#             friend_id = friend_in.friend_id
#         )
#         db_friend_2 = FriendModel(
#             friend_id = friend_in.user_id,
#             user_id = friend_in.friend_id
#         )
#         db.add(db_friend_1)
#         db.add(db_friend_2)
#         db.commit()
#         db.refresh(db_friend_1)
#         db.refresh(db_friend_2)
#         return db_friend_1
#     except ValidationError as ve:
#         raise HTTPException(status_code=422, detail=str(ve))
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Database error: " + str(e))
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))