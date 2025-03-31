from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
import os
from dotenv import load_dotenv

load_dotenv()  
class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY:str = os.getenv("SUPABASE_ANON_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    QDRANT_HOST: str = os.getenv("QDRANT_HOST")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME: str = "file_collection"
    LLAMACLOUD_API_1: str = os.getenv("LLAMACLOUD_API_1")
    LLAMACLOUD_API_2: str = os.getenv("LLAMACLOUD_API_2")
    LLAMACLOUD_API_3: str = os.getenv("LLAMACLOUD_API_3")
    LLAMACLOUD_API_4: str = os.getenv("LLAMACLOUD_API_4")
    LLAMACLOUD_API_5: str = os.getenv("LLAMACLOUD_API_5")
    LLAMACLOUD_API_6: str = os.getenv("LLAMACLOUD_API_6")
    LLAMACLOUD_API_7: str = os.getenv("LLAMACLOUD_API_7")
    LLAMACLOUD_API_8: str = os.getenv("LLAMACLOUD_API_8")
    LLAMACLOUD_API_9: str = os.getenv("LLAMACLOUD_API_9")
    LLAMACLOUD_API_10: str = os.getenv("LLAMACLOUD_API_10")
    LLAMACLOUD_API_11: str = os.getenv("LLAMACLOUD_API_11")
    LLAMACLOUD_API_12: str = os.getenv("LLAMACLOUD_API_12")
    LLAMACLOUD_API_13: str = os.getenv("LLAMACLOUD_API_13")
    LLAMACLOUD_API_14: str = os.getenv("LLAMACLOUD_API_14")
    LLAMACLOUD_API_15: str = os.getenv("LLAMACLOUD_API_15")
    LLAMACLOUD_API_16: str = os.getenv("LLAMACLOUD_API_16")
    LLAMACLOUD_API_17: str = os.getenv("LLAMACLOUD_API_17")
    LLAMACLOUD_API_18: str = os.getenv("LLAMACLOUD_API_18")
    LLAMACLOUD_API_19: str = os.getenv("LLAMACLOUD_API_19")
    LLAMACLOUD_API_20: str = os.getenv("LLAMACLOUD_API_20")

settings = Settings()