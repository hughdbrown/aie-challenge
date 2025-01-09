#!/usr/bin/env python3
""" Code for LLM usage. """
import asyncio
import logging

from dotenv import load_dotenv
from openai import AsyncOpenAI

from utils import system_prompt, user_prompt, get_response

system_template = """
    You are a helpful assistant.
"""

user_template = """
   [input]
   Think through your response step by step.
"""



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
