from app.core.openai import openaiClient
from fastapi import  HTTPException
def prompt_normalize_first(query: str):
    
    system_prompt = f"""
    You are a helpful assistant.
    You are expert in Bengali language.
    You will receive a query in Bengali or Banglish. Banglish is Bengali written in English.
    Your job is to standardize the query in Bengali. You MUST output in Bengali.
    """

    human_prompt = f"""
    Query: {query}
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
    

def prompt_normalize_later(conversation_history: str):
    
    system_prompt = f"""
    You are a helpful assistant.
    You are expert in Bengali language.
    You will receive a conversation in Bengali or Banglish. Banglish is Bengali written in English.
    The last human message is the query.
    Your job is to standardize the query in Bengali. You MUST output in Bengali.
    If you fail to do so, you will be penalized $500.
    """

    human_prompt = f"""
    conversation history: {conversation_history}
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

