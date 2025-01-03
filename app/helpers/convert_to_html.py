from app.core.openai import openaiClient
from fastapi import  HTTPException

def create_html_content(file_content: str) -> str:
    system_prompt = f"""
    You are a helpful assistant. You are expert in Bengali language and html.
    You will receive a markdown file written in Bengali.
    You need to convert the markdown content to HTML.
    Your response will directly be pasted in <body> tag of a HTML file.
    Make sure you preperly parse the markdown content to HTML code.
    Consider headers, bold, italic, lists, links, breaks, etc.
    You MUST remember that, whatever you write will be directly pasted in <body> tag of a HTML file.
    If you fail to follow the instreuctions properly, you will be penalized $500.
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
        # if the content started with ```html and ended with ```,  then remove these
        resonse_content = response.choices[0].message.content
        if response.choices[0].message.content.startswith("```html") and response.choices[0].message.content.endswith("```"):
            resonse_content = response.choices[0].message.content[7:-3]

        return resonse_content
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat completion: {str(e)}")