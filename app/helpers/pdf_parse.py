import os
from typing import List, Dict
import json
from llama_parse import LlamaParse
from llama_index.core.schema import TextNode
from app.core.config import settings
import openai
import requests
from app.core.openai import openaiClient
from app.helpers.qdrant import make_collection, upload_to_qdrant,delete_points_by_uuid
from app.core.supabase import supabase
import uuid
import nest_asyncio

nest_asyncio.apply()

def get_text_nodes(json_list: List[dict]) -> List[TextNode]:
    """Convert JSON list to a list of TextNode objects."""
    text_nodes = []
    for idx, page in enumerate(json_list):
        text_node = TextNode(text=page["md"], metadata={"page": page["page"]})
        text_nodes.append(text_node)
    return text_nodes


def get_llama_cloud_keys() -> List[str]:
    """Retrieve all LlamaCloud API keys from settings."""
    return [
        settings.LLAMACLOUD_API_1, settings.LLAMACLOUD_API_2, settings.LLAMACLOUD_API_3,
        settings.LLAMACLOUD_API_4, settings.LLAMACLOUD_API_5, settings.LLAMACLOUD_API_6,
        settings.LLAMACLOUD_API_7, settings.LLAMACLOUD_API_8, settings.LLAMACLOUD_API_9,
        settings.LLAMACLOUD_API_10, settings.LLAMACLOUD_API_11, settings.LLAMACLOUD_API_12,
        settings.LLAMACLOUD_API_13, settings.LLAMACLOUD_API_14, settings.LLAMACLOUD_API_15,
        settings.LLAMACLOUD_API_16, settings.LLAMACLOUD_API_17, settings.LLAMACLOUD_API_18,
        settings.LLAMACLOUD_API_19, settings.LLAMACLOUD_API_20
    ]

def llama_parse_pdf(pdf_path: str) -> List[Dict]:
    """Parse a PDF file using LlamaParse and return extracted text."""
    parsing_instruction = '''
    You will be given a PDF which contains banking information. You have to parse and return it in markdown format.

    **Important instructions:**
    - Output any math equation in LaTeX markdown (between $$).
    - For images, do **not** return URLs or base64 data. Instead, provide a **detailed description** of the image content, explaining what the image represents and how it is relevant to the document content.
    - Preserve the original formatting, headings, and lists as much as possible.
    '''

    llama_keys = get_llama_cloud_keys()

    for key_index, llamacloud_key in enumerate(llama_keys):

        retry_attempts = 20
        for attempt in range(retry_attempts):
            try:
                os.environ["LLAMA_CLOUD_API_KEY"] = llamacloud_key

                parser = LlamaParse(
                    result_type="markdown",
                    use_vendor_multimodal_model=True,
                    vendor_multimodal_model="openai-gpt-4o-mini",
                    invalidate_cache=True,
                    vendor_multimodal_api_key=settings.OPENAI_API_KEY,
                    parsing_instruction=parsing_instruction
                )
                print(f"Using LlamaCloud API Key {key_index + 1}, Attempt {attempt + 1}")
                json_objs = parser.get_json_result(pdf_path)

                # Validate parsing output
                if not json_objs or "pages" not in json_objs[0]:
                    raise ValueError(f"Failed to parse the file: {pdf_path}")

                return json_objs[0]["pages"]

            except Exception as e:
                print(f"Error with LlamaCloud API Key {key_index + 1}, Attempt {attempt + 1}: {str(e)}")

                # If this was the last retry attempt, move on to the next key
                if attempt == retry_attempts - 1:
                    print(f"Moving on to the next API key after {retry_attempts} failed attempts.")
                    break

    # If all keys fail
    raise Exception("All LlamaCloud API keys failed after 3 retries each.")


def process_pdf_and_generate_summaries(file_url: str):
    downloads_dir = "./uploaded_files"
    os.makedirs(downloads_dir, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = f"./uploaded_files/{file_id}.pdf"
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # Parse the PDF
        pages = llama_parse_pdf(file_path)

        complete_text = ""

        for page in pages:
            page_text = page["md"]
            complete_text += page_text


        return complete_text
    except Exception as e:
        print(f"Error while processing the file: {str(e)}")
        # update_file_status(file_id, "Failed")
    finally:
        # Cleanup: Remove the downloaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)
