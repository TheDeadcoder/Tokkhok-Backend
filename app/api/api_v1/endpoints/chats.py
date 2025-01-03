from typing import List
import uuid
from app.helpers.chatcompletion import response_first, response_later
from app.helpers.qdrant import search_in_qdrant
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload, contains_eager, subqueryload
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from app.helpers.prompt_normalize import prompt_normalize_first, prompt_normalize_later

from app.api import deps
from app.schemas.chats import Chat, ChatCreate, ChatUpdate, ChatWithMessages, ChatResponse
from app.db.models.chats import Chat as ChatModel
from app.db.models.messages import Message as MessageModel
from app.db.models.files import File as FileModel
from app.schemas.messages import Message, MessageCreate

from app.core.config import settings


router = APIRouter()


#################################################################################################
#   CREATE CHAT
#################################################################################################
@router.post("/", response_model = ChatResponse)
async def create_chat(*, db: Session = Depends(deps.get_db), chat_in: ChatCreate):
    
    try:
        db_chat = ChatModel(
            user_id = chat_in.user_id,
            chat_name = chat_in.chat_name,
            selected_public_file_ids = chat_in.public_file_ids
        )
        db.add(db_chat)
        db.commit()
        db.refresh(db_chat)
        
        db_message_user = MessageModel(
            chat_id = db_chat.id,
            sender = "user",
            content = db_chat.chat_name
        )
        
        db.add(db_message_user)
        db.commit()
        db.refresh(db_message_user)
        
        queryText = db_chat.chat_name

        standardized_prompt = prompt_normalize_first(queryText)
        my_files = db.query(FileModel.id).filter(FileModel.uploader_id == chat_in.user_id).all()

        # Extract the file IDs from the query result as a list
        my_file_ids = [file.id for file in my_files]

        # Combine my_file_ids and given_files into a unique set of IDs
        merged_file_ids = list(set(my_file_ids + chat_in.public_file_ids))
        # convert into an array of string
        merged_file_ids = [str(file_id) for file_id in merged_file_ids]

        knowledge = search_in_qdrant(settings.COLLECTION_NAME, standardized_prompt, 10, merged_file_ids)
        print(knowledge)

        combined_result = ""
        result_list = []
        for result in knowledge:
            combined_result += f"## point_id: {result.id}\n"
            combined_result += f"file_title: {result.payload.get('file_title')}\n"
            combined_result += f"file_summary: {result.payload.get('file_summary')}\n"
            combined_result += f"content: {result.payload.get('content')}\n\n"
            result.payload['id'] = result.id
            result_list.append(result.payload)


        
        openai_response = response_first(standardized_prompt, combined_result)
        print(openai_response)

        response_content = openai_response.response
        used_resources = set(openai_response.used_resources)

        filtered_result_list = [
            result for result in result_list if str(result.get('id')) in used_resources
        ]
        
        db_message_assistant = MessageModel(
            chat_id=db_chat.id,
            sender="assistant",
            content=response_content,
            knowledge=filtered_result_list
        )
        
        db.add(db_message_assistant)
        db.commit()
        db.refresh(db_message_assistant)
        

        response = ChatResponse(
            id = db_chat.id,
            user_id = db_chat.user_id,
            chat_name = db_chat.chat_name,
            created_at = db_chat.created_at,
            updated_at = db_chat.updated_at,
            query=Message(
                id=db_message_user.id,
                chat_id=db_message_user.chat_id,
                sender=db_message_user.sender,
                content=db_message_user.content,
                knowledge=db_message_user.knowledge,
                created_at=db_message_user.created_at,
                updated_at=db_message_user.updated_at
            ),
            response=Message(
                id=db_message_assistant.id,
                chat_id=db_message_assistant.chat_id,
                sender=db_message_assistant.sender,
                content=db_message_assistant.content,
                knowledge=db_message_assistant.knowledge,
                created_at=db_message_assistant.created_at,
                updated_at=db_message_assistant.updated_at
            )
        )
        
        return response
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

