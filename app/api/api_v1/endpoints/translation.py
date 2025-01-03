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
import requests
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
    


@router.post("/word")
async def generate_translation(*, db: Session = Depends(deps.get_db), translation_in: str):
    try:
        url = "https://www.google.com/inputtools/request"
        
        params = {
            "text": translation_in,
            "ime": "transliteration_en_bn",
            "num": 2,
            "ie": "utf-8",
            "oe": "utf-8",
            "app": "jsapi",
        }

        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
        
            if data[0] == "SUCCESS" and data[1] and data[1][0][1]:
                transliterated_text = data[1][0][1][0]  # First suggestion
                return transliterated_text
            else:
                raise HTTPException(status_code=400, detail="No transliteration suggestions found")
        else:
            raise HTTPException(status_code=response.status_code, detail="API Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))