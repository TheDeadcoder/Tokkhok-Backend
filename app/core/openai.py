import openai
from app.core.config import settings

openaiClient = openai.Client(api_key = settings.OPENAI_API_KEY)