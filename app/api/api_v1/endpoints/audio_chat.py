from typing import List
from app.helpers.chatcompletion import response_audio
from app.helpers.qdrant import search_in_qdrant
from app.helpers.translate_agent import translate_banglish_to_bangla
from fastapi import BackgroundTasks, APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form
# import io
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import uuid
from app.api import deps
from app.db.models.files import File as FileModel
# from pydub import AudioSegment
from app.db.models.audio_chat import AudioChat as AudioChatModel
from app.schemas.audio_chat import AudioChat
from app.core.openai import openaiClient
from app.core.config import settings
from typing import Any, Optional
import os
router = APIRouter()

#################################################################################################
#  Get all audio_chats for a user
#################################################################################################
@router.get("/user/{user_id}", response_model=List[AudioChat])
async def get_all_audio_chats_for_a_user(user_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    
    try:
        db_audio_chat = db.query(AudioChatModel).filter(AudioChatModel.user_id == user_id).all()
        return db_audio_chat
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    


def store_the_audio_data_in_db(user_id, query, response, db):
    try:
        db_audio_chat = AudioChatModel(
            user_id = user_id,
            query = query,
            response = response
        )
        db.add(db_audio_chat)
        db.commit()
        db.refresh(db_audio_chat)
        return db_audio_chat
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

#################################################################################################
#  Generate Bengali transcript for an audio chat
#################################################################################################
@router.post("/")
async def create_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = Form(...),
    user_id: Optional[uuid.UUID] = Form(None),
    db: Session = Depends(deps.get_db)
):
    # Check file type
    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an MP3 file.")

    # Save the uploaded MP3 file to a temporary location
    temp_file_path = f"uploaded_files/{file.filename}"
    try:
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Send the saved file to OpenAI's Whisper API
        translated_text=  ""
        with open(temp_file_path, "rb") as audio_file:
            response = openaiClient.audio.translations.create(
                model="whisper-1",  # Use OpenAI Whisper model
                file=audio_file,
                response_format="text"
            )
            
            translated_text = response
        
        my_files = db.query(FileModel.id).filter(FileModel.uploader_id == user_id).all()

        # Extract the file IDs from the query result as a list
        merged_file_ids = [str(file.id) for file in my_files]

        knowledge = search_in_qdrant(settings.COLLECTION_NAME, translated_text, 10, merged_file_ids)
        print(knowledge)

        combined_result = ""
        result_list = []
        for result in knowledge:
            combined_result += f"## file_title: {result.payload.get('file_title')}\n"
            combined_result += f"file_summary: {result.payload.get('file_summary')}\n"
            combined_result += f"content: {result.payload.get('content')}\n\n"
            result.payload['id'] = result.id
            result_list.append(result.payload)


        
        openai_response = response_audio(translated_text, combined_result)
        print("openai_response", openai_response)

        background_tasks.add_task(
                store_the_audio_data_in_db, user_id, translated_text, openai_response, db
        )
        return openai_response
            
        
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during transcription: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


    

