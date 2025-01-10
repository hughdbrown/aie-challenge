import logging

import chainlit as cl

# unused imports
# from chainlit.input_widget import Select, Switch, Slider

# chainlit no longer has chainlit.prompt?
# It's moved to this?
#     from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
#
# from chainlit.prompt import Prompt, PromptMessage

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

system_template = "You are a helpful assistant."
user_template = "{input} Think through your response step by step."


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
async def on_message(message: str):
    settings = cl.user_session.get("settings")
    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="system",
                template=system_template,
                formatted=system_template,
            ),
            PromptMessage(
                role="user",
                template=user_template,
                formatted=user_template.format(input=message),
            ),
        ],
        inputs={"input": message},
        settings=settings,
    )
    print([m.to_openai() for m in prompt.messages])
    msg = cl.Message(content="")

    async for stream_resp in await openai.ChatCompletion.acreate(
        messages=[m.to_openai() for m in prompt.messages],
        stream=True,
        settings=settings,
    ):
        token = stream_resp.choices[0]["delta"].get("content", "")
        await msg.stream_token(token)

    prompt.completion = msg.content
    msg.prompt = prompt
    await msg.send()


def main():
    pass
