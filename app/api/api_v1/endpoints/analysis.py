from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import uuid
from app.api import deps


from app.db.models.users import User as UserModel
from app.db.models.files import File as FileModel
from app.db.models.chats import Chat as ChatModel
from app.db.models.messages import Message as MessageModel
from app.db.models.audio_chat import AudioChat as AudioChatModel
from app.db.models.translations import Translation as TranslationModel
from app.db.models.usertrain import UserTrain as UserTrainModel

from app.helpers.validators import validate_email
router = APIRouter()



