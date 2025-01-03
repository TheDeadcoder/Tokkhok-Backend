from typing import List
from app.helpers.convert_to_html import create_html_content
from app.helpers.qdrant import get_points_by_uuid, update_payload_only, upload_to_qdrant, delete_points_by_uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import uuid
from app.api import deps
import os
from app.helpers.fileupload import upload_file_to_supabase, delete_file_from_supabase
from weasyprint import HTML, CSS
from app.helpers.filemetadata import file_metadata_create
from datetime import datetime
from app.db.models.users import User as UserModel
from app.db.models.files import File as FileModel
from app.core.config import settings
from app.schemas.files import FileCreate, FileInDBBase, FileUpdate
router = APIRouter()

#################################################################################################
# GET all files
#################################################################################################
@router.get("/", response_model=List[FileInDBBase])
async def get_all_files(db: Session = Depends(deps.get_db)):
    try:
        db_file = db.query(FileModel).all()
        return db_file
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
    

PDF_DIR = "uploaded_files"

def create_bengali_pdf_weasy(bengali_text: str, output_path: str):
    curated_bd_text = bengali_text
    html_content = f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="utf-8">
        <style>
            @font-face {{
                font-family: "NotoSansBengali";
                src: url("uploaded_files/noto.ttf");
            }}
            body {{
                font-family: "NotoSansBengali", sans-serif;
                font-size: 16px;
                margin: 50px;
                line-height: 1.5;
            }}
            h1, h2, h3, h4, h5, h6 {{
                font-weight: bold;
                margin: 15px 0;
            }}
            p {{
                margin: 10px 0;
            }}
            ul, ol {{
                margin: 10px 20px;
            }}
            li {{
                margin-bottom: 5px;
            }}
        </style>
    </head>
    <body>
        {curated_bd_text}
    </body>
    </html>
    """

    
    HTML(string=html_content).write_pdf(output_path)
    return output_path
#################################################################################################
# ingest a file
#################################################################################################
@router.post("/", response_model=FileInDBBase)
async def create_file(
    query: FileCreate,
    db: Session = Depends(deps.get_db)
):
    
    try:
        # generating title and caption
        metadata = file_metadata_create(query.text)

        file_title = metadata.file_title
        file_caption = metadata.file_caption
        file_summary = metadata.file_summary

        curated_text = create_html_content(query.text)

        image_url = "https://btrnqywodfpanpiyjjiw.supabase.co/storage/v1/object/public/contents/default-image.png"

        if query.image_url:
            image_url = query.image_url

        print(file_title, file_caption)

        # You mentioned using WeasyPrint
        output_path = os.path.join(PDF_DIR, f"{uuid.uuid4()}.pdf")
        create_bengali_pdf_weasy(curated_text, output_path)

        # Convert the output_path file to bytes
        with open(output_path, "rb") as f:
            file_bytes = f.read()

        # Upload to Supabase
        public_url = upload_file_to_supabase(file_bytes, query.uploader_id)

        

        # Create DB entry
        db_file = FileModel(
            file_title = file_title,
            file_caption = file_caption,
            uploader_id = query.uploader_id,
            privacy_status = query.privacy_status,
            file_url = public_url,
            uploaded_at = datetime.now(),
            tags = query.tags,
            image_url = image_url
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        upload_to_qdrant(str(db_file.id), public_url, file_title, file_summary, settings.COLLECTION_NAME, query.privacy_status, query.text)

        # Remove the local file after uploading
        os.remove(output_path)

        return db_file
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating PDF: {str(e)}")


#################################################################################################
# update file metadatas
#################################################################################################
@router.put("/{file_id}", response_model=FileInDBBase)
async def update_file_metadata(*, db: Session = Depends(deps.get_db), file_id: uuid.UUID, fileupdate_in: FileUpdate):
    
    try:
        db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        if fileupdate_in.file_title:
            db_file.file_title = fileupdate_in.file_title
        if fileupdate_in.file_caption:
            db_file.file_caption = fileupdate_in.file_caption
        if fileupdate_in.privacy_status:
            db_file.privacy_status = fileupdate_in.privacy_status
        if fileupdate_in.status:
            db_file.status = fileupdate_in.status

        points = get_points_by_uuid(settings.COLLECTION_NAME,str(db_file.id))
            
        for point in points:
            current_payload = point.payload
                
                
            updated_payload = current_payload.copy()

            if fileupdate_in.file_title:
                updated_payload['file_title'] = fileupdate_in.file_title
            if fileupdate_in.privacy_status:
                updated_payload['privacy_status'] = fileupdate_in.privacy_status

            update_payload_only(
                    collection_name=settings.COLLECTION_NAME,
                    point_id=point.id,
                    payload=updated_payload
            )

        

        
        db.commit()
        db.refresh(db_file)
        return db_file
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))
    

#################################################################################################
# delete a file
#################################################################################################
@router.delete("/{file_id}")
async def delete_file(file_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    
    try:
        db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
        if not db_file:
            raise HTTPException(status_code=404, detail="file not found")
        

        delete_points_by_uuid(settings.COLLECTION_NAME, str(file_id))
        db.delete(db_file)
        db.commit()
        return {"message": "db_file deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))