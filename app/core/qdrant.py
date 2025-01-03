import qdrant_client
from qdrant_client import QdrantClient
from app.core.config import settings

qdrantClient = qdrant_client.QdrantClient(settings.QDRANT_HOST, api_key = settings.QDRANT_API_KEY,timeout=100.0)