from app.core.openai import openaiClient
from fastapi import  HTTPException
def translate_banglish_to_bangla(text: str, example_list_markdown: str):
    
    system_prompt = f"""
    You are a helpful assistant.
    You are expert in Bengali language.
    You will receive a text in Bengali or Banglish. Banglish is Bengali written in English.
    If the text is in Banglish, you need to translate it to Bengali. 
    If the text is already in Bengali, you need to keep it as it is.
    If some parts of the text is in Bengali and some parts are in Banglish, you need to translate the Banglish parts to Bengali.
    Your output MUST be in Bengali.
    You will receive some examples of Banglish to Bengali translations. The examples are as follows:
    {example_list_markdown}
    The text might be in markdown format. You MUST not change the format. Otherwise, you will be penalized $500.
    You MUST output only the translated string and nothihg else. Otherwise, you will be penalized $500.
    """

    human_prompt = f"""
    Text: {text}
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