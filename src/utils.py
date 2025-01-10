from typing import List, Dict

MODEL = "gpt-3.5-turbo"


async def get_response(
    client,
    messages: List[Dict[str, str]],
    model: str = MODEL,
) -> str:
    chat_completion = await client.chat.completions.create(
        messages=messages,
        model=MODEL,
    )
    return chat_completion


def text_content(message: str) -> Dict[str, str]:
    return {"type": "text", "text": message}


def system_prompt(message: str) -> Dict[str, str]:
    return {
        "role": "system",
        "content": [text_content(message)],
    }


def user_prompt(message: str) -> Dict[str, str]:
    return {
        "role": "user",
        "content": [text_content(message)],
    }
