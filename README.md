---
title: "aie_challenge"
pinned: false
colorFrom: "red"
colorTo: "yellow"
sdk: "docker"
python_version: "3.11"
suggested_hardware: "cpu-basic"
app_port: 8000
---


# Purpose
This project is a response to the [AI Engineering Bootcamp challenge](https://aimakerspace.io/aie-challenge/). It is an application written in python that uses:
- python: chainlit, openai
- Docker

The instructions are not clear whether it is necessary that the app be a web app, so the final product may use FastAPI (or not).

# Setup
## src/.env
To run OpenAI models, you need the `OPENAI_API_KEY` environment variable. Adding the file `src/.env` will cause this to be injected into the runtime environment. Your `src/.env` file shold look like this:

```
OPENAI_API_KEY="<some-value>"
```

# Gnarly fix
This code includes a fix that is necessary to run on HuggingFace:

`git diff 47c5a3552b1c7d9dfd319e89afaeadbc30ce43fe..724f8df8873448591b68a7d08e8442c5e5f6e870`

```
diff --git a/Dockerfile b/Dockerfile
index 49eac70..d9d8bf7 100644
--- a/Dockerfile
+++ b/Dockerfile
@@ -5,6 +5,7 @@ RUN useradd -m -u 1000 user
 USER user
 ENV HOME=/home/user
 ENV PATH=/home/user/.local/bin;$PATH
+ENV UVICORN_WS_PROTOCOL=websockets

 WORKDIR /app/src
 COPY --chown=user src .
diff --git a/requirements.txt b/requirements.txt
index d9cd584..5854692 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -1,3 +1,4 @@
+websockets==14.1
 python-dotenv==1.0.1
 openai==1.59.5
 chainlit==2.0.0
```

The gist of it is that `chainlit` has to be running `uvicorn` via websockets to work in Hugginface. Way above my paygrade.
