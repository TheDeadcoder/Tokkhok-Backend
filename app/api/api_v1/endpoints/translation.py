from typing import List
from app.helpers.translate_agent import translate_banglish_to_bangla
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import uuid
from app.api import deps
from app.db.models.usertrain import UserTrain as UserTrainModel
from app.db.models.translations import Translation as TranslationModel

from app.schemas.usertrain import userTrainBase, userTrainCreate, userTrainUpdate, userTrainInDBBase
from app.schemas.translate import TranslationBase, TranslationCreate, TranslationUpdate, TranslationInDBBase

from app.helpers.validators import validate_email
router = APIRouter()

#################################################################################################
#  Generate Trnslation
#################################################################################################
@router.post("/generate", response_model=TranslationInDBBase)
async def generate_translation(*, db: Session = Depends(deps.get_db), translation_in: TranslationCreate):
    
    try:

        db_userTrain = db.query(UserTrainModel).filter(UserTrainModel.is_approved == True).all()
        
        few_shot_prompts = "Following are some examples of translating banglish to Bengali. Banglish is Bengali written in English. \n"
        for userTrain in db_userTrain:
            few_shot_prompts += f"## Banglish-sample: {userTrain.banglish}"
            few_shot_prompts += f"## Translated Bengali-sample: {userTrain.bangla}"
            few_shot_prompts += "\n"

        translated_text = translate_banglish_to_bangla(translation_in.text, few_shot_prompts)

        print(few_shot_prompts)
        print(translated_text)


        db_translation = TranslationModel(
            text = translation_in.text,
            translated_text=translated_text,
            user_id = translation_in.user_id
        )
        db.add(db_translation)
        db.commit()
        db.refresh(db_translation)

        return db_translation
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
