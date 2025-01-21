""" Module for chainlit implementation of Gen-AI API. """
import logging

import chainlit as cl
import openai

from dotenv import load_dotenv

MODEL = "gpt-3.5-turbo"
MSG_HISTORY_KEY = "chat_history"
SETTINGS_KEY = "settings"

logging_args = {
    "format": "%(asctime)s %(levelname)s %(name)s %(filename)s %(funcName)s %(lineno)d %(message)s",
    "level": logging.INFO,
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "encoding": "utf-8",
}
logging.basicConfig(**logging_args)
logger = logging.getLogger(__name__)

logger.info("There should be no logging before this point")
logger.info(f"{cl.version.__file__} {cl.version.__version__}")  # pylint: disable=W1203
logger.info(f"{openai.version.__file__} {openai.version.__version__}")  # pylint: disable=W1203

openai_logger = logging.getLogger("openai")
openai_logger.setLevel(logging.DEBUG)

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.DEBUG)


load_dotenv()

client = openai.AsyncOpenAI()

# Recommended in the chainlit docs for integration with openai:
# https://docs.chainlit.io/integrations/openai
cl.instrument_openai()


@cl.on_chat_start
async def start_chat():
    """ Method called on the start of chat. """
    settings = {
        "model": MODEL,
        # "temperature": 0,
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    cl.user_session.set(SETTINGS_KEY, settings)
    cl.user_session.set(MSG_HISTORY_KEY, [])


@cl.on_message
async def on_message(message: cl.Message):
    """
    Method called whenever there is a new message to submit to Gen-AI.

    on_message implementation is taken from chainlit docs:
        https://docs.chainlit.io/advanced-features/streaming
    """
    logger.info("-" * 30)
    logger.info("> on_message")

    message_history = cl.user_session.get(MSG_HISTORY_KEY)
    message_history.append({"role": "user", "content": message.content})
    settings = cl.user_session.get(SETTINGS_KEY)

    msg = cl.Message(content="")

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        token = part.choices[0].delta.content
        await msg.stream_token(token or "")

    cl.user_session.set(MSG_HISTORY_KEY, message_history)
    logger.info(f"msg = '{msg.content[:100]}...'")  # pylint: disable=W1203
    logger.info("< on_message")

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
