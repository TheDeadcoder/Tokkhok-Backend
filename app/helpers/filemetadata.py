from app.core.openai import openaiClient
from app.schemas.files import fileMetadata

def file_metadata_create(file_content: str) -> fileMetadata:
    system_prompt = f"""
    You are a helpful assistant.
    You are expert in Bengali language.
    You will receive the content of a file written in Bengali.
    You need to generate a title, a brief caption and summary for that file. 
    Make sure the title is within 6 words.
    Make sure the caption is within 3-4 sentences.
    Make sure the summary is enough detailed to understand the content.
    Output format:
    - file_title: title of the file
    - file_caption: brief caption of
    - file_summary: detailed summary of the file. The summary MUST contain every key-point of the file
    """
    human_prompt = f"""
    File-content: {file_content}
    """

    completion = openaiClient.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt},
        ],
        response_format=fileMetadata,
        temperature=0.5
    )
    # logger.debug("OpenAI raw response: %s", completion)
    response = completion.choices[0].message.parsed

    return response