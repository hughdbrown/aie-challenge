#!/usr/bin/env python3
""" Code for LLM usage. """
import asyncio
import logging
from typing import Dict, List

import chainlit as cl
from dotenv import load_dotenv
from openai import AsyncOpenAI

system_template = """
    You are a helpful assistant.
"""

user_template = """
   [input]
   Think through your response step by step.
"""

MODEL = "gpt-3.5-turbo"


logging_args = {
    "format": "%(asctime)s %(levelname)s %(message)s",
    "level": logging.INFO,
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "encoding": "utf-8",
}
logging.basicConfig(**logging_args)
logger = logging.getLogger(__name__)

openai_logger = logging.getLogger("openai")
openai_logger.setLevel(logging.WARNING)
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)


# Load environment variables from .env
load_dotenv()


@cl.on_chat_start
async def start_chat():
    settings = {
        "model": MODEL,
        "temperature": 0,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    cl.user_session.set("settings", settings)


@cl.on_message
async def on_message():
    pass    


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


async def main(client):
    messages = [
        system_prompt("You are a helpful assistant."),
        user_prompt("Assume I am a python developer. What is the difference between LangChain and LlamaIndex?"),
    ]
    result = await get_response(client, messages)
    answer = result.choices[0]
    print(answer.message.content)


if __name__ == '__main__':
    client = AsyncOpenAI()
    asyncio.run(main(client))
