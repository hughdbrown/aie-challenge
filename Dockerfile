# FROM python:3.11
FROM python:3.9

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user
ENV PATH=/home/user/.local/bin;$PATH
ENV UVICORN_WS_PROTOCOL=websockets

WORKDIR /app/src
COPY --chown=user src .
WORKDIR /app
COPY --chown=user requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Docker/chainlit does not run properly on localhost. Needs to set 0.0.0.0 explicitly as host.
# CMD ["python", "-m", "chainlit", "run", "-h", "--port", "7860", "src/chatbot.py"]

# Is there a problem on huggingface with using port 8000? Try 7860
CMD ["python", "-m", "chainlit", "run", "-h", "--host", "0.0.0.0", "--port", "8000", "src/chatbot.py"]