#################################################################################################
#   UPDATE CHAT 
#################################################################################################
@router.put("/add_message/{chat_id}", response_model = ChatResponse)
async def update_chat(*, db: Session = Depends(deps.get_db), chat_id: uuid.UUID, message_in: MessageCreate):
    try:
        db_chat = db.query(ChatModel).filter(ChatModel.id == chat_id).first()
        if not db_chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        queryText = message_in.content
        
        db_message_user = MessageModel(
            chat_id = db_chat.id,
            sender = "user",
            content = queryText
        )
        
        db.add(db_message_user)
        db.commit()
        db.refresh(db_message_user)

        
        db_full_chat = (
            db.query(ChatModel)
            .options(joinedload(ChatModel.messages))
            .filter(ChatModel.id == db_chat.id)
            .first()
        )
        if not db_full_chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        db_full_chat.messages.sort(key=lambda message: message.created_at)
        print(db_full_chat)

        chat_history = f"Conversation:\n\n"
        for currMessage in db_full_chat.messages:
            sender = "assistant" if currMessage.sender == "assistant" else "human"
            chat_history += f"{sender}: {currMessage.content}\n\n"

        print(chat_history)

        standardize_last_query = prompt_normalize_later(chat_history)
        print("*****************************")
        print(standardize_last_query)

        my_files = db.query(FileModel.id).filter(FileModel.uploader_id == db_chat.user_id).all()

        # Extract the file IDs from the query result as a list
        my_file_ids = [file.id for file in my_files]

        # Combine my_file_ids and given_files into a unique set of IDs
        merged_file_ids = list(set(my_file_ids + db_chat.selected_public_file_ids))
        # convert into an array of string
        merged_file_ids = [str(file_id) for file_id in merged_file_ids]

        knowledge = search_in_qdrant(settings.COLLECTION_NAME, standardize_last_query, 10, merged_file_ids)

        combined_result = ""
        result_list = []
        for result in knowledge:
            combined_result += f"## point_id: {result.id}\n"
            combined_result += f"file_title: {result.payload.get('file_title')}\n"
            combined_result += f"file_summary: {result.payload.get('file_summary')}\n"
            combined_result += f"content: {result.payload.get('content')}\n\n"
            result.payload['id'] = result.id
            result_list.append(result.payload)

        
        openai_response = response_later(chat_history, combined_result)

        response_content = openai_response.response
        used_resources = set(openai_response.used_resources)

        filtered_result_list = [
            result for result in result_list if str(result.get('id')) in used_resources
        ]

        db_message_assistant = MessageModel(
            chat_id=db_chat.id,
            sender="assistant",
            content=response_content,
            knowledge=filtered_result_list
        )
        
        db.add(db_message_assistant)
        db.commit()
        db.refresh(db_message_assistant)
        print(db_message_user.content)
        
        response = ChatResponse(
            id = db_chat.id,
            user_id = db_chat.user_id,
            chat_name = db_chat.chat_name,
            created_at = db_chat.created_at,
            updated_at = db_chat.updated_at,
            query=Message(
                id=db_message_user.id,
                chat_id=db_message_user.chat_id,
                sender=db_message_user.sender,
                content=db_message_user.content,
                knowledge=db_message_user.knowledge,
                created_at=db_message_user.created_at,
                updated_at=db_message_user.updated_at
            ),
            response=Message(
                id=db_message_assistant.id,
                chat_id=db_message_assistant.chat_id,
                sender=db_message_assistant.sender,
                content=db_message_assistant.content,
                knowledge=db_message_assistant.knowledge,
                created_at=db_message_assistant.created_at,
                updated_at=db_message_assistant.updated_at
            )
        )
        
        return response
    
    except HTTPException as http_exc:
        raise http_exc
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
#################################################################################################
#   DELETE CHAT BY ID
#################################################################################################
@router.delete("/{chat_id}", response_model=dict)
async def delete_chat_by_id(*, db: Session = Depends(deps.get_db), chat_id: uuid.UUID):
    try:
        db_chat = db.query(ChatModel).filter(ChatModel.id == chat_id).first()
        if not db_chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        db.delete(db_chat)
        db.commit()
        
        return {"detail": "Chat deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
    
#################################################################################################
#   GET ALL CHAT PREVIEWS FOR A USER BY USER ID
#################################################################################################
@router.get("/users/{user_id}", response_model=List[Chat])
async def get_chats_for_user(*, db: Session = Depends(deps.get_db), user_id: uuid.UUID):
    try:
        db_chats = db.query(ChatModel).filter(ChatModel.user_id == user_id).order_by(ChatModel.created_at.desc()).all()
        return db_chats
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

#################################################################################################
#   GET ALL CHAT PREVIEWS
#################################################################################################
@router.get("/", response_model=List[Chat])
async def get_chats_for_user(*, db: Session = Depends(deps.get_db)):
    try:
        db_chats = db.query(ChatModel).order_by(ChatModel.created_at.desc()).all()
        return db_chats
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))

#################################################################################################
#   UPDATE CHAT BY ID
#################################################################################################
@router.put("/{chat_id}", response_model=Chat)
async def update_chat_by_id(*, db: Session = Depends(deps.get_db), chat_id: uuid.UUID, chat_in: ChatUpdate):
    try:
        db_chat = db.query(ChatModel).filter(ChatModel.id == chat_id).first()
        if not db_chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        update_data = chat_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_chat, key, value)

        db.commit()
        db.refresh(db_chat)
        return db_chat
    except HTTPException as http_exc:
        raise http_exc
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    
    
#################################################################################################
#   GET ALL MESSAGES FOR A CHAT USING CHAT_ID
#################################################################################################
@router.get("/{chat_id}", response_model=ChatWithMessages)
async def get_chat_with_messages(*, db: Session = Depends(deps.get_db), chat_id: uuid.UUID):
    try:
        db_chat = (
            db.query(ChatModel)
            .options(joinedload(ChatModel.messages))
            .filter(ChatModel.id == chat_id)
            .first()
        )
        if not db_chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        
        # Sort messages by created_at
        db_chat.messages.sort(key=lambda message: message.created_at)
        
        return db_chat
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))