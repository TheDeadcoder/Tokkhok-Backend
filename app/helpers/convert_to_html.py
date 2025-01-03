from app.core.openai import openaiClient
from fastapi import  HTTPException

def create_html_content(file_content: str) -> str:
    system_prompt = f"""
    You are a helpful assistant.
    You are expert in Bengali language.
    You will receive a markdown content of a file written in Bengali.
    You need to generate an HTML content for that file.
    Your response will go between a <p> your content here </p> tag
    Make sure you preperly parse the markdown content to HTML
    Consider headers, bold, italic, lists, links etc.
    You just output the HTML content that goes between <p> your content here </p> tag.
    If you fail to generate the HTML content as told above, you will be penalized $500.
    """
    human_prompt = f"""
    File-content: {file_content}
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