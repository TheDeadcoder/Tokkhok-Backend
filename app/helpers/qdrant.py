from fastapi import HTTPException
from qdrant_client import models
import uuid

from app.core.qdrant import qdrantClient
from app.helpers.embedding_generate import create_embedding
from qdrant_client.http.models import VectorParams, Distance

#################################################################################################
#   Helper function to make a collection
#   input: collection name, output: integer
#################################################################################################
def make_collection(collection_name:str):
    try:
        qdrantClient.get_collection(collection_name)
        return True
    except Exception as e:
        if "Not found" in str(e):
            qdrantClient.create_collection(
                collection_name,
                vectors_config={
                    "content": VectorParams(
                        size=3072,
                        distance=Distance.COSINE
                    ),
                },
            )
            rt_str = "Collection named:" + collection_name + "has been successfully created"
            return True
        else:
            raise HTTPException(status_code=500, detail="Error occurred making the collection")


#################################################################################################
#   Helper function to upload into qdrant cloud
#   input: modular file, page_no, semantic chunks, summaries and output: nothing
#################################################################################################
def upload_to_qdrant(file_id: str, file_url:str, file_title:str, file_summary: str, collection_name: str,privacy_status: str):
        make_collection(collection_name)
        payload = {
            "file_id": file_id,
            "file_summary": file_summary,
            "file_url": file_url,
            "file_title": file_title,
            "privacy_status": privacy_status
        }

        str_to_embed = file_summary
        content_embedding = create_embedding(str_to_embed)
        document_id = str(uuid.uuid4())
        qdrantClient.upsert(
            collection_name = collection_name,
            points=[
                {
                    "id": document_id,
                    "vector": {
                        "content": content_embedding
                    },
                    "payload": payload
                }
            ]
        )

#################################################################################################
#   Helper function to Get all the vector-point IDs for a particular UUID of a file
#   input: UUID of file and output: array of points
#################################################################################################
def get_points_by_uuid(collection_name:str, uuid:str):
    offset = None
    all_points = []
    
    while True:
        result = qdrantClient.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(key="file_id", match=models.MatchValue(value=uuid)),
                ]
            ),
            limit=10,  
            with_payload=True,
            with_vectors=False,
            offset=offset
        )
        
        points, next_offset = result
        all_points.extend(points)
        
        if next_offset is None:
            break
        
        offset = next_offset
    
    
    return all_points

#################################################################################################
#   Helper function to DELETE all the vector-point IDs for a particular UUID of a file
#   input: UUID and output: array of points
#################################################################################################
def delete_points_by_uuid(collection_name, uuid):
    try:
        qdrantClient.delete(
            collection_name=collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="file_id",
                            match=models.MatchValue(value=uuid),
                        ),
                    ],
                )
            ),
        )

        return True
  
    except Exception as e:
         raise HTTPException(status_code=500, detail="Error occurred while deleting from vectorDB")
    
#################################################################################################
#   Helper function to SEARCH in a collection with given query
#   input: collection, query and limit and output: array of vector points
#################################################################################################

def search_in_qdrant(collection_name, query, limit):
    try:
        embedding = create_embedding(query)
        results = qdrantClient.search(
                collection_name = collection_name,
                query_vector = ("content", embedding),
                limit=limit,
                with_payload=True,
                with_vectors=False,
            )

        return results
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while searching in vectorDB {str(e)}")
    

def update_payload_only(collection_name: str, point_id, payload: dict):
    qdrantClient.overwrite_payload(
        collection_name=collection_name,
        payload=payload,
        points=[point_id],
    )