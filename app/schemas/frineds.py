import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class FriendBase(BaseModel):
    user_id: uuid.UUID
    friend_id: uuid.UUID

class FriendCreate(FriendBase):
    pass

class FriendUpdate(FriendBase):
    pass

class FriendInDBBase(FriendBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Friend(FriendInDBBase):
    pass

class userFriends(BaseModel):
    friends: List[Friend] = []