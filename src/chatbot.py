import logging

import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
from chainlit.prompt import Prompt, PromptMessage
from chainlit.playground.providers import ChatOpenAI
import openai

logging_args = {
    "format": "%(asctime)s %(levelname)s %(message)s",
    "level": logging.INFO,
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "encoding": "utf-8",
}
logging.basicConfig(**logging_args)
logger = logging.getLogger(__name__)

MODEL = "gpt-3.5-turbo"


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


async def chatbot():
    pass


async def main():
    # client = AsyncOpenAI()
    asyncio.run(chatbot())
