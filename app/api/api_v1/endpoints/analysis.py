from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import uuid
from sqlalchemy import func
from app.api import deps

from app.db.models.users import User as UserModel
from app.db.models.files import File as FileModel
from app.db.models.chats import Chat as ChatModel
from app.db.models.messages import Message as MessageModel
from app.db.models.audio_chat import AudioChat as AudioChatModel
from app.db.models.translations import Translation as TranslationModel
from app.db.models.usertrain import UserTrain as UserTrainModel

router = APIRouter()

#################################################################################################
#  Get analysis for a user
#################################################################################################
@router.get("/user/{user_id}", response_model=dict)
async def get_analysis_for_a_user(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    try:
        
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        
        number_of_files = db.query(FileModel).filter(FileModel.uploader_id == user_id).count()

        
        number_of_chats = db.query(ChatModel).filter(ChatModel.user_id == user_id).count()

        
        number_of_messages = (
            db.query(MessageModel)
            .join(ChatModel, MessageModel.chat_id == ChatModel.id)
            .filter(ChatModel.user_id == user_id)
            .count()
        )

        
        number_of_audio_messages = db.query(AudioChatModel).filter(AudioChatModel.user_id == user_id).count()

       
        number_of_user_trains = db.query(UserTrainModel).filter(UserTrainModel.user_id == user_id).count()

        
        number_of_approved_user_trains = (
            db.query(UserTrainModel)
            .filter(UserTrainModel.user_id == user_id, UserTrainModel.is_approved == True)
            .count()
        )

       
        number_of_translations = db.query(TranslationModel).filter(TranslationModel.user_id == user_id).count()

        
        translations = db.query(TranslationModel.translated_text).filter(TranslationModel.user_id == user_id).all()
        total_number_words_translated = sum(
            len(translation.translated_text.split()) for translation in translations
        )

        
        user_analysis = {
            "number_of_files": number_of_files,
            "number_of_chats": number_of_chats,
            "number_of_messages": number_of_messages,
            "number_of_audio_messages": number_of_audio_messages,
            "number_of_user_trains": number_of_user_trains,
            "number_of_approved_user_trains": number_of_approved_user_trains,
            "number_of_translations": number_of_translations,
            "total_number_words_translated": total_number_words_translated,
        }

        return user_analysis
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
