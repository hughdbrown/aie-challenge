FROM python:3.11

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin;$PATH

WORKDIR /app/src
COPY --chown=user src .
WORKDIR /app
COPY --chown=user requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "-m", "chainlit", "run", "src/chatbot.py", "--port", "8000"]
 
