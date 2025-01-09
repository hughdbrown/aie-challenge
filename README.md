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
