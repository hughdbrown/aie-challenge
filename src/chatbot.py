import logging
import os

import chainlit as cl
import openai

from dotenv import load_dotenv

MODEL = "gpt-3.5-turbo"

system_template = "You are a helpful assistant."
user_template = "{input} Think through your response step by step."

logging_args = {
    "format": "%(asctime)s %(levelname)s %(message)s",
    "level": logging.INFO,
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "encoding": "utf-8",
}
logging.basicConfig(**logging_args)
logger = logging.getLogger(__name__)

load_dotenv()


@cl.on_chat_start
async def start_chat():
    logger.info("start_chat")
    settings = {
        "model": MODEL,
        "temperature": 0,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    cl.user_session.set("settings", settings)
    cl.user_session.set("chat_history", [])


@cl.on_message
async def on_message(message: cl.Message):
    logger.info("-" * 30)
    logger.info("> on_message")
    chat_history = cl.user_session.get("chat_history")
    chat_history.append({"role": "user", "content": message.content})
    # settings = cl.user_session.get("settings")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("Missing OPENAI_API_KEY env var")

    # client = openai.OpenAI()
    client = openai.AsyncOpenAI()
    logger.info("on_message have a client")
    # response = client.chat.completions.create(messages=chat_history, model=MODEL)
    response = await client.chat.completions.create(messages=chat_history, model=MODEL)
    logger.info("on_message have response")

    response_content = response.choices[0].message.content
    logger.info("on_message have content")
    chat_history.append({"role": "assistant", "content": response_content})
    cl.user_session.set("chat_history", chat_history)
    logger.info("on_message updated chat_history")

    await cl.Message(content=response_content).send()
    logger.info(f"on_message '{response_content[:100]}...'")

    logger.info("< on_message")
