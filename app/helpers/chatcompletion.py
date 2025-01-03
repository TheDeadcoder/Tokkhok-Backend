from app.core.openai import openaiClient
from fastapi import  HTTPException
from app.schemas.chats import OpenAiResponse
def response_first(query: str, knowledge: str) -> OpenAiResponse:
    
    system_prompt = f"""
    You are a helpful assistant. You are expert in Bengali language.
    You will receive a query in Bangla. 
    Also you will receive relevant knowledge source.
    Your job is to generate high-quality response to the query. You MUST output in Bengali. Otherwise, you will be penalized $500.
    You MUST use the knowledge source to generate the response. You MUST filter out only the knowledge points that you used to generate the response.
    You MUST follow the output format for a Response
    - response: <Your response in markdown format>
    - used_resources: <a List of vector-point IDs that you used while generating the response> 
    """

    human_prompt = f"""
    Query: {query}
    Knowledge: {knowledge}
    """
    
    try:
        completion = openaiClient.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": human_prompt},
            ],
            response_format=OpenAiResponse,
            temperature=0.5,
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat completion: {str(e)}")
    

def response_later(conversation_history: str, knowledge: str) -> OpenAiResponse:
    
    system_prompt = f"""
    You are a helpful assistant. You are expert in Bengali language.
    You will receive a conversarion.
    The User messages are in Bengali or Banglish. Banglish is Bengali written in English.
    The last user-message is the query.
    You will receive relevant knowledge source to respond to the query.
    Your job is to generate high-quality response to the query. You MUST output in Bengali. Otherwise, you will be penalized $500.
    You MUST use the knowledge source to generate the response. You MUST filter out only the knowledge points that you used to generate the response.
    You MUST follow the output format for a Response
    - response: <Your response in markdown format>
    - used_resources: <a List of vector-point IDs that you used while generating the response>
    """

    human_prompt = f"""
    conversation history: {conversation_history}
    Knowledge: {knowledge}
    """
    
    try:
        completion = openaiClient.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": human_prompt},
            ],
            response_format=OpenAiResponse,
            temperature=0.5,
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat completion: {str(e)}")
    


def response_audio(query: str, knowledge: str):
    print("in audio response")
    system_prompt = f"""
    You are a helpful assistant. You are expert in Bengali language.
    You will receive a query in English. 
    Also you will receive relevant knowledge source. The knowledge source is in Bengali.
    Your job is to generate high-quality response to the query. You MUST output in Bengali. Otherwise, you will be penalized $500.
    You MUST use the knowledge source to generate the response. If you dont find the answer in the knowledge source, you can use your knowledge generate the response.
    You MUST return the response string only and nothing else. Otherwise, you will be penalized $500.
    """

    human_prompt = f"""
    Query: {query}
    Knowledge: {knowledge}
    """
    
    try:
        response = openaiClient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": human_prompt},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat completion: {str(e)}")

